from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Story


class StoryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session


    def create(self, title: str, description: str | None) -> Story:
        story = Story(title=title, description=description)

        self.session.add(story)
        self.session.flush()

        return story


    def get_by_id(self, story_id: UUID) -> Story | None:
        return self.session.get(Story, story_id)


    def get_all(self) -> list[Story]:
        query = select(Story).order_by(Story.created_at.desc())

        return list(self.session.scalars(query))


    def delete(self, story: Story) -> None:
        self.session.delete(story)
