from uuid import UUID

from fastapi import APIRouter, status, HTTPException, Response

from app.api.dependencies import StoryServiceDependency
from app.services.story_service import StoryNotFoundError
from app.api.schemas import StoryCreateRequest, StoryUpdateRequest, StoryResponse


router = APIRouter(prefix="/stories", tags=["stories"])


@router.post("", response_model=StoryResponse, status_code=status.HTTP_201_CREATED, summary="Create a story")
def create_story(request: StoryCreateRequest, service: StoryServiceDependency) -> StoryResponse:
    story = service.create_story(request)

    return StoryResponse.model_validate(story)


@router.get("", response_model=list[StoryResponse], summary="List stories")
def list_stories(service: StoryServiceDependency) -> list[StoryResponse]:
    stories = service.list_stories()

    return [StoryResponse.model_validate(story) for story in stories]


@router.get("/{story_id}", response_model=StoryResponse, summary="Get a story")
def get_story(story_id: UUID, service: StoryServiceDependency) -> StoryResponse:
    try:
        story = service.get_story(story_id)

        return StoryResponse.model_validate(story)
    except StoryNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found.") from error


@router.patch("/{story_id}", response_model=StoryResponse, summary="Update a story")
def update_story(story_id: UUID, request: StoryUpdateRequest, service: StoryServiceDependency) -> StoryResponse:
    try:
        story = service.update_story(story_id, request)

        return StoryResponse.model_validate(story)
    except StoryNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found.") from error


@router.delete("/{story_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a story")
def delete_story(story_id: UUID, service: StoryServiceDependency) -> Response:
    try:
        service.delete_story(story_id)
    except StoryNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found.") from error

    return Response(status_code=status.HTTP_204_NO_CONTENT)
