from pydantic import BaseModel, Field, ConfigDict
import uuid
from ..config import settings


class ConversationRequestBase(BaseModel):
    model_config = ConfigDict(extra=settings.schemas_settings.extra)


class ConversationBase(BaseModel):
    name: str = Field(max_length=20)


class ConversationRequest(ConversationBase, ConversationRequestBase):
    user_admin_fk: uuid.UUID


class ConversationResponse(ConversationBase):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)
    user_admin_fk: uuid.UUID


class ConversationUpdate(ConversationBase, ConversationRequestBase):
    name: str = Field(max_length=20, default=None)


class AddUser(BaseModel):
    user_id: uuid.UUID
    is_moder: bool = False
