from spacy.tokens import Doc

from app.modules import SeshatModule
from app.pipeline.schemas import LinkCandidate, LinkParticipant, ModuleResult
from app.pipeline.context import PipelineContext


class VisitModule(SeshatModule):
    name = "visits"

    def analyze(self, doc: Doc, context: PipelineContext) -> ModuleResult:
        characters = context.get_entities_by_type("character")
        locations = context.get_entities_by_type("location")

        visits: list[LinkCandidate] = []
        seen_visits: set[tuple[str, str, str]] = set()

        for character in characters:
            for location in locations:
                if character.sentence != location.sentence:
                    continue

                visit_key = (character.id, location.id, character.sentence)
                if visit_key in seen_visits:
                    continue

                seen_visits.add(visit_key)
                visit = LinkCandidate(
                    link_type="visit",
                    chapter_id=context.chapter_id,
                    sentence=character.sentence,
                    participants=[
                        LinkParticipant(entity_id=character.id, entity_type="character", role="visitor"),
                        LinkParticipant(entity_id=location.id, entity_type="location", role="visited_location"),
                    ],
                    confidence=0.5,
                )

                context.add_link(visit)
                visits.append(visit)

        return ModuleResult(module_name=self.name, data=visits)
