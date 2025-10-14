from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from advanced_alchemy.base import UUIDv7AuditBase
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .channel import Channel
    from .user import User


class ChannelSubscribers(UUIDv7AuditBase):
    __tablename__ = "ChannelSubscribers"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("Users.id", ondelete="cascade"), nullable=False)
    channel_id: Mapped[UUID] = mapped_column(ForeignKey("Channels.id", ondelete="cascade"), nullable=False)
    is_owner: Mapped[bool] = mapped_column(default=False)

    user: Mapped[User] = relationship(
        back_populates="channels",
        foreign_keys="ChannelSubscribers.user_id",
        innerjoin=True,
        uselist=False,
        lazy="joined",
    )
    channel: Mapped[Channel] = relationship(
        back_populates="subscribers",
        foreign_keys="ChannelSubscribers.channel_id",
        innerjoin=True,
        uselist=False,
        lazy="joined",
    )
