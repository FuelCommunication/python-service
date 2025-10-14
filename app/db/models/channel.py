from __future__ import annotations

from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDv7AuditBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .channel_subscribers import ChannelSubscribers


class Channel(UUIDv7AuditBase):
    __tablename__ = "Channels"

    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str | None] = mapped_column(String(length=300), default=None)
    avatar_url: Mapped[str | None] = mapped_column(String(length=500), default=None)

    subscribers: Mapped[list[ChannelSubscribers]] = relationship(
        back_populates="channel",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
