import uuid

from litestar.dto import DTOConfig
from litestar.plugins.pydantic.dto import PydanticDTO
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class User(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str
    password: str
    avatar_url: str | None = None
    bio: str | None = None
    is_verified: bool = False

    model_config = ConfigDict(from_attributes=True)


class UserReadDto(PydanticDTO[User]):
    config = DTOConfig(exclude={"password"})


class CreateUser(BaseModel):
    email: EmailStr
    username: str
    password: str = Field(min_length=8, default=None)

    model_config = ConfigDict(from_attributes=True)


class GetUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, default=None)


class UserUpdatePartial(BaseModel):
    email: EmailStr | None = None
    username: str | None
    password: str | None = Field(min_length=8, default=None)
    avatar_url: str | None = None
    bio: str | None = None
    is_verified: bool | None = None
