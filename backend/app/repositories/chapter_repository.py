from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Chapter


class ChapterRepository:
    def __init__(self, session: Session) -> None:
        self.session = session


    def create(self, story_id: UUID, title: str, number: int, content: str) -> Chapter:
        chapter = Chapter(story_id=story_id, title=title, number=number, content=content)

        self.session.add(chapter)
        self.session.flush()

        return chapter


    def get_by_id(self, chapter_id: UUID) -> Chapter | None:
        return self.session.get(Chapter, chapter_id)


    def get_all_by_story_id(self, story_id: UUID) -> list[Chapter]:
        query = (
            select(Chapter)
            .where(Chapter.story_id == story_id)
            .order_by(Chapter.number.asc())
        )

        return list(self.session.scalars(query))


    def get_by_story_and_number(self, story_id: UUID, number: int) -> Chapter | None:
        query = select(Chapter).where(
            Chapter.story_id == story_id,
            Chapter.number == number,
        )

        return self.session.scalar(query)


    def delete(self, chapter: Chapter) -> None:
        self.session.delete(chapter)
