"""Live job notification sync: runs Apify actors and upserts their rows into ``jobs``.

Design notes
------------
* Actor runs are started concurrently and polled until terminal, so one slow source
  does not serialise the whole sync (the admin button is a single HTTP request).
* Rows are keyed by ``(source, external_id)`` and upserted, so repeat syncs update
  in place instead of duplicating.
* The first successful sync removes the hand-written seed jobs so the board shows
  only real, current notifications.
"""
from __future__ import annotations

import html
import re
import time
import xml.etree.ElementTree as ET
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date, datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any

import httpx
from sqlalchemy import delete, func, select, update
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import Job
from app.services.common import naive_utc_now

APIFY_BASE = "https://api.apify.com/v2"
_ACTIVE_STATUSES = ("READY", "RUNNING")
_POLL_INTERVAL_SECONDS = 2.0

_WHITESPACE = re.compile(r"\s+")
_TAG = re.compile(r"<[^>]+>")

_SEED_SOURCE_KEY = "__seed__"


@dataclass(frozen=True)
class SourceSpec:
    key: str
    label: str
    job_type: str  # government | it
    actor: str
    build_input: Callable[[int], dict]
    map_item: Callable[[dict], dict | None]


# --------------------------------------------------------------------------
# generic text / date helpers
# --------------------------------------------------------------------------


def _text(value: Any, limit: int = 300) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple, set)):
        parts = [_text(v, limit) for v in value]
        value = ", ".join(p for p in parts if p)
    text = _WHITESPACE.sub(" ", str(value)).strip()
    return text[:limit]


def _plain_text(value: Any, limit: int = 1500) -> str:
    if not value:
        return ""
    return _text(html.unescape(_TAG.sub(" ", str(value))), limit)


def _range(value: Any, limit: int = 255) -> str:
    if isinstance(value, (list, tuple)) and len(value) == 2:
        return f"{_text(value[0], 80)} - {_text(value[1], 80)}"[:limit]
    return _text(value, limit)


def _money(value: Any) -> str:
    if isinstance(value, bool):
        return ""
    if isinstance(value, (int, float)):
        return f"{value:,.0f}" if float(value).is_integer() else f"{value:,.2f}"
    return _text(value, 30)


def _salary_text(value: Any) -> str:
    if not value or not isinstance(value, dict):
        return _range(value)
    lo, hi = value.get("min"), value.get("max")
    currency = _text(value.get("currencyCode"), 12)
    unit = _text(value.get("type"), 12).lower()
    suffix = {"year": "/yr", "month": "/mo", "hour": "/hr", "day": "/day"}.get(unit, "")
    if lo is not None and hi is not None:
        body = f"{_money(lo)} - {_money(hi)}"
    elif lo is not None:
        body = _money(lo)
    elif hi is not None:
        body = _money(hi)
    else:
        return ""
    return f"{body} {currency}{suffix}".strip()


