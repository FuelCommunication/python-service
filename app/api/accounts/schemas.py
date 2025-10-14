from uuid import UUID

from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO
from litestar.dto import DTOConfig
from litestar.security.jwt import OAuth2Login
from pydantic import BaseModel, EmailStr

import app.db.models as m


class UserReadDto(SQLAlchemyDTO[m.User]):
    config = DTOConfig(exclude={"password", "created_at", "updated_at", "channels", "oauth_accounts"})


class RegisterAccount(BaseModel):
    email: EmailStr
    username: str
    password: str


class LoginAccount(BaseModel):
    email: EmailStr
    password: str


class OauthAccount(BaseModel):
    id: UUID
    oauth_name: str
    access_token: str
    account_id: str
    account_email: str
    expires_at: int | None = None
    refresh_token: str | None = None


class UserUpdatePartial(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    password: str | None = None
    avatar_url: str | None = None
    bio: str | None = None


class User(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    avatar_url: str | None = None
    bio: str | None = None

    model_config = {"from_attributes": True}


class AuthBody(BaseModel):
    user: User
    session: OAuth2Login
