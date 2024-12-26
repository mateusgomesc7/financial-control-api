from datetime import datetime
from http import HTTPStatus

from app.models.income import Income


def test_create_income(client, user, member, token, mock_db_time):
    with mock_db_time(model=Income, time=datetime(2024, 1, 1)):
        response = client.post(
            "/incomes/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "test",
                "amount": 100.0,
                "id_member_fk": member.id,
            },
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            "name": "test",
            "amount": 100.0,
            "id_user_fk": user.id,
            "id": 1,
            "member": {
                "id": member.id,
                "name": member.name,
            },
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00",
        }
