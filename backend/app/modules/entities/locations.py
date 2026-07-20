from spacy.tokens import Doc

from app.modules import SeshatModule
from app.pipeline.schemas import EntityMention, ModuleResult
from app.pipeline.context import PipelineContext
from app.utils import make_entity_id


class LocationModule(SeshatModule):
    name = "locations"

    SPACY_LOCATION_LABELS = {
        "GPE", "LOC", "FAC"
    }

    LOCATION_KEYWORDS = {
        "forest", "river", "village",
        "city", "capital", "castle",
        "kingdom", "mountain", "cave",
        "temple", "tower", "room",
        "inn", "road", "lake",
        "sea", "island", "house",
        "palace", "camp"
    }


    def analyze(self, doc: Doc, context: PipelineContext) -> ModuleResult:
        found_locations: list[EntityMention] = []
        warnings: list[str] = []

        self._extract_spacy_locations(doc=doc, context=context, found_locations=found_locations)
        self._extract_keyword_locations(doc=doc, context=context, found_locations=found_locations)

        if found_locations:
            uncertain_count = sum(
                1
                for location in found_locations
                if location.label == "LOCATION_CANDIDATE"
            )

            if uncertain_count > 0:
                warnings.append(f"{uncertain_count} location(s) were detected using keyword rules.")

        return ModuleResult(module_name=self.name, data=found_locations, warnings=warnings)


    def _extract_spacy_locations(self, doc: Doc, context: PipelineContext, found_locations: list[EntityMention]) -> None:
        for ent in doc.ents:
            if ent.label_ not in self.SPACY_LOCATION_LABELS:
                continue

            name = ent.text.strip()
            location = EntityMention(
                id=make_entity_id("location", name),
                name=name,
                entity_type="location",
                label=ent.label_,
                sentence=ent.sent.text.strip(),
                start_char=ent.start_char,
                end_char=ent.end_char,
                confidence=1.0,
            )

            context.add_entity(location)
            found_locations.append(location)


    def _extract_keyword_locations(self, doc: Doc, context: PipelineContext, found_locations: list[EntityMention]) -> None:
        for token in doc:
            name = token.text.lower()

            if name not in self.LOCATION_KEYWORDS:
                continue

            location = EntityMention(
                id=make_entity_id("location", name),
                name=name,
                entity_type="location",
                label="LOCATION_CANDIDATE",
                sentence=token.sent.text.strip(),
                start_char=token.idx,
                end_char=token.idx + len(token.text),
                confidence=0.6,
            )

            context.add_entity(location)
            found_locations.append(location)