_DATE_FORMATS = (
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%Y/%m/%d",
    "%d.%m.%Y",
    "%d %b %Y",
    "%d %B %Y",
    "%b %d, %Y",
    "%B %d, %Y",
)
_ISO_DATE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
_SLASH_DATE = re.compile(r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b")


def parse_date(value: Any) -> date | None:
    """Best-effort date parse for the loose date strings the sources publish."""
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        seconds = float(value)
        if seconds > 100_000_000_000:  # milliseconds
            seconds /= 1000.0
        try:
            return datetime.fromtimestamp(seconds, tz=timezone.utc).date()
        except (OverflowError, OSError, ValueError):
            return None
    text = _text(value, 64)
    if not text:
        return None
    head = text.split("T", 1)[0].strip()
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(head, fmt).date()
        except ValueError:
            continue
    match = _ISO_DATE.search(text)
    if match:
        year, month, day = (int(part) for part in match.groups())
        try:
            return date(year, month, day)
        except ValueError:
            pass
    match = _SLASH_DATE.search(text)
    if match:
        first, second, year = (int(part) for part in match.groups())
        for month, day in ((first, second), (second, first)):
            try:
                return date(year, month, day)
            except ValueError:
                continue
    return None


# --------------------------------------------------------------------------
# category derivation
# --------------------------------------------------------------------------

_GOV_CATEGORIES = {
    "jobs": "notification",
    "job": "notification",
    "notification": "notification",
    "notifications": "notification",
    "admissions": "notification",
    "latest-notifications": "notification",
    "bank-jobs": "notification",
    "railway-jobs": "notification",
    "engineering-jobs": "notification",
    "sarkari-naukri": "notification",
    "admit-card": "admit-card",
    "admitcards": "admit-card",
    "result": "result",
    "results": "result",
    "answer-keys": "result",
    "exam-date": "upcoming",
    "syllabus": "upcoming",
}


def gov_category(value: Any, fallback: str = "notification") -> str:
    key = _text(value, 60).lower().replace("_", "-").replace(" ", "-")
    return _GOV_CATEGORIES.get(key, fallback)


_FRESHER_HINTS = ("junior", "graduate", "trainee", "entry level", "entry-level", "fresher")
_CONTRACT_HINTS = ("contract", "freelance", "temporary", "part-time", "part time")


def it_category(title: str, employment_type: Any = "", remote: bool = False) -> str:
    blob = f"{title} {employment_type}".lower()
    if "intern" in blob:
        return "internship"
    if any(hint in blob for hint in _FRESHER_HINTS):
        return "fresher"
    if remote or "remote" in blob:
        return "remote"
    if any(hint in blob for hint in _CONTRACT_HINTS):
        return "contract"
    return "fulltime"


def _is_remote(*values: Any) -> bool:
    for value in values:
        if isinstance(value, bool) and value:
            return True
        if "remote" in _text(value, 200).lower():
            return True
    return False


# --------------------------------------------------------------------------
# per-source mappers
# --------------------------------------------------------------------------


def _map_freejobalert(item: dict) -> dict | None:
    title = _text(item.get("postName"), 300) or _text(item.get("recruitmentBoard"), 300)
    detail_url = _text(item.get("detailUrl"), 1000)
    if not title or not detail_url:
        return None
    qualification = _text(item.get("qualification"), 400)
    advt_no = _text(item.get("advtNo"), 120)
    parts = [part for part in (qualification, f"Advertisement no. {advt_no}" if advt_no else "") if part]
    return {
        "title": title,
        "company": _text(item.get("recruitmentBoard"), 255),
        "type": "government",
        "category": gov_category(item.get("section")),
        "description": _text(" \u2022 ".join(parts), 1200)
        or "Government recruitment notification published on FreeJobAlert.",
        "location": "All India",
        "salary": "",
        "apply_link": detail_url,
        "deadline": parse_date(item.get("lastDate")),
        "source": "freejobalert",
        "external_id": detail_url,
        "posted_at": parse_date(item.get("postDate")),
    }


def _map_sarkariresult(item: dict) -> dict | None:
    title = _text(item.get("title"), 300)
    source_url = _text(item.get("sourceUrl"), 1000)
    if not title or not source_url:
        return None
    application_links = item.get("officialApplicationUrls") or []
    apply_link = _text(application_links[0], 1000) if application_links else source_url
    if not apply_link:
        apply_link = source_url
    summary = _text(item.get("summary"), 700)
    qualification = _text(item.get("qualificationsText"), 400)
    posts = _text(item.get("jobTitles"), 300)
    vacancy = item.get("vacancyTotal")
    parts = [
        part
        for part in (
            summary,
            f"Posts: {posts}" if posts else "",
            f"Vacancies: {vacancy}" if vacancy not in (None, "") else "",
            f"Qualification: {qualification}" if qualification else "",
        )
        if part
    ]
    return {
        "title": title,
        "company": _text(item.get("organization"), 255),
        "type": "government",
        "category": gov_category(item.get("sourceType")),
        "description": _text(" \u2022 ".join(parts), 1500)
        or "Government notification published on SarkariResult.",
        "location": _text(item.get("locations") or "All India", 255) or "All India",
        "salary": "",
        "apply_link": apply_link,
        "deadline": parse_date(item.get("applicationDeadlineAt")),
        "source": "sarkariresult",
        "external_id": _text(item.get("recordId"), 120) or source_url,
        "posted_at": parse_date(item.get("sourcePublishedAt")),
    }


def _map_rojgarlive(item: dict) -> dict | None:
    title = _text(item.get("title"), 300)
    source_url = _text(item.get("sourceUrl"), 1000)
    if not title or not source_url:
        return None
    application_links = item.get("officialApplicationUrls") or []
    apply_link = _text(application_links[0], 1000) if application_links else source_url
    if not apply_link:
        apply_link = source_url
    summary = _text(item.get("summary"), 700)
    posts = _text(item.get("jobTitles"), 300)
    vacancy = item.get("vacancyCount")
    qualification = _text(item.get("qualificationsText"), 400)
    locations = _text(item.get("locations"), 255)
    salary = _text(item.get("salaryText"), 255)
    parts = [
        part
        for part in (
            summary,
            f"Posts: {posts}" if posts else "",
            f"Vacancies: {vacancy}" if vacancy not in (None, "") else "",
            f"Qualification: {qualification}" if qualification else "",
        )
        if part
    ]
    return {
        "title": title,
        "company": _text(item.get("organization"), 255),
        "type": "government",
        "category": gov_category(item.get("category") or item.get("contentType")),
        "description": _text(" \u2022 ".join(parts), 1500)
        or "Government notification published on RojgarLive.",
        "location": locations or "All India",
        "salary": salary,
        "apply_link": apply_link,
        "deadline": parse_date(item.get("applicationDeadlineAt")),
        "source": "rojgarlive",
        "external_id": _text(item.get("recordId"), 120) or source_url,
        "posted_at": parse_date(item.get("sourcePublishedAt")),
    }


def _map_linkedin(item: dict) -> dict | None:
    title = _text(item.get("title"), 300)
    link = _text(item.get("link"), 1000)
    job_id = _text(item.get("id"), 120)
    if not title or not (job_id or link):
        return None
    employment_type = item.get("employmentType")
    remote = _is_remote(item.get("workRemoteAllowed"), item.get("workplaceTypes"))
    description = _plain_text(item.get("descriptionText")) or _plain_text(item.get("descriptionHtml"))
    return {
        "title": title,
        "company": _text(item.get("companyName"), 255),
        "type": "it",
        "category": it_category(title, employment_type, remote),
        "description": description or "IT job listing published on LinkedIn.",
        "location": _text(item.get("location"), 255),
        "salary": _range(item.get("salaryInfo")),
        "apply_link": link or "#",
        "deadline": parse_date(item.get("expireAt")),
        "source": "linkedin",
        "external_id": job_id or link,
        "posted_at": parse_date(item.get("postedAt")),
    }


def _map_indeed(item: dict) -> dict | None:
    title = _text(item.get("title"), 300)
    if not title:
        return None
    job_id = _text(item.get("id"), 120)
    apply_link = _text(item.get("originalApplyUrl"), 1000)
    view_link = _text(item.get("viewJobLink"), 1000)
    if apply_link.startswith("/"):
        apply_link = f"https://www.indeed.com{apply_link}"
    elif not apply_link and view_link:
        apply_link = (
            view_link
            if view_link.startswith("http")
            else f"https://www.indeed.com{view_link if view_link.startswith('/') else f'/viewjob{view_link}'}"
        )
    if not apply_link:
        apply_link = view_link or "#"
    if not job_id and apply_link == "#":
        return None
    company_details = item.get("companyDetails") or {}
    employment_type = _text(item.get("jobTypes"), 80)
    description = _plain_text(item.get("jobDescription"))
    return {
        "title": title,
        "company": _text(company_details.get("name"), 255) or _text(item.get("jobSourceName"), 255),
        "type": "it",
        "category": it_category(title, employment_type, remote=False),
        "description": description or "IT job listing published on Indeed.",
        "location": _text(item.get("formattedLocation") or item.get("location"), 255),
        "salary": _salary_text(item.get("salary")),
        "apply_link": apply_link,
        "deadline": parse_date(item.get("expirationDate")),
        "source": "indeed",
        "external_id": job_id or apply_link,
        "posted_at": parse_date(item.get("pubDate")),
    }


# --------------------------------------------------------------------------
# remote job boards: direct feeds (public HTTP, no Apify credits, always fresh)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class FeedSpec:
    key: str
    label: str
    fetch: Callable[[httpx.Client], list[dict]]
    map_item: Callable[[dict], dict | None]


def _public_client() -> httpx.Client:
    """Feeds are public: never send the Apify token to third-party sites."""
    return httpx.Client(
        timeout=httpx.Timeout(60.0),
        follow_redirects=True,
        headers={"User-Agent": "CareerPrepHub/1.0"},
    )


def _fetch_remoteok(client: httpx.Client) -> list[dict]:
    response = client.get("https://remoteok.com/api")
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list):
        return []
    return [item for item in payload if isinstance(item, dict) and item.get("id")]


