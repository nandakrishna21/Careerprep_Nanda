"""Experience-years parsing, capture, filtering and facets (no network)."""

from app.services.job_taxonomy import (
    classify_experience,
    experience_label,
    experience_options,
)


def test_classify_experience_ranges():
    assert classify_experience("Dev", None, "0-4 Yrs") == (0, 4)
    assert classify_experience("Dev", None, "3-5 Yrs") == (3, 5)
    assert classify_experience("Analyst", "Need 2 to 4 years experience") == (2, 4)
    assert classify_experience("Engineer", "Minimum 3+ years required") == (3, None)
    assert classify_experience("Developer", "5 years experience preferred") == (5, None)


def test_classify_experience_fresher_and_unknown():
    assert classify_experience("Fresher Software Engineer", None, None) == (0, 0)
    assert classify_experience("Python Intern", None, None) == (0, 0)
    assert classify_experience("Data Analyst - Freshers Welcome", "entry role", None) == (0, 0)
    assert classify_experience("Senior Manager", "Lead the team", None) == (None, None)
    assert classify_experience("Developer", "Great company", None) == (None, None)
    assert classify_experience(None, None, None) == (None, None)


def test_experience_label():
    assert experience_label(0, 0) == "Fresher"
    assert experience_label(2, 4) == "2-4 yrs"
    assert experience_label(3, None) == "3+ yrs"
    assert experience_label(5, 5) == "5 yrs"
    assert experience_label(None, None) == ""


def test_experience_options_counts_and_cap():
    options = experience_options([0, 0, 1, 2, 5, None])
    assert [o["value"] for o in options] == ["0", "1", "2", "3", "4", "5"]
    assert options[0] == {"value": "0", "label": "Fresher", "count": 2}
    assert options[2]["count"] == 4  # exp_min <= 2
    assert experience_options([None, None]) == []
    capped = experience_options([0, 25])
    assert capped[-1]["value"] == "10"


def test_naukri_mapper_captures_experience():
    from app.services.job_sync import _map_naukri

    row = _map_naukri(
        {
            "jobId": "9",
            "title": "Backend Developer",
            "company": "Acme",
            "experience": "2-5 Yrs",
            "location": "Pune",
            "url": "https://www.naukri.com/job-listings-x-9",
        }
    )
    assert row is not None
    assert (row["exp_min"], row["exp_max"]) == (2, 5)


def test_experience_filter_facets_and_label(client, db):
    from app.models import Job

    specs = [
        ("Exp Test Fresher", "fresher co", 0, 0),
        ("Exp Test Junior Dev", "junior co", 1, 2),
        ("Exp Test Senior Dev", "senior co", 6, None),
    ]
    for title, company, lo, hi in specs:
        if db.query(Job).filter(Job.title == title).first() is None:
            db.add(
                Job(
                    title=title,
                    company=company,
                    type="it",
                    category="fulltime",
                    description="Exp filter probe",
                    location="Remote",
                    salary="",
                    apply_link="https://example.com",
                    source="probe",
                    external_id=f"probe-{title}",
                    exp_min=lo,
                    exp_max=hi,
                )
            )
    db.commit()

    two = client.get("/api/jobs", params={"type": "it", "experience": 2}).json()
    titles = {item["title"] for item in two["items"]}
    assert "Exp Test Fresher" in titles
    assert "Exp Test Junior Dev" in titles
    assert "Exp Test Senior Dev" not in titles

    zero = client.get("/api/jobs", params={"type": "it", "experience": 0}).json()
    zero_titles = {item["title"] for item in zero["items"]}
    assert "Exp Test Fresher" in zero_titles
    assert "Exp Test Senior Dev" not in zero_titles
    assert "Exp Test Junior Dev" not in zero_titles

    facets = client.get("/api/jobs/facets").json()
    values = {o["value"] for o in facets["it"]["experience"]}
    assert "0" in values and "1" in values

    fresher = next(item for item in zero["items"] if item["title"] == "Exp Test Fresher")
    assert fresher["experience"] == "Fresher"


def test_posted_within_and_deadline_sort(client, db):
    from datetime import date, timedelta

    from app.models import Job

    today = date.today()
    specs = [
        ("Exp Test Old Open", today - timedelta(days=40), today + timedelta(days=60)),
        ("Exp Test Fresh Urgent", today - timedelta(days=2), today + timedelta(days=3)),
    ]
    for title, posted, deadline in specs:
        if db.query(Job).filter(Job.title == title).first() is None:
            db.add(
                Job(
                    title=title,
                    company="probe co",
                    type="it",
                    category="fulltime",
                    description="freshness probe",
                    location="Hyderabad",
                    salary="",
                    apply_link="https://example.com",
                    source="probe",
                    external_id=f"probe-{title}",
                    posted_at=posted,
                    deadline=deadline,
                )
            )
    db.commit()

    fresh = client.get("/api/jobs", params={"type": "it", "posted_within": 7}).json()
    fresh_titles = {item["title"] for item in fresh["items"]}
    assert "Exp Test Fresh Urgent" in fresh_titles
    assert "Exp Test Old Open" not in fresh_titles

    ordered = client.get("/api/jobs", params={"type": "it", "sort": "deadline"}).json()
    deadlines = [item["deadline"] for item in ordered["items"] if item["deadline"]]
    assert deadlines == sorted(deadlines)
