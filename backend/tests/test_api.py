from app.core.config import settings


def _admin_headers(client):
    res = client.post(
        "/api/auth/login",
        json={"email": settings.admin_email, "password": settings.admin_password},
    )
    assert res.status_code == 200, res.text
    return {"Authorization": f"Bearer {res.json()['access_token']}"}


def test_student_forbidden_from_admin(client, auth_headers):
    res = client.get("/api/admin/users", headers=auth_headers)
    assert res.status_code == 403


def test_admin_users_listing(client):
    res = client.get("/api/admin/users", headers=_admin_headers(client))
    assert res.status_code == 200
    body = res.json()
    assert body["total"] >= 1
    assert any(u["role"] == "admin" for u in body["items"])


def test_admin_analytics(client):
    res = client.get("/api/admin/analytics", headers=_admin_headers(client))
    assert res.status_code == 200
    body = res.json()
    assert body["users_total"] >= 1
    assert "signups_by_day" in body
    assert "top_quizzes" in body


def test_jobs_listing_search_and_save(client, db, auth_headers):
    res = client.get("/api/jobs")
    assert res.status_code == 200
    body = res.json()
    assert body["total"] >= 1
    assert {"id", "title", "type", "category"} <= set(body["items"][0])

    filtered = client.get("/api/jobs?type=government").json()
    assert filtered["items"]
    assert all(j["type"] == "government" for j in filtered["items"])

    search = client.get("/api/jobs?q=python").json()
    assert search["total"] >= 0

    job_id = body["items"][0]["id"]
    save = client.post(f"/api/jobs/{job_id}/save", headers=auth_headers)
    assert save.status_code == 200

    saved = client.get("/api/jobs/saved", headers=auth_headers)
    assert saved.status_code == 200
    assert any(j["id"] == job_id for j in saved.json()["items"])

    patch = client.patch(
        f"/api/jobs/{job_id}/save", json={"status": "applied"}, headers=auth_headers
    )
    assert patch.status_code == 200

    unsaved = client.delete(f"/api/jobs/{job_id}/save", headers=auth_headers)
    assert unsaved.status_code == 200


def test_leaderboard_weekly(client, auth_headers):
    res = client.get("/api/leaderboard?period=weekly", headers=auth_headers)
    assert res.status_code == 200
    entries = res.json()
    assert isinstance(entries, list)
    if entries:
        assert entries[0]["rank"] == 1
        assert "xp" in entries[0]


def test_search_groups(client):
    res = client.get("/api/search?q=percentage")
    assert res.status_code == 200
    body = res.json()
    for key in ("courses", "topics", "lessons", "quizzes", "mock_tests", "jobs", "current_affairs"):
        assert key in body


def test_progress_dashboard_and_study_session(client, auth_headers):
    res = client.get("/api/progress/dashboard", headers=auth_headers)
    assert res.status_code == 200
    body = res.json()
    for key in (
        "total_study_hours",
        "total_quizzes",
        "average_score",
        "strong_topics",
        "weak_topics",
        "streak_days",
        "xp",
        "level",
        "mock_tests_taken",
        "badges_unlocked",
        "daily_activity",
        "performance_trend",
        "mock_performance",
    ):
        assert key in body

    session = client.post(
        "/api/progress/study-session",
        json={"minutes": 45, "activity_type": "study"},
        headers=auth_headers,
    )
    assert session.status_code == 200
    assert session.json()["streak_days"] >= 1


def test_achievements_list(client, auth_headers):
    res = client.get("/api/achievements", headers=auth_headers)
    assert res.status_code == 200
    rows = res.json()
    assert len(rows) >= 8
    assert {"code", "title", "unlocked"} <= set(rows[0])


def test_notifications_endpoints(client, auth_headers):
    res = client.get("/api/notifications", headers=auth_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    read = client.post("/api/notifications/read", json={}, headers=auth_headers)
    assert read.status_code == 200


def test_admin_course_crud(client):
    headers = _admin_headers(client)
    created = client.post(
        "/api/admin/courses",
        json={
            "title": "Test Subject",
            "slug": "test-subject",
            "category": "government",
            "description": "Temp",
            "icon": "book",
            "level": "Beginner",
            "order": 99,
            "career_path": False,
            "is_published": False,
        },
        headers=headers,
    )
    assert created.status_code in (200, 201), created.text
    course_id = created.json()["id"]

    updated = client.put(
        f"/api/admin/courses/{course_id}",
        json={"description": "Updated"},
        headers=headers,
    )
    assert updated.status_code == 200

    deleted = client.delete(f"/api/admin/courses/{course_id}", headers=headers)
    assert deleted.status_code == 200
