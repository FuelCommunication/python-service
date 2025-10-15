from uuid import UUID

from advanced_alchemy.exceptions import NotFoundError
from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.exceptions import HTTPException, NotFoundException
from litestar.pagination import OffsetPagination
from litestar.repository.filters import LimitOffset
from litestar.status_codes import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_409_CONFLICT

import app.db.models as m

from .deps import provide_channel_repo, provide_limit_offset_pagination
from .repositories import ChannelRepository
from .schemas import ChannelReadDto, CreateChannel, Subscriber, Subscription, UpdateChannelPartial


class ChannelController(Controller):
    """Channel Controller"""

    path = "/channels"
    tags = ["Channels"]
    dependencies = {"channels_repo": Provide(provide_channel_repo), "limit_offset": Provide(provide_limit_offset_pagination)}
    return_dto = ChannelReadDto

    @post(path="{user_id:uuid}", status_code=HTTP_201_CREATED)
    async def create(self, user_id: UUID, data: CreateChannel, channels_repo: ChannelRepository) -> m.Channel:
        """Create a new channel"""
        channel = await channels_repo.is_exist(title=data.title)
        if channel:
            raise HTTPException(status_code=HTTP_409_CONFLICT, detail="Channel is already exist")

        new_channel = await channels_repo.create(user_id=user_id, data=data)
        return new_channel

    @get()
    async def get_channels(self, channels_repo: ChannelRepository, limit_offset: LimitOffset) -> OffsetPagination[m.Channel]:
        """Get an existing channel"""
        results, total = await channels_repo.list_and_count(limit_offset)
        return OffsetPagination[m.Channel](
            items=results,
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )

    @get(path="/sub/user/{user_id:uuid}")
    async def get_channel_subscriptions(self, user_id: UUID, channels_repo: ChannelRepository) -> list[Subscription]:
        """Get an existing channel"""
        channels = await channels_repo.get_user_subscriptions(user_id=user_id)
        return [Subscription(**row) for row in channels]

    @get(path="/sub/channel/{channel_id:uuid}")
    async def get_channel_subscribers(self, channel_id: UUID, channels_repo: ChannelRepository) -> list[Subscriber]:
        """Get an existing channel"""
        users = await channels_repo.get_channel_subscribers(channel_id=channel_id)
        return [Subscriber(**row) for row in users]

    @patch(path="/{channel_id:uuid}", status_code=HTTP_201_CREATED)
    async def partial_update(self, channel_id: UUID, data: UpdateChannelPartial, channels_repo: ChannelRepository) -> m.Channel:
        """Update a channel"""
        try:
            channel = await channels_repo.update_partial(channel_id=channel_id, data=data)
            return channel
        except NotFoundError:
            raise NotFoundException(detail=f"Channel with ID {channel_id} not found")

    @delete(path="/{channel_id:uuid}")
    async def delete(self, channel_id: UUID, channels_repo: ChannelRepository) -> None:
        """Delete an existing channel"""
        try:
            await channels_repo.delete(channel_id)
        except NotFoundError:
            raise NotFoundException(detail=f"Channel with ID {channel_id} not found")

    @post(path="/{channel_id:uuid}/subscribe/{user_id:uuid}", status_code=HTTP_204_NO_CONTENT)
    async def subscribe(self, channel_id: UUID, user_id: UUID, channels_repo: ChannelRepository) -> None:
        """Subscribe user to channel"""
        try:
            await channels_repo.subscribe(user_id=user_id, channel_id=channel_id)
        except NotFoundError:
            raise NotFoundException(detail="User or channel not found")

    @post(path="/{channel_id:uuid}/unsubscribe/{user_id:uuid}", status_code=HTTP_204_NO_CONTENT)
    async def unsubscribe(self, channel_id: UUID, user_id: UUID, channels_repo: ChannelRepository) -> None:
        """Unsubscribe user from channel"""
        try:
            await channels_repo.unsubscribe(user_id=user_id, channel_id=channel_id)
        except NotFoundError:
            raise NotFoundException(detail="User or channel not found")
