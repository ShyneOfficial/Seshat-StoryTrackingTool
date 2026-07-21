from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict
from fastapi import APIRouter, status

from app.api.schemas import NonEmptyName
from app.api.errors import database_not_configured


router = APIRouter(tags=["chapters"])

class ChapterCreateRequest(BaseModel):
    title: NonEmptyName = Field(examples=["Initialization"])
    number: int = Field(ge=1, examples=[1])
    content: str = Field(default="", examples=["Owen woke up in the forest."])

class ChapterUpdateRequest(BaseModel):
    title: NonEmptyName | None = None
    number: int | None = Field(default=None, ge=1)
    content: str | None = None

class ChapterRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    story_id: UUID
    title: str
    number: int
    content: str
    revision: int
    created_at: datetime
    updated_at: datetime


@router.post("/stories/{story_id}/chapters", response_model=ChapterRequest, status_code=status.HTTP_201_CREATED, summary="Create a chapter")
def create_chapter(story_id: UUID, request: ChapterCreateRequest) -> ChapterRequest:
    database_not_configured("chapter")


@router.get("/stories/{story_id}/chapters", response_model=list[ChapterRequest], summary="List the chapters of a story")
def list_story_chapters(story_id: UUID) -> list[ChapterRequest]:
    database_not_configured("chapter")


@router.get("/chapters/{chapter_id}", response_model=ChapterRequest, summary="Get a chapter")
def get_chapter(chapter_id: UUID) -> ChapterRequest:
    database_not_configured("chapter")


@router.patch("/chapters/{chapter_id}", response_model=ChapterRequest, summary="Update a chapter")
def update_chapter(chapter_id: UUID, request: ChapterUpdateRequest) -> ChapterRequest:
    database_not_configured("chapter")


@router.delete("/chapters/{chapter_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a chapter")
def delete_chapter(chapter_id: UUID) -> None:
    database_not_configured("chapter")
