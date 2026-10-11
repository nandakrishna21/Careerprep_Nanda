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
    assert "access_token" not in body
    assert body["otp_sent"] is False  # dev mode: no SMTP, code returned below
    assert body["user_id"]
    dev_otp = body.get("dev_otp")
    assert dev_otp, "expected dev-mode OTP in register response"

    # Login is blocked until the email is verified.
    blocked = client.post("/api/auth/login", json={"email": email, "password": "Secret123"})
    assert blocked.status_code == 403

    verify = client.post("/api/auth/verify-otp", json={"email": email, "otp": dev_otp})
    assert verify.status_code == 200, verify.text
    verified = verify.json()
    assert verified["access_token"]
    assert verified["user"]["email"] == email
    assert verified["user"]["role"] == "student"

    headers = {"Authorization": f"Bearer {verified['access_token']}"}
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
    reg = client.post(
        "/api/auth/register",
        json={"full_name": "Reset", "email": email, "password": "Secret123"},
    )
    assert reg.status_code == 200
    verify = client.post(
        "/api/auth/verify-otp", json={"email": email, "otp": reg.json()["dev_otp"]}
    )
    assert verify.status_code == 200
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


def _register(client, email, name="OTP User"):
    res = client.post(
        "/api/auth/register",
        json={"full_name": name, "email": email, "password": "Secret123"},
    )
    assert res.status_code == 200, res.text
    return res.json()


def test_login_blocked_until_verified(client):
    email = "gated.user@example.com"
    _register(client, email)
    res = client.post("/api/auth/login", json={"email": email, "password": "Secret123"})
    assert res.status_code == 403
    assert "verify" in res.json()["detail"].lower()


def test_wrong_otp_rejected(client):
    email = "wrong.user@example.com"
    _register(client, email)
    res = client.post("/api/auth/verify-otp", json={"email": email, "otp": "000000"})
    assert res.status_code == 400
    assert "invalid code" in res.json()["detail"].lower()


def test_expired_otp_rejected(client, db):
    from datetime import timedelta

    from sqlalchemy import select

    from app.models import EmailOTP
    from app.services.common import naive_utc_now

    email = "expired.user@example.com"
    body = _register(client, email)
    row = db.scalar(select(EmailOTP).order_by(EmailOTP.id.desc()))
    assert row is not None
    row.expires_at = naive_utc_now() - timedelta(minutes=1)
    db.commit()
    res = client.post("/api/auth/verify-otp", json={"email": email, "otp": body["dev_otp"]})
    assert res.status_code == 400
    assert "expired" in res.json()["detail"].lower()


def test_otp_attempts_lockout(client):
    email = "locked.user@example.com"
    _register(client, email)
    for _ in range(5):
        res = client.post("/api/auth/verify-otp", json={"email": email, "otp": "000000"})
        assert res.status_code == 400
    res = client.post("/api/auth/verify-otp", json={"email": email, "otp": "000000"})
    assert res.status_code == 400
    assert "too many" in res.json()["detail"].lower()


def test_resend_cooldown_and_unknown_email(client):
    email = "resend.user@example.com"
    _register(client, email)
    res = client.post("/api/auth/resend-otp", json={"email": email})
    assert res.status_code == 429
    assert "wait" in res.json()["detail"].lower()

    res = client.post("/api/auth/resend-otp", json={"email": "nobody-here@example.com"})
    assert res.status_code == 200
    assert "dev_otp" not in res.json()


def test_verify_already_verified(client):
    email = "twice.user@example.com"
    body = _register(client, email)
    first = client.post("/api/auth/verify-otp", json={"email": email, "otp": body["dev_otp"]})
    assert first.status_code == 200
    second = client.post("/api/auth/verify-otp", json={"email": email, "otp": body["dev_otp"]})
    assert second.status_code == 400
    assert "already verified" in second.json()["detail"].lower()
