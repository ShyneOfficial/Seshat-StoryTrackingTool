from spacy.tokens import Doc

from app.modules import SeshatModule
from app.schemas import EntityMention, ModuleResult
from app.pipeline.context import PipelineContext
from app.utils import make_entity_id


class CharacterModule(SeshatModule):
    name = "characters"

    def analyze(self, doc: Doc, context: PipelineContext) -> ModuleResult:
        found_characters: list[EntityMention] = []

        for ent in doc.ents:
            if ent.label_ != "PERSON":
                continue

            name = ent.text.strip()

            character = EntityMention(
                id=make_entity_id("character", name),
                name=name,
                entity_type="character",
                label=ent.label_,
                sentence=ent.sent.text.strip(),
                start_char=ent.start_char,
                end_char=ent.end_char,
                confidence=1.0,
            )

            context.add_entity(character)
            found_characters.append(character)

        return ModuleResult(module_name=self.name, data=found_characters)
