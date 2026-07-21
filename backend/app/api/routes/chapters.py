from uuid import UUID

from fastapi import APIRouter, status, HTTPException, Response

from app.api.dependencies import ChapterServiceDependency
from app.api.schemas import ChapterCreateRequest, ChapterUpdateRequest, ChapterResponse
from app.services.chapter_service import ChapterNotFoundError, ChapterNumberConflictError
from app.services.story_service import StoryNotFoundError


router = APIRouter(tags=["chapters"])


@router.post("/stories/{story_id}/chapters", response_model=ChapterResponse, status_code=status.HTTP_201_CREATED, summary="Create a chapter")
def create_chapter(story_id: UUID, request: ChapterCreateRequest, service: ChapterServiceDependency) -> ChapterResponse:
    try:
        chapter = service.create_chapter(story_id=story_id, data=request)

        return ChapterResponse.model_validate(chapter)
    except StoryNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found.") from error
    except ChapterNumberConflictError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=("A chapter with this number already exists in the story.")) from error


@router.get("/stories/{story_id}/chapters", response_model=list[ChapterResponse], summary="List the chapters of a story")
def list_story_chapters(story_id: UUID, service: ChapterServiceDependency) -> list[ChapterResponse]:
    try:
        chapters = service.list_story_chapters(story_id)

        return [ChapterResponse.model_validate(chapter) for chapter in chapters]
    except StoryNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found.") from error


@router.get("/chapters/{chapter_id}", response_model=ChapterResponse, summary="Get a chapter")
def get_chapter(chapter_id: UUID, service: ChapterServiceDependency) -> ChapterResponse:
    try:
        chapter = service.get_chapter(chapter_id)

        return ChapterResponse.model_validate(chapter)
    except ChapterNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found.") from error


@router.patch("/chapters/{chapter_id}", response_model=ChapterResponse, summary="Update a chapter")
def update_chapter(chapter_id: UUID, request: ChapterUpdateRequest, service: ChapterServiceDependency) -> ChapterResponse:
    try:
        chapter = service.update_chapter(chapter_id=chapter_id, data=request)

        return ChapterResponse.model_validate(chapter)
    except ChapterNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found.") from error
    except ChapterNumberConflictError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=("A chapter with this number already exists in the story.")) from error


@router.delete("/chapters/{chapter_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a chapter")
def delete_chapter(chapter_id: UUID, service: ChapterServiceDependency) -> Response:
    try:
        service.delete_chapter(chapter_id)
    except ChapterNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found.") from error

    return Response(status_code=status.HTTP_204_NO_CONTENT)
