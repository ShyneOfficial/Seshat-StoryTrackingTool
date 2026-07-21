from uuid import UUID
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, ConfigDict, model_validator

from app.api.schemas.shared import NonEmptyName


class ChapterCreateRequest(BaseModel):
    title: NonEmptyName = Field(examples=["Initialization"])
    number: int = Field(ge=1, examples=[1])
    content: str = Field(default="", examples=["Owen woke up in the forest."])


class ChapterUpdateRequest(BaseModel):
    title: NonEmptyName | None = None
    number: int | None = Field(default=None, ge=1)
    content: str | None = None

    @model_validator(mode="before")
    @classmethod
    def reject_null_values(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        for field in ("title", "number", "content"):
            if field in data and data[field] is None:
                raise ValueError(f"The {field.capitalize()} of the chapter cannot be null")

        return data


class ChapterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    story_id: UUID
    title: str
    number: int
    content: str
    revision: int
    created_at: datetime
    updated_at: datetime
