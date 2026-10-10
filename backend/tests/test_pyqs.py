"""PYQ bank coverage (2020-2026 papers) and the /pyqs year filter."""


def test_pyq_paper_specs_cover_every_exam_year():
    from app.seed import extras

    papers = [spec for spec in extras.PYQ_SPECS if "mix" in spec]
    assert len(papers) == 13 * 7
    pairs = {(spec["exam_slug"], spec["year"]) for spec in papers}
    assert len(pairs) == 13 * 7
    assert {year for _, year in pairs} == {2020, 2021, 2022, 2023, 2024, 2025, 2026}
    slugs = [spec["slug"] for spec in extras.PYQ_SPECS]
    assert len(set(slugs)) == len(slugs)
    for spec in papers:
        assert spec["count"] == 15
        assert sum(count for _, _, count in spec["mix"]) == 15


def test_pyq_mix_build_produces_tagged_questions():
    from app.seed import extras

    spec = next(s for s in extras.PYQ_SPECS if s["slug"] == "pyq-ssc-gd-2025")
    questions = extras.build_pyq_questions(spec)
    assert len(questions) == 15
    assert all(question["tags"] for question in questions)
    for question in questions:
        assert len(question["options"]) == 4
        assert 0 <= question["correct_index"] < 4


def test_pyqs_year_filter(client, db):
    from sqlalchemy import select

    from app.models import Exam, Quiz

    exam = db.scalar(select(Exam).where(Exam.slug == "ssc-cgl"))
    if exam is None:
        exam = Exam(name="SSC CGL", slug="ssc-cgl", category="ssc", description="Test exam")
        db.add(exam)
        db.flush()

    for slug, year in (("test-pyq-2021", 2021), ("test-pyq-2025", 2025)):
        if db.scalar(select(Quiz).where(Quiz.slug == slug)) is None:
            db.add(
                Quiz(
                    title=f"Test PYQ {year}",
                    slug=slug,
                    quiz_type="pyq",
                    difficulty="intermediate",
                    duration_minutes=20,
                    total_questions=0,
                    negative_marks=0.25,
                    is_published=True,
                    exam_id=exam.id,
                    meta={"year": year, "exam": "ssc-cgl"},
                )
            )
    db.commit()

    body_2025 = client.get("/api/pyqs?year=2025").json()
    assert body_2025, "expected seeded 2025 papers plus the test row"
    assert all(item["meta"].get("year") == 2025 for item in body_2025)

    body_2021 = client.get("/api/pyqs?year=2021").json()
    assert any(item["slug"] == "test-pyq-2021" for item in body_2021)
    assert all(item["meta"].get("year") == 2021 for item in body_2021)

    combined = client.get("/api/pyqs?exam=ssc-cgl&year=2025").json()
    assert combined, "expected SSC CGL 2025 papers"
    assert all(item["meta"].get("year") == 2025 for item in combined)
