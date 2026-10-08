"""Role and location normalisation for the jobs board.

Two filterable dimensions are derived from every listing so the UI can offer a
"developer roles / job roles" filter and a location filter that always line up with
data that actually exists:

``role``
    A stable slug such as ``frontend`` or ``teaching``. IT listings are classified
    by developer discipline, government listings by sector, because those are the
    two questions a job seeker is really asking.
``city``
    A cleaned place name, so dozens of raw LinkedIn/Indeed strings collapse into a
    handful of sensible options (``"Bengaluru, Karnataka, India"`` and
    ``"Bengaluru East, Karnataka, India"`` both become ``Bengaluru``).

Both values are derived automatically on insert/update through SQLAlchemy events,
so no caller has to remember to set them.
"""

from __future__ import annotations

import re
from typing import Iterable

from sqlalchemy import inspect, text

OTHER = "other"

# --------------------------------------------------------------------------
# IT roles
# --------------------------------------------------------------------------

# Order matters: the first rule that matches wins, so the most specific
# disciplines are checked before the catch-all "software engineer".
_IT_RULES: list[tuple[str, tuple[str, ...]]] = [
    (
        "fullstack",
        (
            r"\bfull[\s\-]?stack\b",
            r"\bmern\b",
            r"\bmean[\s\-]?stack\b",
            r"\bmevn\b",
            r"\bstack[\s\-]?developer\b",
        ),
    ),
    (
        "frontend",
        (
            r"\bfront[\s\-]?end\b",
            r"\breact\b",
            r"\bangular\b",
            r"\bvue\b",
            r"\bnext\.?js\b",
            r"\bsvelte\b",
            r"\bjavascript\b",
            r"\btypescript\b",
            r"\bhtml\b",
            r"\bcss\b",
            r"\bui/ux\b",
            r"\bui\b",
            r"\bux\b",
            r"\bweb design",
        ),
    ),
    (
        "backend",
        (
            r"\bback[\s\-]?end\b",
            r"\bapi\b",
            r"\bnode\.?js\b",
            r"\bnodejs\b",
            r"\bdjango\b",
            r"\bfastapi\b",
            r"\bspring\b",
            r"\blaravel\b",
            r"\bexpress\b",
            r"\brails\b",
            r"\bgolang\b",
            r"\bgo developer\b",
            r"\bpython\b",
            r"\bjava\b",
            r"\bc#",
            r"\bcsharp\b",
            r"\.net\b",
            r"\bphp\b",
            r"\bruby\b",
            r"\bscala\b",
        ),
    ),
    (
        "mobile",
        (
            r"\bandroid\b",
            r"\bflutter\b",
            r"\bios\b",
            r"\bswift\b",
            r"\bkotlin\b",
            r"\bmobile\b",
        ),
    ),
    (
        "devops-cloud",
        (
            r"\bdevops\b",
            r"\bsre\b",
            r"\bsite reliability\b",
            r"\bcloud\b",
            r"\baws\b",
            r"\bazure\b",
            r"\bgcp\b",
            r"\bkubernetes\b",
            r"\bdocker\b",
            r"\bterraform\b",
            r"\bplatform engineer\b",
            r"\bsystem admin",
            r"\bsysadmin\b",
            r"\bci/?cd\b",
            r"\brelease engineer\b",
        ),
    ),
    (
        "data-science-ai",
        (
            r"\bdata scientist\b",
            r"\bmachine learning\b",
            r"\bmlops\b",
            r"\bml engineer\b",
            r"\bartificial intelligence\b",
            r"\bai\b",
            r"\bgenai\b",
            r"\bllm\b",
            r"\bagentic\b",
            r"\bdeep learning\b",
            r"\bnlp\b",
            r"\bcomputer vision\b",
            r"\bprompt engineer\b",
        ),
    ),
    (
        "data-analytics",
        (
            r"\bdata analyst\b",
            r"\bdata analytics\b",
            r"\bdata engineer\b",
            r"\bbusiness intelligence\b",
            r"\betl\b",
            r"\btableau\b",
            r"\bpower bi\b",
            r"\banalytics\b",
            r"\bdata visualization\b",
        ),
    ),
    (
        "qa-testing",
        (
            r"\bqa\b",
            r"\bquality assurance\b",
            r"\btest engineer\b",
            r"\bsdet\b",
            r"\bautomation tester\b",
            r"\bsoftware test",
            r"\bmanual test",
        ),
    ),
    ("cyber-security", (r"\bsecurity\b", r"\bcyber\b", r"\binfosec\b", r"\bsoc analyst\b")),
    ("database", (r"\bdba\b", r"\bdatabase\b", r"\bsql server\b")),
    (
        "software-engineer",
        (
            r"\bsoftware engineer\b",
            r"\bsoftware developer\b",
            r"\btech lead\b",
            r"\btechnical lead\b",
            r"\blead engineer\b",
            r"\bsde\b",
            r"\bprogrammer\b",
            r"\bdeveloper\b",
            r"\bengineer\b",
        ),
    ),
]

