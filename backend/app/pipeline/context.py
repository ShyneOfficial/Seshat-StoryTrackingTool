from dataclasses import dataclass, field

from app.pipeline.schemas import EntityMention, EntityType, LinkCandidate, LinkType


@dataclass
class PipelineContext:
    text: str
    chapter_id: str
    entities: list[EntityMention] = field(default_factory=list)
    links: list[LinkCandidate] = field(default_factory=list)


    def add_entity(self, entity: EntityMention) -> None:
        self.entities.append(entity)


    def add_link(self, link: LinkCandidate) -> None:
        self.links.append(link)

    def get_entities_by_type(self, entity_type: EntityType) -> list[EntityMention]:
        return [
            entity
            for entity in self.entities
            if entity.entity_type == entity_type
        ]

    def get_entities_in_sentence(self, sentence: str, entity_type: EntityType | None = None) -> list[EntityMention]:
        entities = self.entities

        if entity_type is None:
            return [
                entity
                for entity in entities
                if entity.sentence == sentence
            ]

        return [
            entity
            for entity in entities
            if entity.sentence == sentence
            and entity.entity_type == entity_type
        ]
    
    def get_links_by_type(self, link_type: LinkType) -> list[LinkCandidate]:
        return [
            link
            for link in self.links
            if link.link_type == link_type
        ]

    def get_links_in_sentence(self, sentence: str, link_type: LinkType | None = None) -> list[LinkCandidate]:
        links = self.links

        if link_type is None:
            return [
                link
                for link in links
                if link.sentence == sentence
            ]

        return [
            link
            for link in links
            if link.sentence == sentence
            and link.link_type == link_type
        ]
