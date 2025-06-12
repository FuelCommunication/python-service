import uuid

from litestar.dto import DTOConfig
from litestar.plugins.pydantic.dto import PydanticDTO
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Account(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str
    password: str
    avatar_url: str | None = None
    bio: str | None = None
    is_verified: bool = False

    model_config = ConfigDict(from_attributes=True)


class AccountReadDto(PydanticDTO[Account]):
    config = DTOConfig(exclude={"password"})


class AccountUpdatePartial(BaseModel):
    email: EmailStr | None = None
    username: str | None
    password: str | None = Field(min_length=8, default=None)
    avatar_url: str | None = None
    bio: str | None = None
    is_verified: bool | None = None


class CreateAccount(BaseModel):
    email: EmailStr
    username: str
    password: str = Field(min_length=8, default=None)

    model_config = ConfigDict(from_attributes=True)


class GetAccount(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, default=None)
