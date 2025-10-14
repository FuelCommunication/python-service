from __future__ import annotations

from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDv7AuditBase
from sqlalchemy import LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .channel_subscribers import ChannelSubscribers
    from .oauth_user import UserOauth


class User(UUIDv7AuditBase):
    __tablename__ = "Users"

    email: Mapped[str] = mapped_column(unique=True, index=True)
    username: Mapped[str]
    password: Mapped[bytes | None] = mapped_column(LargeBinary, default=None)
    avatar_url: Mapped[str | None] = mapped_column(String(length=500))
    bio: Mapped[str | None]

    channels: Mapped[list[ChannelSubscribers]] = relationship(
        back_populates="user",
        lazy="selectin",
        cascade="all, delete",
        viewonly=True,
    )
    oauth_accounts: Mapped[list[UserOauth]] = relationship(
        back_populates="user", lazy="selectin", cascade="all, delete-orphan", uselist=True
    )
