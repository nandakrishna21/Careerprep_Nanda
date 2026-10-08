from app.core.config import settings


def test_health(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_register_me_login_flow(client):
    email = "flow.user@example.com"
    res = client.post(
        "/api/auth/register",
        json={"full_name": "Flow User", "email": email, "password": "Secret123"},
    )
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["access_token"]
    assert body["user"]["email"] == email
    assert body["user"]["role"] == "student"

    headers = {"Authorization": f"Bearer {body['access_token']}"}
    me = client.get("/api/auth/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["user"]["email"] == email
    assert "profile" in me.json()

    login = client.post("/api/auth/login", json={"email": email, "password": "Secret123"})
    assert login.status_code == 200
    assert login.json()["access_token"]


def test_duplicate_email_conflict(client):
    email = "dup.user@example.com"
    payload = {"full_name": "Dup", "email": email, "password": "Secret123"}
    assert client.post("/api/auth/register", json=payload).status_code == 200
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 409


def test_wrong_password_and_me_unauthorized(client):
    client.post(
        "/api/auth/register",
        json={"full_name": "WP", "email": "wp.user@example.com", "password": "Secret123"},
    )
    res = client.post("/api/auth/login", json={"email": "wp.user@example.com", "password": "Nope12345"})
    assert res.status_code == 401
    assert client.get("/api/auth/me").status_code == 401


def test_short_password_rejected(client):
    res = client.post(
        "/api/auth/register",
        json={"full_name": "Short", "email": "short@example.com", "password": "abc"},
    )
    assert res.status_code == 422


def test_forgot_and_reset_password(client):
    email = "reset.user@example.com"
    client.post(
        "/api/auth/register",
        json={"full_name": "Reset", "email": email, "password": "Secret123"},
    )
    res = client.post("/api/auth/forgot-password", json={"email": email})
    assert res.status_code == 200
    token = res.json().get("reset_token")
    assert token, "expected dev-mode reset_token in response"

    reset = client.post(
        "/api/auth/reset-password",
        json={"token": token, "password": "NewSecret456"},
    )
    assert reset.status_code == 200

    assert client.post("/api/auth/login", json={"email": email, "password": "Secret123"}).status_code == 401
    assert (
        client.post("/api/auth/login", json={"email": email, "password": "NewSecret456"}).status_code == 200
    )


def test_logout_message(client):
    res = client.post("/api/auth/logout")
    assert res.status_code == 200
    assert "message" in res.json()


def test_admin_seeded_from_settings(client):
    res = client.post(
        "/api/auth/login",
        json={"email": settings.admin_email, "password": settings.admin_password},
    )
    assert res.status_code == 200
    assert res.json()["user"]["role"] == "admin"
