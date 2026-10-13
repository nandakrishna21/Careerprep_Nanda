"""Naukri / Glassdoor mappers and relative-date parsing (no network)."""

from datetime import timedelta

from app.services.common import naive_utc_now
from app.services.job_sync import _map_glassdoor, _map_naukri, _relative_date


def test_relative_date():
    today = naive_utc_now().date()
    assert _relative_date("6 Days Ago") == today - timedelta(days=6)
    assert _relative_date("30+ Days Ago") == today - timedelta(days=30)
    assert _relative_date("Just now") == today
    assert _relative_date("Today") == today
    assert _relative_date("Yesterday") == today - timedelta(days=1)
    assert _relative_date("nonsense") is None
    assert _relative_date(None) is None


def test_map_naukri():
    row = _map_naukri(
        {
            "jobId": "120826505033",
            "title": "Data Scientist/Software Developer",
            "company": "Xylem Water Solutions",
            "experience": "0-4 Yrs",
            "salary": "Not disclosed",
            "location": "Bengaluru",
            "skills": ["Python", "SQL"],
            "description": "Work on data platforms.",
            "postedLabel": "6 Days Ago",
            "createdDate": "2026-10-06T05:24:10.381Z",
            "url": "https://www.naukri.com/job-listings-x-120826505033",
        }
    )
    assert row is not None
    assert row["type"] == "it"
    assert row["source"] == "naukri"
    assert row["external_id"] == "120826505033"
    assert row["company"] == "Xylem Water Solutions"
    assert row["location"] == "Bengaluru"
    assert row["salary"] == ""
    assert str(row["posted_at"]) == "2026-10-06"


def test_map_naukri_falls_back_to_posted_label():
    row = _map_naukri(
        {
            "jobId": "1",
            "title": "Python Developer",
            "company": "Acme",
            "location": "Remote",
            "url": "https://www.naukri.com/job-listings-x-1",
            "postedLabel": "2 Days Ago",
        }
    )
    assert row is not None
    assert row["category"] == "remote"
    assert row["posted_at"] == naive_utc_now().date() - timedelta(days=2)


def test_map_naukri_rejects_empty():
    assert _map_naukri({"jobId": "1", "title": ""}) is None
    assert _map_naukri({"title": "Dev"}) is None


def test_map_glassdoor():
    row = _map_glassdoor(
        {
            "title": "Full Stack Developer",
            "posted_date": "2026-08-20",
            "location": {"raw": "Remote"},
            "is_remote": True,
            "description": "Build things.",
            "platform_url": "https://www.glassdoor.co.in/job-listing/j?jl=123",
            "official_url": "",
            "company_name": "Helm Ops",
            "salary_minimum": 135000,
            "salary_maximum": 145000,
            "salary_currency": "USD",
        }
    )
    assert row is not None
    assert row["type"] == "it"
    assert row["category"] == "remote"
    assert row["source"] == "glassdoor"
    assert row["location"] == "Remote"
    assert row["salary"] == "135,000 - 145,000 USD"
    assert str(row["posted_at"]) == "2026-08-20"


def test_map_glassdoor_rejects_empty():
    assert _map_glassdoor({"title": "Dev"}) is None
    assert _map_glassdoor({"platform_url": "https://x"}) is None


def test_hyderabad_inputs():
    from app.services.job_sync import (
        _HYDERABAD_ROLES,
        _glassdoor_input,
        _indeed_input,
        _linkedin_input,
        _naukri_hyderabad_input,
    )

    assert _HYDERABAD_ROLES == [
        "full stack developer",
        "backend developer",
        "machine learning engineer",
    ]
    linkedin = _linkedin_input("backend developer", cap=6, location="Hyderabad")(25)
    assert linkedin["location"] == "Hyderabad"
    assert linkedin["limitPerSource"] == 6
    assert _linkedin_input("x")(25)["location"] == "India"
    indeed = _indeed_input("backend developer", "Hyderabad", cap=8)(25)
    assert indeed["location"] == "Hyderabad"
    assert indeed["count"] == 8
    naukri = _naukri_hyderabad_input(25)
    assert len(naukri["startUrls"]) == 3
    assert all("hyderabad" in entry["url"] for entry in naukri["startUrls"])
    glassdoor = _glassdoor_input("backend developer", cap=10)(25)
    assert glassdoor["country"] == "India"
    assert glassdoor["max_results"] == 10
    assert "location" not in glassdoor  # city filter resolves nothing; facets cover it
