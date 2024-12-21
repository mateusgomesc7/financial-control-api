from pydantic import BaseModel, ConfigDict


class MemberSchema(BaseModel):
    name: str
    id_user_fk: int


class MemberPublic(BaseModel):
    id: int
    name: str
    id_user_fk: int

    model_config = ConfigDict(from_attributes=True)


class MemberList(BaseModel):
    members: list[MemberPublic]