def _remoteok_salary(item: dict) -> str:
    def amount(value: Any) -> str:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return ""
        return _money(value)

    lo, hi = amount(item.get("salary_min")), amount(item.get("salary_max"))
    if lo and hi:
        return f"{lo} - {hi}"
    return lo or hi


def _map_remoteok(item: dict) -> dict | None:
    title = _text(item.get("position"), 300)
    external_id = _text(item.get("id"), 120)
    if not title or not external_id:
        return None
    url = _text(item.get("url"), 1000)
    if url.startswith("http"):
        apply_link = url
    elif url.startswith("/"):
        apply_link = f"https://remoteok.com{url}"
    else:
        apply_link = "https://remoteok.com"
    return {
        "title": title,
        "company": _text(item.get("company"), 255),
        "type": "it",
        "category": it_category(title, "", remote=True),
        "description": _plain_text(item.get("description"), 1500)
        or "Remote job listing published on RemoteOK.",
        "location": _text(item.get("location"), 255) or "Remote",
        "salary": _remoteok_salary(item),
        "apply_link": apply_link,
        "deadline": None,
        "source": "remoteok",
        "external_id": external_id,
        "posted_at": parse_date(item.get("date")),
    }


def _fetch_remotive(client: httpx.Client) -> list[dict]:
    response = client.get("https://remotive.com/api/remote-jobs", params={"limit": 100})
    response.raise_for_status()
    payload = response.json()
    jobs = payload.get("jobs", []) if isinstance(payload, dict) else []
    return [job for job in jobs if isinstance(job, dict) and job.get("id")]


def _map_remotive(item: dict) -> dict | None:
    title = _text(item.get("title"), 300)
    external_id = _text(item.get("id"), 120)
    if not title or not external_id:
        return None
    return {
        "title": title,
        "company": _text(item.get("company_name"), 255),
        "type": "it",
        "category": it_category(title, item.get("job_type"), remote=True),
        "description": _plain_text(item.get("description"), 1500)
        or "Remote job listing published on Remotive.",
        "location": _text(item.get("candidate_required_location"), 255) or "Remote",
        "salary": _text(item.get("salary"), 255),
        "apply_link": _text(item.get("url"), 1000) or "https://remotive.com",
        "deadline": None,
        "source": "remotive",
        "external_id": external_id,
        "posted_at": parse_date(item.get("publication_date")),
    }


_WWR_FEEDS = [
    "https://weworkremotely.com/categories/remote-programming-jobs.rss",
    "https://weworkremotely.com/categories/remote-devops-sysadmin-jobs.rss",
    "https://weworkremotely.com/categories/remote-design-jobs.rss",
    "https://weworkremotely.com/categories/remote-customer-support-jobs.rss",
]

