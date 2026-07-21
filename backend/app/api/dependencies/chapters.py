from typing import Annotated

from fastapi import Depends

from app.api.dependencies.database import DatabaseSession
from app.repositories.chapter_repository import ChapterRepository
from app.repositories.story_repository import StoryRepository
from app.services.chapter_service import ChapterService


def get_chapter_service(session: DatabaseSession) -> ChapterService:
    return ChapterService(
        session=session,
        chapter_repository=ChapterRepository(session),
        story_repository=StoryRepository(session),
    )


ChapterServiceDependency = Annotated[
    ChapterService,
    Depends(get_chapter_service),
]
