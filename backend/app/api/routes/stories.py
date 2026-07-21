from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict
from fastapi import APIRouter, status

from app.api.schemas import NonEmptyName
from app.api.errors import database_not_configured


router = APIRouter(prefix="/stories", tags=["stories"])

class StoryCreateRequest(BaseModel):
    title: NonEmptyName = Field(examples=["Arcadia"])
    description: str | None = Field(default=None, max_length=2000)

class StoryUpdateRequest(BaseModel):
    title: NonEmptyName | None = None
    description: str | None = Field(default=None, max_length=2000)

class StoryRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    created_at: datetime
    updated_at: datetime


@router.post("", response_model=StoryRequest, status_code=status.HTTP_201_CREATED, summary="Create a story")
def create_story(request: StoryCreateRequest) -> StoryRequest:
    database_not_configured("story")


@router.get("", response_model=list[StoryRequest], summary="List stories")
def list_stories() -> list[StoryRequest]:
    database_not_configured("story")


@router.get("/{story_id}", response_model=StoryRequest, summary="Get a story")
def get_story(story_id: UUID) -> StoryRequest:
    database_not_configured("story")


@router.patch("/{story_id}", response_model=StoryRequest, summary="Update a story")
def update_story(story_id: UUID, request: StoryUpdateRequest) -> StoryRequest:
    database_not_configured("story")


@router.delete("/{story_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a story")
def delete_story(story_id: UUID) -> None:
    database_not_configured("story")
