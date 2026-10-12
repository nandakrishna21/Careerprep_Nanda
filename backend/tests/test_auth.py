from app.core.config import settings
from conftest import _owner_headers, approve_user


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
    assert body["approved"] is False
    assert body["user_id"]
    assert "Account created" in body.get("message", "")

    # Login stays blocked until the super admin approves.
    pending = client.post("/api/auth/login", json={"email": email, "password": "Secret123"})
    assert pending.status_code == 403
    assert "pending approval" in pending.json()["detail"].lower()

    # Superadmin accepts -> login works.
    owner = _owner_headers(client)
    approve_user(client, owner, body["user_id"])

    login = client.post("/api/auth/login", json={"email": email, "password": "Secret123"})
    assert login.status_code == 200
    assert login.json()["access_token"]

    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    me = client.get("/api/auth/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["user"]["email"] == email
    assert "profile" in me.json()


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
    from conftest import signup_approve_login

    email = "reset.user@example.com"
    signup_approve_login(client, email, "Reset")
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


def test_admin_cannot_approve_accounts(client):
    from conftest import signup_approve_login

    email = "approve.gated@example.com"
    owner = _owner_headers(client)
    reg = client.post(
        "/api/auth/register",
        json={"full_name": "Gated", "email": email, "password": "Secret123"},
    )
    assert reg.status_code == 200
    user_id = reg.json()["user_id"]

    admin_login = client.post(
        "/api/auth/login",
        json={"email": settings.admin_email, "password": settings.admin_password},
    )
    admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}
    res = client.patch(
        f"/api/admin/users/{user_id}", json={"is_approved": True}, headers=admin_headers
    )
    assert res.status_code == 403

    approve_user(client, owner, user_id)
    login = client.post("/api/auth/login", json={"email": email, "password": "Secret123"})
    assert login.status_code == 200


def test_approval_notifies_user_once(client, db):
    from sqlalchemy import func, select

    from app.models import Notification

    email = "notify.me@example.com"
    owner = _owner_headers(client)
    reg = client.post(
        "/api/auth/register",
        json={"full_name": "Notify Me", "email": email, "password": "Secret123"},
    )
    user_id = reg.json()["user_id"]

    approve_user(client, owner, user_id)
    notes = db.scalars(
        select(Notification).where(
            Notification.user_id == user_id, Notification.type == "account_approved"
        )
    ).all()
    assert len(notes) == 1

    # Approving again is idempotent: no duplicate notification.
    approve_user(client, owner, user_id)
    count = db.scalar(
        select(func.count(Notification.id)).where(
            Notification.user_id == user_id, Notification.type == "account_approved"
        )
    )
    assert count == 1


def _register(client, email, name="OTP User"):
    res = client.post(
        "/api/auth/register",
        json={"full_name": name, "email": email, "password": "Secret123"},
    )
    assert res.status_code == 200, res.text
    return res.json()


def test_login_blocked_until_approved(client):
    email = "gated.user@example.com"
    _register(client, email)
    res = client.post("/api/auth/login", json={"email": email, "password": "Secret123"})
    assert res.status_code == 403
    assert "pending approval" in res.json()["detail"].lower()


def test_owner_register_logs_instantly(client):
    res = client.post(
        "/api/auth/register",
        json={
            "full_name": "Owner",
            "email": settings.superadmin_email,
            "password": "Secret123",
        },
    )
    if res.status_code == 200:
        body = res.json()
        assert body["approved"] is True
        assert body["access_token"]
    else:
        assert res.status_code == 409


def test_removed_email_verification_routes(client):
    assert client.post("/api/auth/verify-email", json={"token": "x" * 32}).status_code == 404
    assert client.post("/api/auth/resend-otp", json={"email": "a@b.com"}).status_code == 404
