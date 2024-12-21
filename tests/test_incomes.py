from http import HTTPStatus


def test_create_income(client, member, token):
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
        "id_member_fk": member.id,
        "id": 1,
    }
