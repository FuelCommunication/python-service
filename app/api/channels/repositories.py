from collections.abc import Sequence
from uuid import UUID

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from litestar.repository import ConflictError, NotFoundError
from sqlalchemy import RowMapping, exists, select

import app.db.models as m

from .schemas import CreateChannel, UpdateChannelPartial


class ChannelRepository(SQLAlchemyAsyncRepository[m.Channel]):
    model_type = m.Channel

    async def get_user_subscriptions(self, *, user_id: UUID) -> Sequence[RowMapping]:
        stmt = (
            select(
                m.Channel.id,
                m.Channel.title,
                m.Channel.description,
                m.Channel.avatar_url,
            )
            .join(m.Channel.subscribers)
            .where(m.ChannelSubscribers.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.mappings().all()

    async def get_channel_subscribers(self, *, channel_id: UUID) -> Sequence[RowMapping]:
        stmt = (
            select(
                m.User.id,
                m.User.username,
            )
            .join(m.User.channels)
            .where(m.ChannelSubscribers.channel_id == channel_id)
        )
        result = await self.session.execute(stmt)
        return result.mappings().all()

    async def create(self, *, user_id: UUID, data: CreateChannel) -> m.Channel:
        new_channel = m.Channel(**data.model_dump(exclude_unset=True, exclude_none=True))
        obj = await self.add(new_channel)
        await self.session.flush()

        owner_sub = m.ChannelSubscribers(
            user_id=user_id,
            channel_id=obj.id,
            is_owner=True,
        )
        self.session.add(owner_sub)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def is_exist(self, *, title: str) -> bool:
        stmt = select(exists().where(self.model_type.title == title))
        result = await self.session.execute(stmt)
        return bool(result.scalar())

    async def update_partial(self, *, channel_id: UUID, data: UpdateChannelPartial) -> m.Channel:
        channel = await self.get(channel_id)
        if not channel:
            raise NotFoundError(f"Channel with ID {channel_id} not found")

        raw_obj = data.model_dump(exclude_unset=True, exclude_none=True)
        raw_obj.update({"id": channel_id})
        obj = await self.update(m.Channel(**raw_obj))
        await self.session.commit()
        return obj

    async def subscribe(self, *, user_id: UUID, channel_id: UUID) -> None:
        user = await self.session.get(m.User, user_id)
        channel = await self.session.get(m.Channel, channel_id)

        if not user or not channel:
            raise NotFoundError("User or channel not found")

        stmt = select(m.ChannelSubscribers).where(
            m.ChannelSubscribers.user_id == user_id,
            m.ChannelSubscribers.channel_id == channel_id,
        )
        existing = await self.session.scalar(stmt)
        if existing:
            return

        subscription = m.ChannelSubscribers(
            user_id=user_id,
            channel_id=channel_id,
            is_owner=False,
        )
        self.session.add(subscription)
        await self.session.commit()

    async def unsubscribe(self, *, user_id: UUID, channel_id: UUID) -> None:
        stmt = select(m.ChannelSubscribers).where(
            m.ChannelSubscribers.user_id == user_id,
            m.ChannelSubscribers.channel_id == channel_id,
        )
        subscription = await self.session.scalar(stmt)

        if not subscription:
            raise NotFoundError("Subscription not found")
        if subscription.is_owner:
            raise ConflictError("Owner cannot unsubscribe from their own channel")

        await self.session.delete(subscription)
        await self.session.commit()