_WWR_HEADQUARTERS = re.compile(r"headquarters:\s*</strong>\s*([^<]+)", re.IGNORECASE)


def _fetch_wwr(client: httpx.Client) -> list[dict]:
    out: list[dict] = []
    for url in _WWR_FEEDS:
        response = client.get(url)
        response.raise_for_status()
        root = ET.fromstring(response.text)
        for entry in root.findall("./channel/item"):
            out.append(
                {
                    tag: (node.text or "" if (node := entry.find(tag)) is not None else "")
                    for tag in ("title", "link", "guid", "pubDate", "description")
                }
            )
    return out


def _wwr_company_title(raw: Any) -> tuple[str, str]:
    """WeWorkRemotely titles look like ``"Acme: Senior Backend Engineer"``."""
    title = _text(raw, 300)
    if ": " in title:
        company, _, rest = title.partition(": ")
        if company and rest and len(company) <= 60:
            return _text(company, 255), rest
    return "", title


def _wwr_location(description_html: Any) -> str:
    match = _WWR_HEADQUARTERS.search(str(description_html or ""))
    if match:
        place = _text(match.group(1), 120)
        if place:
            return "Remote" if "remote" in place.lower() else place
    return "Remote"


def _wwr_date(value: Any) -> date | None:
    try:
        return parsedate_to_datetime(str(value)).date()
    except (TypeError, ValueError, OverflowError, IndexError):
        return None


def _map_wwr(item: dict) -> dict | None:
    company, title = _wwr_company_title(item.get("title"))
    link = _text(item.get("link"), 1000)
    guid = _text(item.get("guid"), 500)
    if not title or not (guid or link):
        return None
    description = item.get("description") or ""
    return {
        "title": title,
        "company": company,
        "type": "it",
        "category": it_category(title, "", remote=True),
        "description": _plain_text(description, 1500)
        or "Remote job listing published on WeWorkRemotely.",
        "location": _wwr_location(description),
        "salary": "",
        "apply_link": link or guid or "https://weworkremotely.com",
        "deadline": None,
        "source": "weworkremotely",
        "external_id": guid or link,
        "posted_at": _wwr_date(item.get("pubDate")),
    }


_NODESK_ITEM = re.compile(r"<item>(.*?)</item>", re.S | re.I)
_NODESK_FIELD = re.compile(r"<(title|link|guid|pubDate|description)>(.*?)</\1>", re.S | re.I)
_NODESK_CDATA = re.compile(r"<!\[CDATA\[(.*?)\]\]>", re.S)


def _fetch_nodesk(client: httpx.Client) -> list[dict]:
    # The feed embeds bare HTML entities, so regex beats a strict XML parser.
    response = client.get("https://nodesk.co/remote-jobs/index.xml")
    response.raise_for_status()
    out: list[dict] = []
    for block in _NODESK_ITEM.findall(response.text):
        row: dict[str, str] = {}
        for tag, raw in _NODESK_FIELD.findall(block):
            text = _NODESK_CDATA.sub(r"\1", raw)
            row[tag.lower()] = html.unescape(text).strip()
        if row.get("title"):
            out.append(row)
    return out


def _nodesk_company_title(raw: Any) -> tuple[str, str]:
    """NoDesk titles look like ``"Senior Designer at Acme"``."""
    title = _text(raw, 300)
    if " at " in title:
        role, _, company = title.rpartition(" at ")
        if role and company and len(company) <= 60:
            return _text(company, 255), role
    return "", title


def _map_nodesk(item: dict) -> dict | None:
    company, title = _nodesk_company_title(item.get("title"))
    link = _text(item.get("link"), 1000)
    guid = _text(item.get("guid"), 500)
    if not title or not (guid or link):
        return None
    return {
        "title": title,
        "company": company,
        "type": "it",
        "category": it_category(title, "", remote=True),
        "description": _plain_text(item.get("description"), 1500)
        or "Remote job listing published on NoDesk.",
        "location": "Remote",
        "salary": "",
        "apply_link": link or guid or "https://nodesk.co/remote-jobs/",
        "deadline": None,
        "source": "nodesk",
        "external_id": guid or link,
        "posted_at": _wwr_date(item.get("pubdate")),
    }


REMOTE_FEEDS: list[FeedSpec] = [
    FeedSpec(key="remoteok", label="RemoteOK", fetch=_fetch_remoteok, map_item=_map_remoteok),
    FeedSpec(key="remotive", label="Remotive", fetch=_fetch_remotive, map_item=_map_remotive),
    FeedSpec(
        key="weworkremotely",
        label="WeWorkRemotely",
        fetch=_fetch_wwr,
        map_item=_map_wwr,
    ),
    FeedSpec(key="nodesk", label="NoDesk", fetch=_fetch_nodesk, map_item=_map_nodesk),
]


