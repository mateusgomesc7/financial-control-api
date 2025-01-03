from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]
