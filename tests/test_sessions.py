# =============================================================
# Tests de /sessions — CRUD complet et protection par JWT.
# =============================================================
import pytest


@pytest.fixture()
def auth_headers(client):
    """Crée un compte, se connecte, et renvoie les headers prêts à
    réutiliser dans les tests qui suivent — évite de répéter ces 2
    appels dans chaque test."""
    client.post(
        "/auth/register",
        json={"pseudo": "Zouzou", "email": "zouzou@test.com", "password": "motdepasse123"},
    )
    response = client.post(
        "/auth/login", json={"email": "zouzou@test.com", "password": "motdepasse123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_session_requires_auth(client):
    response = client.post("/sessions")
    assert response.status_code == 401


def test_create_session(client, auth_headers):
    response = client.post("/sessions", headers=auth_headers)
    assert response.status_code == 201
    body = response.json()
    assert body["score_total"] == 0
    assert body["finished"] is False


def test_list_sessions_only_returns_mine(client, auth_headers):
    client.post("/sessions", headers=auth_headers)
    client.post("/sessions", headers=auth_headers)

    response = client.get("/sessions", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_session_score(client, auth_headers):
    created = client.post("/sessions", headers=auth_headers).json()

    response = client.patch(
        f"/sessions/{created['id']}",
        json={"score_total": 420, "finished": True},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["score_total"] == 420
    assert response.json()["finished"] is True


def test_get_unknown_session_returns_404(client, auth_headers):
    response = client.get("/sessions/999999", headers=auth_headers)
    assert response.status_code == 404


def test_cannot_access_another_users_session(client, auth_headers):
    created = client.post("/sessions", headers=auth_headers).json()

    # Un deuxième compte ne doit pas pouvoir voir la partie du premier.
    client.post(
        "/auth/register",
        json={"pseudo": "Aziz", "email": "aziz@test.com", "password": "motdepasse456"},
    )
    other_token = client.post(
        "/auth/login", json={"email": "aziz@test.com", "password": "motdepasse456"}
    ).json()["access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}

    response = client.get(f"/sessions/{created['id']}", headers=other_headers)
    assert response.status_code == 403


def test_delete_session(client, auth_headers):
    created = client.post("/sessions", headers=auth_headers).json()

    response = client.delete(f"/sessions/{created['id']}", headers=auth_headers)
    assert response.status_code == 204

    response = client.get(f"/sessions/{created['id']}", headers=auth_headers)
    assert response.status_code == 404