# Every remote job website learners actually ask for. Boards this app crawls
# into the Remote tab are marked live; the rest are shown as directory cards
# that link out (paywalled, login-walled or JS-only sites cannot be scraped).
REMOTE_SITES: list[dict] = [
    {
        "name": "We Work Remotely",
        "url": "https://weworkremotely.com",
        "blurb": "Largest remote-only board; screened programming, design, marketing roles.",
        "live": True,
    },
    {
        "name": "RemoteOK",
        "url": "https://remoteok.com",
        "blurb": "High-volume global tech board, nomad-friendly roles.",
        "live": True,
    },
    {
        "name": "Remotive",
        "url": "https://remotive.com",
        "blurb": "Frequently refreshed remote jobs with global filters.",
        "live": True,
    },
    {
        "name": "NoDesk",
        "url": "https://nodesk.co",
        "blurb": "Curated remote jobs, guides and company profiles.",
        "live": True,
    },
    {
        "name": "LinkedIn",
        "url": "https://www.linkedin.com/jobs/",
        "blurb": "Corporate remote openings plus networking.",
        "live": True,
    },
    {
        "name": "Remote.co",
        "url": "https://remote.co",
        "blurb": "Curated listings: support, design, data entry, writing.",
        "live": False,
    },
    {
        "name": "FlexJobs",
        "url": "https://www.flexjobs.com",
        "blurb": "Hand-screened verified remote roles (subscription).",
        "live": False,
    },
    {
        "name": "Surely Remote",
        "url": "https://surelyremote.com",
        "blurb": "Hand-screened work-from-home jobs for Indian professionals.",
        "live": False,
    },
    {
        "name": "Wellfound",
        "url": "https://wellfound.com",
        "blurb": "Startup and tech remote roles with salary upfront.",
        "live": False,
    },
    {
        "name": "Upwork",
        "url": "https://www.upwork.com",
        "blurb": "Contract and long-term freelance remote work.",
        "live": False,
    },
    {
        "name": "Fiverr",
        "url": "https://www.fiverr.com",
        "blurb": "Gig-style project tasks: editing, design, writing.",
        "live": False,
    },
]


# --------------------------------------------------------------------------
# source definitions
# --------------------------------------------------------------------------


def _residential_proxy() -> dict:
    return {"useApifyProxy": True, "apifyProxyGroups": ["RESIDENTIAL"], "apifyProxyCountry": "IN"}


def _freejobalert_input(max_items: int) -> dict:
    return {
        "sections": ["latest-notifications", "bank-jobs", "railway-jobs", "engineering-jobs"],
        "maxItems": max_items,
        "proxyConfiguration": _residential_proxy(),
        "disableUsageStats": True,
    }


def _sarkariresult_input(max_items: int) -> dict:
    return {
        "mode": "latestSnapshot",
        "updateTypes": ["jobs", "admitCards", "results"],
        "articleUrls": [],
        "search": "",
        "onlyOpen": False,
        "includeDetails": True,
        "includeOfficialLinks": True,
        "includeStructuredTables": False,
        "maxItems": max_items,
        "maxDetailRequests": max_items,
        "maxPagesPerType": 2,
        "maxConcurrency": 2,
        "outputMode": "allMatches",
        "monitorScope": "careerprep-snapshot",
        "retries": 2,
        "proxyConfiguration": {},
    }


def _rojgarlive_input(max_items: int) -> dict:
    return {
        "mode": "latestFeed",
        "categories": ["sarkari-naukri", "admit-card", "result"],
        "searchQueries": [],
        "articleUrls": [],
        "includeNonJobUpdates": False,
        "organizationKeywords": [],
        "titleKeywords": [],
        "onlyOpen": False,
        "includeDetails": True,
        "includeOfficialLinks": True,
        "includeJobPostingMetadata": True,
        "maxItems": max_items,
        "maxPages": 2,
        "maxDetailRequests": max_items,
        "maxConcurrency": 2,
        "outputMode": "allMatches",
        "monitorScope": "careerprep-snapshot",
        "retries": 2,
        "proxyConfiguration": {},
    }


def _linkedin_input(keywords: str, cap: int = 8) -> Callable[[int], dict]:
    def build(max_items: int) -> dict:
        return {
            "urls": [],
            "keywords": keywords,
            "location": "India",
            "datePosted": "pastMonth",
            "companyIds": [],
            "under10Applicants": False,
            "autoConvertToAiSearch": True,
            "scrapeCompany": False,
            "limitPerSource": max(1, min(cap, max_items or cap)),
            "splitByLocation": False,
        }

    return build


def _indeed_input(query: str, location: str, cap: int = 12) -> Callable[[int], dict]:
    def build(max_items: int) -> dict:
        return {
            "country": "in",
            "query": query,
            "location": location,
            "radiusKm": 50,
            "count": max(1, min(cap, max_items or cap)),
        }

    return build


# Every developer discipline job seekers actually search for. Each entry becomes its
# own actor run so the board shows the whole market in one place rather than the two
# or three generic queries the app started with.
_LINKEDIN_ROLES = [
    "software engineer",
    "software developer",
    "frontend developer",
    "backend developer",
    "full stack developer",
    "react developer",
    "angular developer",
    "node js developer",
    "python developer",
    "java developer",
    "dotnet developer",
    "golang developer",
    "devops engineer",
    "cloud engineer",
    "data analyst",
    "data scientist",
    "machine learning engineer",
    "android developer",
    "flutter developer",
    "qa automation engineer",
    "mern stack developer",
    "database developer",
    "cyber security analyst",
    "technical support engineer",
]

