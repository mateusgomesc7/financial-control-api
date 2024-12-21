from http import HTTPStatus

from app.schemas.members import MemberPublic


def test_create_member(client, user, token):
    response = client.post(
        "/members/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "test",
            "id_user_fk": user.id,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "name": "test",
        "id_user_fk": user.id,
        "id": 1,
    }


def test_read_members(client):
    response = client.get("/members/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"members": []}


def test_read_members_with_member(client, member):
    member_schema = MemberPublic.model_validate(member).model_dump()
    response = client.get("/members/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"members": [member_schema]}


def test_update_member(client, member, other_user, token):
    response = client.put(
        f"/members/{member.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "test",
            "id_user_fk": other_user.id,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "name": "test",
        "id_user_fk": other_user.id,
        "id": member.id,
    }


def test_delete_member(client, member, token):
    response = client.delete(
        f"/members/{member.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Member deleted successfully"}


def test_delete_member_not_permissions(client, other_member, token):
    response = client.delete(
        f"/members/{other_member.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        "detail": "You don't have permission to delete this member"
    }