# --------------------------------------------------------------------------
# Government roles
# --------------------------------------------------------------------------

_GOV_RULES: list[tuple[str, tuple[str, ...]]] = [
    (
        "health-medical",
        (
            r"\bmedical\b",
            r"\bdoctor\b",
            r"\bnurse\b",
            r"\bnursing\b",
            r"\bhospital\b",
            r"\baiims\b",
            r"\bnorcet\b",
            r"\bphysiotherapist\b",
            r"\bveterinar",
            r"\bdentist\b",
            r"\bdental\b",
            r"\bpharmac",
            r"\bclinic",
            r"\bhealth\b",
            r"\bsurgeon\b",
            r"\btherapist\b",
            r"\bcounsellor wellness\b",
        ),
    ),
    (
        "banking",
        (
            r"\bbank",
            r"\bbanking\b",
            r"\bibps\b",
            r"\bsbi\b",
            r"\brbi\b",
            r"\biob\b",
            r"\bboi\b",
            r"\bcredit analyst\b",
            r"\btrade finance\b",
            r"\bwealth\b",
            r"\bfinancial\b",
            r"\bmutual fund\b",
        ),
    ),
    (
        "railway",
        (
            r"\brailway\b",
            r"\brailways\b",
            r"\brrb\b",
            r"\brrc\b",
            r"\bntpc\b",
            r"\bstation master\b",
            r"\bticket collector\b",
            r"\bloco pilot\b",
            r"\brail\b",
        ),
    ),
    (
        "defence-police",
        (
            r"\bpolice\b",
            r"\bconstable\b",
            r"\bhavildar\b",
            r"\bsub[\s\-]?inspector\b",
            r"\bitbp\b",
            r"\bcrpf\b",
            r"\bbsf\b",
            r"\bassam rifles\b",
            r"\bcoast guard\b",
            r"\barmy\b",
            r"\bnavy\b",
            r"\bair force\b",
            r"\bdefence\b",
            r"\bdefense\b",
            r"\bmilitary\b",
            r"\bparamilitary\b",
            r"\bsecurity guard\b",
            r"\bfireman\b",
            r"\bjail\b",
            r"\bwarden\b",
        ),
    ),
    (
        "teaching",
        (
            r"\bteacher\b",
            r"\bteaching\b",
            r"\btet\b",
            r"\bprofessor\b",
            r"\bfaculty\b",
            r"\blecturer\b",
            r"\bpgt\b",
            r"\btgt\b",
            r"\bprimary teacher\b",
            r"\bschool\b",
            r"\bprincipal\b",
            r"\beducator\b",
            r"\binstructor\b",
            r"\btutor\b",
            r"\blibrarian\b",
            r"\blibrary\b",
            r"\bacademic\b",
        ),
    ),
    (
        "apprenticeship",
        (
            r"\bapprentice",
            r"\binternship\b",
            r"\bintern\b",
            r"\btrainee\b",
            r"\btraining\b",
        ),
    ),
    (
        "engineering-technical",
        (
            r"\bengineer",
            r"\bengineering\b",
            r"\btechnician\b",
            r"\btechnical\b",
            r"\blaboratory\b",
            r"\blab assistant\b",
            r"\belectrical\b",
            r"\bcivil\b",
            r"\bmechanical\b",
            r"\btrade\b",
            r"\boperator\b",
            r"\bdraftsman\b",
        ),
    ),
    (
        "management",
        (
            r"\bofficer\b",
            r"\bmanager\b",
            r"\bexecutive\b",
            r"\bconsultant\b",
            r"\bspecialist\b",
            r"\bsecretary\b",
            r"\bhead\b",
            r"\bdirector\b",
            r"\bsupervisor\b",
            r"\badvisor\b",
            r"\badviser\b",
            r"\bcounselor\b",
            r"\bcounsellor\b",
        ),
    ),
    (
        "clerical",
        (
            r"\bclerk",
            r"\bclerical\b",
            r"\bsteno",
            r"\btypist\b",
            r"\bdata entry\b",
            r"\bjudicial assistant\b",
            r"\bcourt attendant\b",
            r"\bcourt assistant\b",
            r"\bdriver\b",
            r"\bchauffeur\b",
            r"\bassistant\b",
            r"\bldc\b",
            r"\budc\b",
            r"\blower division\b",
        ),
    ),
    (
        "public-services",
        (
            r"\bssc\b",
            r"\bupsc\b",
            r"\bpsc\b",
            r"\bdsssb\b",
            r"\bbpsc\b",
            r"\bbpssc\b",
            r"\bupsssc\b",
            r"\buppsc\b",
            r"\bjssc\b",
            r"\bappsc\b",
            r"\bcivil services\b",
            r"\bgroup[\s\-]?1\b",
            r"\bgroup[\s\-]?i\b",
            r"\bcourt\b",
            r"\bvidhan parishad\b",
            r"\bjudicial\b",
            r"\bhigh court\b",
            r"\bsupreme court\b",
            r"\banganwadi\b",
            r"\bsafai\b",
            r"\bmunicipal\b",
            r"\bstaff\b",
            r"\bpanchayat\b",
            r"\brecruitment\b",
        ),
    ),
]

