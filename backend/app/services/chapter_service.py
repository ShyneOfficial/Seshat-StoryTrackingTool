from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.schemas import ChapterCreateRequest, ChapterUpdateRequest
from app.db.models.chapter import Chapter
from app.repositories.chapter_repository import ChapterRepository
from app.repositories.story_repository import StoryRepository
from app.services.story_service import StoryNotFoundError


class ChapterNotFoundError(Exception):
    pass


class ChapterNumberConflictError(Exception):
    pass


class ChapterService:
    def __init__(self, session: Session, chapter_repository: ChapterRepository, story_repository: StoryRepository) -> None:
        self.session = session
        self.chapter_repository = chapter_repository
        self.story_repository = story_repository

    def create_chapter(self, story_id: UUID, data: ChapterCreateRequest) -> Chapter:
        self._ensure_story_exists(story_id)

        existing_chapter = (
            self.chapter_repository.get_by_story_and_number(
                story_id=story_id,
                number=data.number,
            )
        )

        if existing_chapter is not None:
            raise ChapterNumberConflictError(data.number)

        try:
            chapter = self.chapter_repository.create(
                story_id=story_id,
                title=data.title,
                number=data.number,
                content=data.content,
            )

            self.session.commit()
            self.session.refresh(chapter)
        except IntegrityError as error:
            self.session.rollback()
            if self._get_constraint_name(error) == "uq_chapters_story_id_number":
                raise ChapterNumberConflictError(data.number) from error
            raise

        return chapter

    def list_story_chapters(self, story_id: UUID) -> list[Chapter]:
        self._ensure_story_exists(story_id)

        return self.chapter_repository.get_all_by_story_id(story_id)

    def get_chapter(self, chapter_id: UUID) -> Chapter:
        chapter = self.chapter_repository.get_by_id(chapter_id)

        if chapter is None:
            raise ChapterNotFoundError(chapter_id)

        return chapter

    def update_chapter(self, chapter_id: UUID, data: ChapterUpdateRequest) -> Chapter:
        chapter = self.get_chapter(chapter_id)
        changes = data.model_dump(exclude_unset=True)

        if "number" in changes and changes["number"] != chapter.number:
            existing_chapter = (
                self.chapter_repository.get_by_story_and_number(
                    story_id=chapter.story_id,
                    number=changes["number"],
                )
            )

            if existing_chapter is not None:
                raise ChapterNumberConflictError(changes["number"])

        if "content" in changes and changes["content"] != chapter.content:
            chapter.revision += 1

        for field, value in changes.items():
            setattr(chapter, field, value)

        try:
            self.session.commit()
            self.session.refresh(chapter)
        except IntegrityError as error:
            self.session.rollback()

            if self._get_constraint_name(error) == "uq_chapters_story_id_number":
                raise ChapterNumberConflictError(changes.get("number", chapter.number)) from error
            raise

        return chapter

    def delete_chapter(self, chapter_id: UUID) -> None:
        chapter = self.get_chapter(chapter_id)

        self.chapter_repository.delete(chapter)
        self.session.commit()

    def _ensure_story_exists(self, story_id: UUID) -> None:
        story = self.story_repository.get_by_id(story_id)

        if story is None:
            raise StoryNotFoundError(story_id)

    @staticmethod
    def _get_constraint_name(error: IntegrityError) -> str | None:
        diagnostic = getattr(error.orig, "diag", None)

        return getattr(diagnostic, "constraint_name", None)
