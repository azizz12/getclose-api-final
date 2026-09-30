# =============================================================
# Tests de /auth/register et /auth/login — cas nominaux et d'erreur.
# =============================================================


def test_register_creates_user(client):
    response = client.post(
        "/auth/register",
        json={"pseudo": "Zouzou", "email": "zouzou@test.com", "password": "motdepasse123"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["pseudo"] == "Zouzou"
    assert body["email"] == "zouzou@test.com"
    # Le mot de passe hashé ne doit JAMAIS apparaître dans la réponse.
    assert "hashed_password" not in body
    assert "password" not in body


def test_register_rejects_duplicate_email(client):
    payload = {"pseudo": "Zouzou", "email": "zouzou@test.com", "password": "motdepasse123"}
    client.post("/auth/register", json=payload)

    response = client.post(
        "/auth/register",
        json={"pseudo": "Autre", "email": "zouzou@test.com", "password": "autremotdepasse"},
    )
    assert response.status_code == 409


def test_register_rejects_short_password(client):
    response = client.post(
        "/auth/register",
        json={"pseudo": "Zouzou", "email": "zouzou@test.com", "password": "court"},
    )
    # Rejeté par Pydantic avant même d'atteindre la logique métier.
    assert response.status_code == 422


def test_login_returns_token(client):
    client.post(
        "/auth/register",
        json={"pseudo": "Zouzou", "email": "zouzou@test.com", "password": "motdepasse123"},
    )
    response = client.post(
        "/auth/login", json={"email": "zouzou@test.com", "password": "motdepasse123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_rejects_wrong_password(client):
    client.post(
        "/auth/register",
        json={"pseudo": "Zouzou", "email": "zouzou@test.com", "password": "motdepasse123"},
    )
    response = client.post(
        "/auth/login", json={"email": "zouzou@test.com", "password": "mauvais"}
    )
    assert response.status_code == 401


def test_login_rejects_unknown_email(client):
    response = client.post(
        "/auth/login", json={"email": "inconnu@test.com", "password": "peuimporte"}
    )
    assert response.status_code == 401
