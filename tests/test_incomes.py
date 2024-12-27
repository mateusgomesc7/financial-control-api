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


def test_read_incomes_paginated(client, token):
    response = client.get(
        "/incomes/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "items": [],
        "pagination": {
            "count": 0,
            "page": 1,
            "per_page": 10,
            "total": 0,
            "total_pages": 1,
        },
    }


def test_read_incomes_paginated_with_income(
    client, member, income, token, mock_db_time
):
    with mock_db_time(model=Income, time=datetime(2024, 1, 1)):
        response = client.get(
            "/incomes/",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            "items": [
                {
                    "name": income.name,
                    "amount": float(income.amount),
                    "id_user_fk": income.id_user_fk,
                    "id": income.id,
                    "member": {
                        "id": member.id,
                        "name": member.name,
                    },
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00",
                }
            ],
            "pagination": {
                "count": 1,
                "page": 1,
                "per_page": 10,
                "total": 1,
                "total_pages": 1,
            },
        }


def test_update_income(client, income, member, token):
    response = client.put(
        f"/incomes/{income.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "test",
            "amount": 200.0,
            "id_member_fk": income.id_member_fk,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "name": "test",
        "amount": 200.0,
        "id_user_fk": income.id_user_fk,
        "id": income.id,
        "member": {
            "id": member.id,
            "name": member.name,
        },
        "created_at": income.created_at.isoformat(),
        "updated_at": income.updated_at.isoformat(),
    }
