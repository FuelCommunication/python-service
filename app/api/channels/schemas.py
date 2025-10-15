from uuid import UUID

from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO
from litestar.dto import DTOConfig
from pydantic import BaseModel

import app.db.models as m


class ChannelReadDto(SQLAlchemyDTO[m.Channel]):
    config = DTOConfig(exclude={"created_at", "updated_at", "subscribers"})


class CreateChannel(BaseModel):
    title: str
    description: str
    avatar_url: str | None = None


class UpdateChannelPartial(BaseModel):
    title: str | None = None
    description: str | None = None
    avatar_url: str | None = None


class Subscriber(BaseModel):
    id: UUID
    username: str


class Subscription(BaseModel):
    id: UUID
    title: str
    description: str
    avatar_url: str | None
