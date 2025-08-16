from uuid import UUID

from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO
from litestar.dto import DTOConfig
from pydantic import BaseModel, EmailStr

from ...db.models import UsersModel


class OauthAccount(BaseModel):
    id: UUID
    oauth_name: str
    access_token: str
    account_id: str
    account_email: str
    expires_at: int | None = None
    refresh_token: str | None = None


class UserReadDto(SQLAlchemyDTO[UsersModel]):
    config = DTOConfig(exclude={"password"})


class UserUpdatePartial(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    password: str | None = None
    avatar_url: str | None = None
    bio: str | None = None


class RegisterAccount(BaseModel):
    email: EmailStr
    username: str
    password: str


class LoginAccount(BaseModel):
    email: EmailStr
    password: str