_INDEED_ROLES = [
    "software engineer",
    "software developer",
    "frontend developer",
    "backend developer",
    "full stack developer",
    "react developer",
    "python developer",
    "java developer",
    "devops engineer",
    "data analyst",
    "software test engineer",
    "web developer",
]


SOURCES: list[SourceSpec] = [
    SourceSpec(
        key="freejobalert",
        label="FreeJobAlert",
        job_type="government",
        actor="bovi/freejobalert-jobs",
        build_input=_freejobalert_input,
        map_item=_map_freejobalert,
    ),
    SourceSpec(
        key="sarkariresult",
        label="SarkariResult",
        job_type="government",
        actor="getascraper/sarkariresult-jobs-monitor",
        build_input=_sarkariresult_input,
        map_item=_map_sarkariresult,
    ),
    SourceSpec(
        key="rojgarlive",
        label="RojgarLive",
        job_type="government",
        actor="getascraper/rojgarlive-jobs-monitor",
        build_input=_rojgarlive_input,
        map_item=_map_rojgarlive,
    ),
    *[
        SourceSpec(
            key="linkedin",
            label="LinkedIn",
            job_type="it",
            actor="curious_coder/linkedin-jobs-scraper",
            build_input=_linkedin_input(role),
            map_item=_map_linkedin,
        )
        for role in _LINKEDIN_ROLES
    ],
    *[
        SourceSpec(
            key="indeed",
            label="Indeed",
            job_type="it",
            actor="curious_coder/indeed-scraper",
            build_input=_indeed_input(role, "India"),
            map_item=_map_indeed,
        )
        for role in _INDEED_ROLES
    ],
]


def available_sources() -> list[dict]:
    """Distinct sources the admin UI can offer."""
    seen: dict[tuple[str, str], SourceSpec] = {}
    for spec in SOURCES:
        seen.setdefault((spec.key, spec.job_type), spec)
    return [
        {"key": spec.key, "label": spec.label, "job_type": spec.job_type}
        for spec in seen.values()
    ]


# Remote-only Apify queries. Kept out of SOURCES so the daily sync stays cheap;
# they run on demand through the "remote" track. The LinkedIn/Indeed mappers
# already detect remote flags and titles, so no new mappers are needed.
_LINKEDIN_REMOTE_ROLES = [
    "remote software engineer",
    "remote frontend developer",
    "remote backend developer",
    "remote full stack developer",
    "remote python developer",
    "remote react developer",
    "remote devops engineer",
    "remote data analyst",
]

_INDEED_REMOTE_ROLES = [
    "software engineer",
    "frontend developer",
    "backend developer",
    "full stack developer",
    "python developer",
    "data analyst",
]

REMOTE_SOURCES: list[SourceSpec] = [
    *[
        SourceSpec(
            key="linkedin-remote",
            label="LinkedIn Remote",
            job_type="it",
            actor="curious_coder/linkedin-jobs-scraper",
            build_input=_linkedin_input(role, cap=6),
            map_item=_map_linkedin,
        )
        for role in _LINKEDIN_REMOTE_ROLES
    ],
    *[
        SourceSpec(
            key="indeed-remote",
            label="Indeed Remote",
            job_type="it",
            actor="curious_coder/indeed-scraper",
            build_input=_indeed_input(role, "Remote", cap=8),
            map_item=_map_indeed,
        )
        for role in _INDEED_REMOTE_ROLES
    ],
]


# --------------------------------------------------------------------------
# Apify client
# --------------------------------------------------------------------------


def _client() -> httpx.Client:
    # The token travels in a header so it never lands in a URL, log line or error message.
    return httpx.Client(
        timeout=httpx.Timeout(60.0),
        follow_redirects=True,
        headers={"Authorization": f"Bearer {settings.apify_token}"},
    )


def _actor_path(actor: str) -> str:
    """Apify addresses store actors as ``username~name`` in REST paths."""
    return actor.replace("/", "~", 1)


_RETRYABLE_STATUS = {402, 429, 500, 502, 503, 504}
_MAX_ATTEMPTS = 3


def _http_error(response: httpx.Response) -> httpx.HTTPStatusError:
    """Build an error that carries the API's explanation but never the token."""
    body = _text(response.text, 300)
    message = f"{response.status_code} {response.reason_phrase} for {response.request.url.path}"
    if body:
        message = f"{message}: {body}"
    return httpx.HTTPStatusError(message, request=response.request, response=response)


def _start_run(client: httpx.Client, spec: SourceSpec, max_items: int) -> dict:
    """Start one actor run, retrying the transient errors Apify returns under load."""
    url = f"{APIFY_BASE}/acts/{_actor_path(spec.actor)}/runs"
    payload = spec.build_input(max_items)
    last_error: httpx.HTTPStatusError | None = None
    for attempt in range(_MAX_ATTEMPTS):
        response = client.post(url, json=payload)
        if response.is_success:
            return response.json()["data"]
        last_error = _http_error(response)
        if response.status_code not in _RETRYABLE_STATUS or attempt == _MAX_ATTEMPTS - 1:
            raise last_error
        time.sleep(5 * (attempt + 1))
    raise last_error if last_error else RuntimeError("unable to start actor run")


