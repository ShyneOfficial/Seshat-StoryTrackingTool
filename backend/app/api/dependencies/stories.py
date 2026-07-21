from typing import Annotated

from fastapi import Depends

from app.repositories.story_repository import StoryRepository
from app.services.story_service import StoryService
from app.api.dependencies.database import DatabaseSession


def get_story_service(session: DatabaseSession) -> StoryService:
    return StoryService(
        session=session,
        repository=StoryRepository(session)
    )


StoryServiceDependency = Annotated[
    StoryService,
    Depends(get_story_service),
]
