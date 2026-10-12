"""Superadmin role, signup notifications, and privilege guards."""

from app.core.config import settings


def _register_verify(client, email, name="Test User"):
    from conftest import _owner_headers, approve_user

    reg = client.post(
        "/api/auth/register",
        json={"full_name": name, "email": email, "password": "Secret123"},
    )
    if reg.status_code == 200:
        body = reg.json()
        approve_user(client, _owner_headers(client), body["user_id"])
    else:
        assert reg.status_code == 409, reg.text  # already registered by an earlier test
    login = client.post("/api/auth/login", json={"email": email, "password": "Secret123"})
    assert login.status_code == 200, login.text
    return login.json()["access_token"]


def _auth(token):
    return {"Authorization": f"Bearer {token}"}


def _admin_token(client):
    res = client.post(
        "/api/auth/login",
        json={"email": settings.admin_email, "password": settings.admin_password},
    )
    assert res.status_code == 200, res.text
    return res.json()["access_token"]


def test_superadmin_email_gets_role_on_signup(client):
    token = _register_verify(client, settings.superadmin_email, "Owner")
    me = client.get("/api/auth/me", headers=_auth(token)).json()
    assert me["user"]["role"] == "superadmin"


def test_new_signup_notifies_superadmin(client):
    owner_token = _register_verify(client, settings.superadmin_email, "Owner")
    newcomer = "newcomer.notify@example.com"
    _register_verify(client, newcomer, "New Comer")
    body = client.get("/api/admin/notifications", headers=_auth(owner_token)).json()
    assert body["unread_count"] >= 1
    matches = [n for n in body["items"] if newcomer in (n["body"] or "")]
    assert matches, "expected a signup notification for the newcomer"
    assert matches[0]["type"] == "user_signup"
    assert matches[0]["is_read"] is False


def test_notifications_forbidden_for_others(client, auth_headers):
    admin_headers = _auth(_admin_token(client))
    assert client.get("/api/admin/notifications", headers=admin_headers).status_code == 403
    assert client.get("/api/admin/notifications", headers=auth_headers).status_code == 403
    assert client.get("/api/admin/notifications").status_code == 401


def test_notifications_mark_read(client):
    owner_token = _register_verify(client, settings.superadmin_email, "Owner")
    _register_verify(client, "read.me@example.com", "Read Me")
    headers = _auth(owner_token)
    before = client.get("/api/admin/notifications", headers=headers).json()
    assert before["unread_count"] >= 1
    res = client.post("/api/admin/notifications/read", json={}, headers=headers)
    assert res.status_code == 200
    assert res.json()["updated"] >= 1
    after = client.get("/api/admin/notifications", headers=headers).json()
    assert after["unread_count"] == 0


def test_only_superadmin_can_grant_superadmin(client, auth_headers):
    newcomer_token = _register_verify(client, "promote.me@example.com", "Promote Me")
    newcomer_id = (
        client.get("/api/auth/me", headers=_auth(newcomer_token)).json()["user"]["id"]
    )
    admin_headers = _auth(_admin_token(client))

    res = client.patch(
        f"/api/admin/users/{newcomer_id}", json={"role": "superadmin"}, headers=admin_headers
    )
    assert res.status_code == 403

    owner_token = _register_verify(client, settings.superadmin_email, "Owner")
    res = client.patch(
        f"/api/admin/users/{newcomer_id}",
        json={"role": "superadmin"},
        headers=_auth(owner_token),
    )
    assert res.status_code == 200
    assert res.json()["role"] == "superadmin"


def test_admin_cannot_touch_superadmin_account(client):
    owner_token = _register_verify(client, settings.superadmin_email, "Owner")
    owner_id = client.get("/api/auth/me", headers=_auth(owner_token)).json()["user"]["id"]
    admin_headers = _auth(_admin_token(client))

    res = client.patch(
        f"/api/admin/users/{owner_id}", json={"is_active": False}, headers=admin_headers
    )
    assert res.status_code == 403


def test_superadmin_can_use_admin_panel_apis(client):
    owner_token = _register_verify(client, settings.superadmin_email, "Owner")
    res = client.get("/api/admin/users", headers=_auth(owner_token))
    assert res.status_code == 200
    assert "items" in res.json()
