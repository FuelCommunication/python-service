from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from advanced_alchemy.base import UUIDv7AuditBase
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .user import UsersModel


class UserOauthModel(UUIDv7AuditBase):
    __tablename__ = "UserOauthModel"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("Users.id", ondelete="cascade"))
    oauth_name: Mapped[str] = mapped_column(String(length=100), index=True)
    access_token: Mapped[str] = mapped_column(String(length=1024))
    expires_at: Mapped[int | None]
    refresh_token: Mapped[str | None]
    account_id: Mapped[str] = mapped_column(String(length=320), index=True)
    account_email: Mapped[str] = mapped_column(String(length=320))

    user: Mapped[UsersModel] = relationship(
        back_populates="oauth_accounts",
        innerjoin=True,
        lazy="joined",
    )
