from uuid import UUID

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)


class IDResponseSchema(BaseModel):
    created_id: UUID = Field(..., alias="id")