ROLE_LABELS: dict[str, str] = {
    # IT
    "fullstack": "Full Stack",
    "frontend": "Frontend",
    "backend": "Backend",
    "mobile": "Mobile / Android",
    "devops-cloud": "DevOps & Cloud",
    "data-science-ai": "Data Science & AI",
    "data-analytics": "Data & Analytics",
    "qa-testing": "QA & Testing",
    "cyber-security": "Cyber Security",
    "database": "Database / DBA",
    "software-engineer": "Software Engineering",
    # Government
    "health-medical": "Health & Medical",
    "banking": "Banking & Finance",
    "railway": "Railway",
    "defence-police": "Defence, Police & Security",
    "teaching": "Teaching & Education",
    "apprenticeship": "Apprenticeship & Internship",
    "engineering-technical": "Engineering & Technical",
    "clerical": "Clerical & Support",
    "public-services": "Public Services & Courts",
    "management": "Management & Officers",
    OTHER: "Other",
}

_COMPILED: dict[str, list[tuple[str, list[re.Pattern[str]]]]] = {
    "it": [(slug, [re.compile(p) for p in patterns]) for slug, patterns in _IT_RULES],
    "government": [(slug, [re.compile(p) for p in patterns]) for slug, patterns in _GOV_RULES],
}


def _first_match(rules: list[tuple[str, list[re.Pattern[str]]]], title: str) -> str:
    haystack = (title or "").lower()
    for slug, patterns in rules:
        for pattern in patterns:
            if pattern.search(haystack):
                return slug
    return OTHER


def classify_role(title: str, job_type: str) -> str:
    """Return a stable role slug for a listing."""
    bucket = "government" if job_type == "government" else "it"
    return _first_match(_COMPILED[bucket], title)


def role_label(slug: str | None) -> str:
    if not slug:
        return ROLE_LABELS[OTHER]
    return ROLE_LABELS.get(slug, slug.replace("-", " ").title())


# --------------------------------------------------------------------------
# Location normalisation
# --------------------------------------------------------------------------

_CITY_ALIASES: dict[str, str] = {
    "bangalore": "Bengaluru",
    "bengalore": "Bengaluru",
    "bengaluru": "Bengaluru",
    "gurgaon": "Gurugram",
    "gurugram": "Gurugram",
    "bombay": "Mumbai",
    "mumbai": "Mumbai",
    "navi mumbai": "Mumbai",
    "greater mumbai": "Mumbai",
    "new delhi": "Delhi",
    "delhi": "Delhi",
    "calcutta": "Kolkata",
    "kolkata": "Kolkata",
    "greater kolkata": "Kolkata",
    "hyderabad": "Hyderabad",
    "greater hyderabad": "Hyderabad",
    "madras": "Chennai",
    "chennai": "Chennai",
    "greater chennai": "Chennai",
    "pune": "Pune",
    "greater pune": "Pune",
    "ahmedabad": "Ahmedabad",
    "greater ahmedabad": "Ahmedabad",
    "trivandrum": "Thiruvananthapuram",
    "trivendrum": "Thiruvananthapuram",
    "thiruvananthapuram": "Thiruvananthapuram",
    "cochin": "Kochi",
    "kochi": "Kochi",
    "noida": "Noida",
    "greater noida": "Noida",
    "faridabad": "Faridabad",
    "jaipur": "Jaipur",
    "lucknow": "Lucknow",
    "surat": "Surat",
    "indore": "Indore",
    "bhopal": "Bhopal",
    "chandigarh": "Chandigarh",
    "mohali": "Mohali",
    "kozhikode": "Kozhikode",
    "kottayam": "Kottayam",
    "coimbatore": "Coimbatore",
    "mysuru": "Mysuru",
    "mysore": "Mysuru",
    "visakhapatnam": "Visakhapatnam",
    "vizag": "Visakhapatnam",
    "nagpur": "Nagpur",
    "vadodara": "Vadodara",
    "rajkot": "Rajkot",
    "patna": "Patna",
    "ranchi": "Ranchi",
    "bhubaneswar": "Bhubaneswar",
    "guwahati": "Guwahati",
}

