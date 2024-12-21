from http import HTTPStatus

from app.schemas.members import MemberPublic


def test_create_month(client, user):
    date = "2024-12-01T00:00:01"
    response = client.post(
        "/months/",
        json={"created_at": date},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"id": 1, "created_at": date}
