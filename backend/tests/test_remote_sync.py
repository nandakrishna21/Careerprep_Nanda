"""Remote-board mappers and endpoints. Pure unit tests plus API checks."""

from app.services.job_sync import (
    REMOTE_SITES,
    _map_nodesk,
    _map_remoteok,
    _map_remotive,
    _map_wwr,
    it_category,
)
from app.services.job_taxonomy import classify_role, role_label


def test_it_category_detects_remote_titles():
    assert it_category("Remote Python Developer", "", remote=False) == "remote"
    assert it_category("Senior Backend Engineer", "Full-time", remote=True) == "remote"
    assert it_category("Python Intern", "", remote=True) == "internship"


def test_design_bucket_catches_product_designers():
    assert classify_role("Lead Product Designer", "it") == "design-ui-ux"
    assert classify_role("Senior Level Designer", "it") == "design-ui-ux"
    assert classify_role("Senior Designer", "it") == "design-ui-ux"
    assert role_label("design-ui-ux") == "Design & UX"
    # UI/UX-titled roles stay frontend for consistency with earlier rows.
    assert classify_role("UX Designer", "it") == "frontend"


def test_engineer_variants_and_annotators():
    assert classify_role("Sr Solutions Architect", "it") == "software-engineer"
    assert classify_role("Member of Technical Staff Engineering", "it") == "software-engineer"
    assert classify_role("Video Data Annotator", "it") == "data-analytics"


def test_map_remoteok():
    row = _map_remoteok(
        {
            "id": "4242",
            "position": "Senior Backend Engineer",
            "company": "Acme",
            "location": "Worldwide",
            "date": "2026-10-01T10:00:00",
            "url": "https://remoteok.com/remote-jobs/4242",
            "salary_min": 80000,
            "salary_max": 120000,
            "description": "<p>Build APIs.</p>",
        }
    )
    assert row is not None
    assert row["type"] == "it"
    assert row["category"] == "remote"
    assert row["source"] == "remoteok"
    assert row["external_id"] == "4242"
    assert row["company"] == "Acme"
    assert row["location"] == "Worldwide"
    assert row["salary"] == "80,000 - 120,000"
    assert row["apply_link"] == "https://remoteok.com/remote-jobs/4242"
    assert row["description"] == "Build APIs."
    assert str(row["posted_at"]) == "2026-10-01"


def test_map_remoteok_rejects_empty():
    assert _map_remoteok({"id": "1", "position": ""}) is None
    assert _map_remoteok({"position": "Dev"}) is None


def test_map_remotive():
    row = _map_remotive(
        {
            "id": 2091045,
            "title": "Tier III Service Desk Engineer",
            "company_name": "Unio Digital",
            "job_type": "full_time",
            "candidate_required_location": "Worldwide",
            "url": "https://remotive.com/remote-jobs/x-2091045",
            "publication_date": "2026-10-07T01:11:09",
            "salary": "$60k - $80k",
            "description": "<p>Support.</p>",
        }
    )
    assert row is not None
    assert row["type"] == "it"
    assert row["category"] == "remote"
    assert row["source"] == "remotive"
    assert row["external_id"] == "2091045"
    assert row["location"] == "Worldwide"
    assert row["salary"] == "$60k - $80k"


def test_map_wwr_splits_company_and_location():
    row = _map_wwr(
        {
            "title": "Dremio: Software Engineer - Developer Experience",
            "link": "https://weworkremotely.com/remote-jobs/dremio-x",
            "guid": "https://weworkremotely.com/remote-jobs/dremio-x",
            "pubDate": "Mon, 28 Sep 2026 07:31:05 +0000",
            "description": "<p><strong>Headquarters:</strong> Portugal - Remote</p>",
        }
    )
    assert row is not None
    assert row["company"] == "Dremio"
    assert row["title"] == "Software Engineer - Developer Experience"
    assert row["type"] == "it"
    assert row["category"] == "remote"
    assert row["source"] == "weworkremotely"
    assert row["location"] == "Remote"
    assert str(row["posted_at"]) == "2026-09-28"


def test_map_wwr_without_company_prefix():
    row = _map_wwr(
        {
            "title": "Backend Engineer",
            "link": "https://weworkremotely.com/remote-jobs/x",
            "guid": "https://weworkremotely.com/remote-jobs/x",
            "pubDate": "not a date",
            "description": "",
        }
    )
    assert row is not None
    assert row["company"] == ""
    assert row["title"] == "Backend Engineer"
    assert row["location"] == "Remote"
    assert row["posted_at"] is None


def test_map_nodesk_splits_role():
    row = _map_nodesk(
        {
            "title": "Senior Designer at Acme",
            "link": "https://nodesk.co/remote-jobs/acme-x/",
            "guid": "https://nodesk.co/remote-jobs/acme-x/",
            "pubdate": "Thu, 08 Oct 2026 08:00:00 +0200",
            "description": "Design things.",
        }
    )
    assert row is not None
    assert row["company"] == "Acme"
    assert row["title"] == "Senior Designer"
    assert row["type"] == "it"
    assert row["category"] == "remote"
    assert row["source"] == "nodesk"
    assert str(row["posted_at"]) == "2026-10-08"


def test_remote_sites_directory_covers_every_board():
    assert len(REMOTE_SITES) == 11
    names = {site["name"] for site in REMOTE_SITES}
    for expected in (
        "We Work Remotely",
        "Remote.co",
        "FlexJobs",
        "RemoteOK",
        "Remotive",
        "Surely Remote",
        "LinkedIn",
        "Wellfound",
        "NoDesk",
        "Upwork",
        "Fiverr",
    ):
        assert expected in names
    for site in REMOTE_SITES:
        assert site["url"].startswith("https://")
        assert site["blurb"]
    live = {site["name"] for site in REMOTE_SITES if site["live"]}
    assert live == {"We Work Remotely", "RemoteOK", "Remotive", "NoDesk", "LinkedIn"}


def test_remote_tab_and_facets_and_sites(client, db):
    from sqlalchemy import select

    from app.models import Job

    if (
        db.scalar(select(Job).where(Job.title == "Remote Python Developer (Test)"))
        is None
    ):
        db.add(
            Job(
                title="Remote Python Developer (Test)",
                company="TestCorp",
                type="it",
                category="remote",
                description="Work from anywhere",
                location="Remote",
                salary="",
                apply_link="https://example.com/remote",
                source="remotive",
                external_id="test-remote-1",
            )
        )
        db.commit()

    body = client.get("/api/jobs?type=it&category=remote").json()
    assert body["total"] >= 1
    assert any(item["category"] == "remote" for item in body["items"])

    facets = client.get("/api/jobs/facets").json()
    assert "remote" in facets
    assert any(option["value"] == "backend" for option in facets["remote"]["roles"])

    sites = client.get("/api/jobs/remote-sites").json()
    assert len(sites["sites"]) == 11