_STATES = {
    "andhra pradesh",
    "arunachal pradesh",
    "assam",
    "bihar",
    "chhattisgarh",
    "goa",
    "gujarat",
    "haryana",
    "himachal pradesh",
    "jammu and kashmir",
    "jharkhand",
    "karnataka",
    "kerala",
    "madhya pradesh",
    "maharashtra",
    "manipur",
    "meghalaya",
    "mizoram",
    "nagaland",
    "odisha",
    "punjab",
    "rajasthan",
    "sikkim",
    "tamil nadu",
    "telangana",
    "tripura",
    "uttar pradesh",
    "uttarakhand",
    "west bengal",
    "puducherry",
    "chandigarh",
    "delhi",
}

# Trailing words that describe an area rather than name a place.
_AREA_SUFFIXES = {
    "region",
    "metropolitan",
    "division",
    "district",
    "urban",
    "city",
    "area",
    "belt",
    "zone",
    "east",
    "west",
    "north",
    "south",
    "central",
}


def _clean_segment(segment: str) -> str:
    segment = segment.strip().strip("-/")
    # "Pune/Pimpri-Chinchwad" is one place as far as a filter is concerned.
    if "/" in segment:
        segment = segment.split("/")[0].strip()
    words = segment.split()
    while len(words) > 1 and words[-1].lower().strip(".,") in _AREA_SUFFIXES:
        words.pop()
    return " ".join(words).strip(" .,")


def normalize_city(raw: str) -> str:
    """Collapse a raw location string into a filter-friendly place name."""
    value = (raw or "").strip()
    if not value or len(value) > 100 or "|" in value:
        return OTHER
    if sum(ch.isdigit() for ch in value) > 10:
        return OTHER

    lowered = value.lower()
    if "remote" in lowered or "work from home" in lowered:
        return "Remote"
    if "all india" in lowered or "across india" in lowered or "pan india" in lowered:
        return "All India"
    if "examination centre" in lowered or "examination center" in lowered:
        return "All India"

    segments = [cleaned for cleaned in (_clean_segment(p) for p in value.split(",")) if cleaned]
    if not segments:
        return OTHER

    # Prefer a recognised city even when it is not the first segment, so
    # "Bandra West, Mumbai, Maharashtra" resolves to Mumbai.
    for segment in segments:
        alias = _CITY_ALIASES.get(segment.lower())
        if alias:
            return alias
    for segment in segments:
        if segment.lower() in _STATES:
            return segment

    first = segments[0]
    return first if len(first) <= 40 else OTHER


def classify_job(title: str, job_type: str, location: str) -> tuple[str, str]:
    """Return ``(role, city)`` for a listing."""
    return classify_role(title, job_type), normalize_city(location)


# --------------------------------------------------------------------------
# Schema upkeep (the project has no alembic history yet)
# --------------------------------------------------------------------------

_JOB_COLUMNS = {"role": "VARCHAR(64)", "city": "VARCHAR(120)"}


def ensure_job_columns(engine) -> None:
    """Add the filter columns to an existing ``jobs`` table if they are missing."""
    inspector = inspect(engine)
    if "jobs" not in inspector.get_table_names():
        return

    existing = {column["name"] for column in inspector.get_columns("jobs")}
    with engine.begin() as conn:
        for name, ddl_type in _JOB_COLUMNS.items():
            if name not in existing:
                conn.execute(text(f"ALTER TABLE jobs ADD COLUMN {name} {ddl_type}"))
        for name in _JOB_COLUMNS:
            conn.execute(text(f"CREATE INDEX IF NOT EXISTS ix_jobs_{name} ON jobs ({name})"))


def backfill_jobs(engine) -> int:
    """Derive ``role``/``city`` for rows written before these columns existed."""
    from sqlalchemy import or_, select
    from sqlalchemy.orm import sessionmaker

    from app.models import Job

    ensure_job_columns(engine)

    db = sessionmaker(bind=engine)()
    try:
        rows = db.scalars(
            select(Job).where(or_(Job.role.is_(None), Job.city.is_(None)))
        ).all()
        for row in rows:
            row.role, row.city = classify_job(row.title, row.type, row.location)
        db.commit()
        return len(rows)
    finally:
        db.close()


def roles_with_counts(values: Iterable[str]) -> list[dict]:
    """Role slugs -> filter options sorted by popularity."""
    counts: dict[str, int] = {}
    for value in values:
        slug = value or OTHER
        counts[slug] = counts.get(slug, 0) + 1
    return [
        {"value": slug, "label": role_label(slug), "count": count}
        for slug, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def locations_with_counts(values: Iterable[str]) -> list[dict]:
    """City slugs -> filter options sorted by popularity."""
    counts: dict[str, int] = {}
    for value in values:
        slug = value or OTHER
        counts[slug] = counts.get(slug, 0) + 1
    return [
        {"value": slug, "label": slug, "count": count}
        for slug, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]
