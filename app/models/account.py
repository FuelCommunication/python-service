from advanced_alchemy.base import UUIDv7AuditBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class AccountModel(UUIDv7AuditBase):
    __tablename__ = "Accounts"

    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    username: Mapped[str]
    password: Mapped[bytes]

    avatar_url: Mapped[str | None] = mapped_column(String(length=500), nullable=True, default=None)
    bio: Mapped[str | None]
    is_verified: Mapped[bool] = mapped_column(default=False)
