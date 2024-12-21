from http import HTTPStatus

from freezegun import freeze_time


def test_get_token(client, user):
    response = client.post(
        "/auth/token/",
        data={"username": user.username, "password": user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token["token_type"] == "Bearer"
    assert "access_token" in token


def test_jwt_invalid_token(client):
    response = client.delete(
        "/users/1", headers={"Authorization": "Bearer token-invalido"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_jwt_expired_token(client, user):
    with freeze_time("2023-07-14 12:00:00"):
        response = client.post(
            "/auth/token/",
            data={"username": user.username, "password": user.clean_password},
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time("2023-07-14 12:31:00"):
        response = client.put(
            f"/users/{user.id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "new-name",
                "username": "new-username",
                "email": "email@email.com",
                "password": "new-password",
            },
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Could not validate credentials"}


def test_token_wrong_password(client, user):
    response = client.post(
        "/auth/token/",
        data={"username": user.username, "password": "wrong-password"},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Incorrect username or password"}


def test_token_wrong_username(client, user):
    response = client.post(
        "/auth/token/",
        data={"username": "wrong_username", "password": user.clean_password},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Incorrect username or password"}


def test_refresh_token(client, token):
    response = client.post(
        "/auth/refresh_token/",
        headers={"Authorization": f"Bearer {token}"},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert data["token_type"] == "Bearer"
    assert "access_token" in data
    assert "token_type" in data


def test_token_expired_dont_refresh(client, user):
    with freeze_time("2023-07-14 12:00:00"):
        response = client.post(
            "/auth/token",
            data={"username": user.username, "password": user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time("2023-07-14 12:31:00"):
        response = client.post(
            "/auth/refresh_token",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Could not validate credentials"}
