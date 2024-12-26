from pydantic import BaseModel, ConfigDict


class MemberSchema(BaseModel):
    name: str


class MemberPublic(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class MemberList(BaseModel):
    members: list[MemberPublic]
