from fast_depends import Depends
from faststream.kafka import KafkaBroker

from app.api.accounts.schemas import UserUpdatePartial
from app.core.settings import settings

from .deps import UserRepository, get_users_repo
from .schemas import UpdateImage

broker = KafkaBroker(settings.broker_url)


@broker.subscriber("images")
async def handle_images(message: UpdateImage, users_repo: UserRepository = Depends(get_users_repo)):
    await users_repo.update_partial(user_id=message.user_id, data=UserUpdatePartial(avatar_url=message.data))
