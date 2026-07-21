from uuid import UUID

from sqlalchemy.orm import Session

from app.api.schemas import StoryCreateRequest, StoryUpdateRequest
from app.db.models.story import Story
from app.repositories.story_repository import StoryRepository


class StoryNotFoundError(Exception):
    pass


class StoryService:
    def __init__(self, session: Session, repository: StoryRepository) -> None:
        self.session = session
        self.repository = repository


    def create_story(self, data: StoryCreateRequest) -> Story:
        story = self.repository.create(title=data.title, description=data.description)

        self.session.commit()
        self.session.refresh(story)

        return story


    def list_stories(self) -> list[Story]:
        return self.repository.get_all()


    def get_story(self, story_id: UUID) -> Story:
        story = self.repository.get_by_id(story_id)

        if story is None:
            raise StoryNotFoundError(story_id)

        return story


    def update_story(self, story_id: UUID, data: StoryUpdateRequest) -> Story:
        story = self.get_story(story_id)

        changes = data.model_dump(exclude_unset=True)

        for field, value in changes.items():
            setattr(story, field, value)

        self.session.commit()
        self.session.refresh(story)

        return story


    def delete_story(self, story_id: UUID) -> None:
        story = self.get_story(story_id)

        self.repository.delete(story)
        self.session.commit()
