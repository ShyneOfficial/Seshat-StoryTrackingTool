from uuid import UUID
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, ConfigDict, model_validator

from app.api.schemas.shared import NonEmptyName

class StoryCreateRequest(BaseModel):
    title: NonEmptyName = Field(examples=["Arcadia"])
    description: str | None = Field(default=None, max_length=2000)


class StoryUpdateRequest(BaseModel):
    title: NonEmptyName | None = None
    description: str | None = Field(default=None, max_length=2000)

    @model_validator(mode="before")
    @classmethod
    def reject_null_title(cls, data: Any) -> Any:
        if isinstance(data, dict) and "title" in data and data["title"] is None:
            raise ValueError("title cannot be null")

        return data


class StoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    created_at: datetime
    updated_at: datetime
