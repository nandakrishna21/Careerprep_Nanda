"""My Jobs List: private applied-jobs tracker with syllabus + strategy."""

# NOTE: use the session fixtures (owner_headers = superadmin, auth_headers =
# regular user). Creating extra users mid-session re-imports conftest and hits
# the Windows test.db lock, so we reuse these two identities.


def test_templates_list_has_two_roles(client, auth_headers):
    body = client.get("/api/my-jobs/templates", headers=auth_headers).json()
    keys = {item["template_key"] for item in body["items"]}
    assert {"uiicl-ao-scale1", "upsc-epfo-apfc"} <= keys


def test_create_from_template_seeds_syllabus_strategy(client, owner_headers):
    # superadmin adds both applied roles
    for key in ("uiicl-ao-scale1", "upsc-epfo-apfc"):
        res = client.post(f"/api/my-jobs/from-template/{key}", headers=owner_headers)
        assert res.status_code == 201, res.text
        body = res.json()
        assert body["template_key"] == key
        assert len(body["syllabus"]) >= 5
        assert len(body["exam_pattern"]) >= 2
        assert len(body["strategy"]) > 200
        assert len(body["preparation_plan"]) >= 3
    listing = client.get("/api/my-jobs", headers=owner_headers).json()
    assert listing["total"] >= 2
    # idempotent re-add returns existing, no duplicates
    before = listing["total"]
    again = client.post("/api/my-jobs/from-template/uiicl-ao-scale1", headers=owner_headers)
    assert again.status_code == 201
    assert client.get("/api/my-jobs", headers=owner_headers).json()["total"] == before


def test_crud_is_private_per_user(client, auth_headers, owner_headers):
    created = client.post(
        "/api/my-jobs",
        json={"title": "Custom Applied Role", "organization": "Test Org", "status": "preparing"},
        headers=auth_headers,
    )
    assert created.status_code == 201, created.text
    my_id = created.json()["id"]

    # superadmin (different user) cannot see or touch it
    other = client.get(f"/api/my-jobs/{my_id}", headers=owner_headers)
    assert other.status_code == 404

    updated = client.put(f"/api/my-jobs/{my_id}", json={"status": "interview", "notes": "Mock done"}, headers=auth_headers)
    assert updated.status_code == 200
    assert updated.json()["status"] == "interview"

    assert client.get("/api/my-jobs?status=interview", headers=auth_headers).json()["total"] >= 1

    deleted = client.delete(f"/api/my-jobs/{my_id}", headers=auth_headers)
    assert deleted.status_code == 200
    assert client.get(f"/api/my-jobs/{my_id}", headers=auth_headers).status_code == 404


def test_requires_auth(client):
    assert client.get("/api/my-jobs").status_code == 401
    assert client.get("/api/my-jobs/templates").status_code == 401
