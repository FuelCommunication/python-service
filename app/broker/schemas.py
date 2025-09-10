from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class UpdateImage(BaseModel):
    user_id: UUID
    action: Literal["create", "update", "delete"]
    data: str | None