def _wait_for_run(client: httpx.Client, run_id: str) -> dict:
    deadline = time.monotonic() + settings.apify_run_timeout_seconds
    while time.monotonic() < deadline:
        response = client.get(f"{APIFY_BASE}/actor-runs/{run_id}")
        response.raise_for_status()
        data = response.json()["data"]
        if data.get("status") not in _ACTIVE_STATUSES:
            return data
        time.sleep(_POLL_INTERVAL_SECONDS)
    raise TimeoutError(f"Actor run {run_id} did not finish in {settings.apify_run_timeout_seconds}s")


def _dataset_items(client: httpx.Client, dataset_id: str) -> list[dict]:
    response = client.get(
        f"{APIFY_BASE}/datasets/{dataset_id}/items",
        params={"format": "json", "clean": "true"},
    )
    response.raise_for_status()
    payload = response.json()
    return payload if isinstance(payload, list) else []


def _fetch_source(spec: SourceSpec, max_items: int) -> tuple[SourceSpec, list[dict], dict]:
    """Run one actor to completion and return its raw dataset items."""
    with _client() as client:
        run = _start_run(client, spec, max_items)
        run = _wait_for_run(client, run["id"])
        status = run.get("status")
        meta = {
            "key": spec.key,
            "label": spec.label,
            "job_type": spec.job_type,
            "actor": spec.actor,
            "run_id": run.get("id"),
            "status": status,
            "console_url": f"https://console.apify.com/actors/runs/{run.get('id')}",
        }
        if status != "SUCCEEDED":
            message = run.get("statusMessage") or f"actor finished with status {status}"
            raise RuntimeError(message)
        items = _dataset_items(client, run["defaultDatasetId"])
        meta["fetched"] = len(items)
        return spec, items, meta


# --------------------------------------------------------------------------
# database side
# --------------------------------------------------------------------------


def _seed_sources() -> set[str]:
    from app.seed.extras import JOBS  # imported lazily: the seed module is heavy

    return {str(job.get("source", "")) for job in JOBS}


def _dedupe(candidates: list[dict]) -> list[dict]:
    """Drop exact duplicates produced by overlapping queries or sources."""
    seen: set[tuple[str, str, str]] = set()
    unique: list[dict] = []
    for row in candidates:
        title_key = _text(row["title"], 300).lower()
        key = (row["type"], title_key, row.get("company", "").lower())
        if key in seen:
            continue
        seen.add(key)
        unique.append(row)
    return unique


def _existing_by_key(db: Session, keys: set[str]) -> dict[str, Job]:
    if not keys:
        return {}
    rows = db.scalars(select(Job).where(Job.external_id.is_not(None))).all()
    return {f"{row.source}|{row.external_id}": row for row in rows if f"{row.source}|{row.external_id}" in keys}


def _safe_error(exc: BaseException) -> str:
    """Never let the API token reach an admin-facing error message."""
    message = str(exc) or exc.__class__.__name__
    if settings.apify_token:
        message = message.replace(settings.apify_token, "***")
    return message[:500]


def sync_jobs(db: Session, tracks: list[str] | None = None) -> dict:
    """Run the configured sources and merge their rows into the jobs table."""
    started_monotonic = time.monotonic()
    started_at = naive_utc_now()

    if not settings.apify_token:
        raise ValueError("APIFY_TOKEN is not configured - set it in .env to enable live job sync.")

    wanted = [track for track in ("government", "it") if not tracks or track in tracks]
    specs = [spec for spec in SOURCES if spec.job_type in wanted]

    per_run: list[dict] = []
    fetched: list[tuple[SourceSpec, list[dict]]] = []

    # Apify throttles concurrent paid runs on the FREE plan (HTTP 402), so keep the
    # pool small and let _start_run retry rather than firing everything at once.
    # The crawler now fans out over ~40 role queries, so the pool has to stay modest.
    max_workers = min(4, max(1, len(specs)))
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(_fetch_source, spec, settings.apify_max_items): spec for spec in specs
        }
        for future in as_completed(futures):
            spec = futures[future]
            try:
                _, items, meta = future.result()
            except Exception as exc:  # noqa: BLE001 - report every source failure to the admin
                per_run.append(
                    {
                        "key": spec.key,
                        "label": spec.label,
                        "job_type": spec.job_type,
                        "actor": spec.actor,
                        "ok": False,
                        "error": _safe_error(exc),
                    }
                )
            else:
                meta["ok"] = True
                per_run.append(meta)
                fetched.append((spec, items))

    candidates: list[dict] = []
    for spec, items in fetched:
        for item in items:
            if not isinstance(item, dict):
                continue
            row = spec.map_item(item)
            if row:
                candidates.append(row)

    candidates = _dedupe(candidates)
    stats = _persist_candidates(db, candidates, tuple(wanted))

    return {
        "ok": bool(candidates),
        "started_at": started_at.isoformat(),
        "duration_seconds": round(time.monotonic() - started_monotonic, 1),
        "sources": sorted(per_run, key=lambda item: (item["job_type"], item["key"])),
        **stats,
    }


def _persist_candidates(
    db: Session, candidates: list[dict], wanted: tuple[str, ...]
) -> dict:
    """Dedupe, upsert, purge seeds and retire expired rows. Shared by both syncs."""
    candidates = _dedupe(candidates)
    now = naive_utc_now()

    for row in candidates:
        row["synced_at"] = now

    keys = {f"{row['source']}|{row['external_id']}" for row in candidates}
    existing = _existing_by_key(db, keys)

    created = 0
    updated = 0
    for row in candidates:
        lookup = f"{row['source']}|{row['external_id']}"
        match = existing.get(lookup)
        if match is None:
            db.add(Job(**row))
            created += 1
        else:
            for field, value in row.items():
                if field == "external_id":
                    continue
                if value in (None, "") and getattr(match, field) not in (None, ""):
                    continue
                setattr(match, field, value)
            match.synced_at = now
            updated += 1

    purged = 0
    if candidates:
        # The board must show only real notifications once live data exists.
        purged = db.execute(
            delete(Job).where(Job.source.in_(_seed_sources()), Job.type.in_(wanted))
        ).rowcount or 0

    # Retire listings whose application window has closed. Rows are unpublished rather
    # than deleted so anyone who saved one keeps their application history.
    today = naive_utc_now().date()
    retired = db.execute(
        update(Job)
        .where(
            Job.external_id.is_not(None),
            Job.type.in_(wanted),
            Job.is_published.is_(True),
            Job.deadline.is_not(None),
            Job.deadline < today,
        )
        .values(is_published=False)
    ).rowcount or 0

    db.commit()

    total_in_db = (
        db.scalar(select(func.count(Job.id)).where(Job.type.in_(wanted))) or 0
    )

    return {
        "created": created,
        "updated": updated,
        "purged_seed_jobs": purged,
        "retired_expired": retired,
        "synced_total": len(candidates),
        "jobs_total": int(total_in_db),
    }


def sync_remote_jobs(db: Session) -> dict:
    """Crawl the remote boards: Apify remote queries plus the boards' own feeds."""
    started_monotonic = time.monotonic()
    started_at = naive_utc_now()

    if not settings.apify_token:
        raise ValueError("APIFY_TOKEN is not configured - set it in .env to enable live job sync.")

    per_run: list[dict] = []
    fetched: list[tuple[SourceSpec | FeedSpec, list[dict]]] = []

    # Same throttle discipline as the main sync: the FREE plan 402s on bursts.
    max_workers = min(4, max(1, len(REMOTE_SOURCES)))
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(_fetch_source, spec, settings.apify_max_items): spec
            for spec in REMOTE_SOURCES
        }
        for future in as_completed(futures):
            spec = futures[future]
            try:
                _, items, meta = future.result()
            except Exception as exc:  # noqa: BLE001 - report every source failure to the admin
                per_run.append(
                    {
                        "key": spec.key,
                        "label": spec.label,
                        "job_type": spec.job_type,
                        "actor": spec.actor,
                        "ok": False,
                        "error": _safe_error(exc),
                    }
                )
            else:
                meta["ok"] = True
                per_run.append(meta)
                fetched.append((spec, items))

    # Direct board feeds: public HTTP, no actor runs, seconds not minutes.
    with _public_client() as client:
        for feed in REMOTE_FEEDS:
            try:
                items = feed.fetch(client)
            except Exception as exc:  # noqa: BLE001 - one dead feed must not kill the sync
                per_run.append(
                    {
                        "key": feed.key,
                        "label": feed.label,
                        "job_type": "it",
                        "ok": False,
                        "error": _safe_error(exc),
                    }
                )
            else:
                per_run.append(
                    {
                        "key": feed.key,
                        "label": feed.label,
                        "job_type": "it",
                        "ok": True,
                        "fetched": len(items),
                    }
                )
                fetched.append((feed, items))

    candidates: list[dict] = []
    for spec, items in fetched:
        for item in items:
            if not isinstance(item, dict):
                continue
            row = spec.map_item(item)
            if row:
                candidates.append(row)

    stats = _persist_candidates(db, candidates, ("it",))

    return {
        "ok": bool(candidates),
        "started_at": started_at.isoformat(),
        "duration_seconds": round(time.monotonic() - started_monotonic, 1),
        "sources": sorted(per_run, key=lambda item: (item["job_type"], item["key"])),
        **stats,
    }


def sync_status(db: Session) -> dict:
    """Cheap snapshot of what is on the board right now, for the admin screen."""
    rows = db.execute(
        select(Job.source, Job.type, func.count(Job.id), func.max(Job.synced_at))
        .group_by(Job.source, Job.type)
        .order_by(Job.type, Job.source)
    ).all()

    by_source = [
        {
            "source": source or "manual",
            "job_type": job_type,
            "count": count,
            "last_synced_at": last_synced_at.isoformat() if last_synced_at else None,
        }
        for source, job_type, count, last_synced_at in rows
    ]

    seed_left = (
        db.scalar(select(func.count(Job.id)).where(Job.source.in_(_seed_sources()))) or 0
    )
    last_sync = db.scalar(select(func.max(Job.synced_at)).where(Job.external_id.is_not(None)))

    return {
        "token_configured": bool(settings.apify_token),
        "max_items_per_source": settings.apify_max_items,
        "run_timeout_seconds": settings.apify_run_timeout_seconds,
        "last_synced_at": last_sync.isoformat() if last_sync else None,
        "seed_jobs_remaining": seed_left,
        "sources": available_sources(),
        "by_source": by_source,
    }
