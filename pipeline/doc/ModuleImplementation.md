# Seshat — Module Implementation Guide

> This document explains how to implement new **Entity Modules** and **Link Modules** in the Seshat NLP pipeline.

The current pipeline is built around a simple idea:

```txt
Raw chapter text
↓
spaCy Doc
↓
Entity modules
↓
Link modules
↓
AnalysisResult
```

Modules should only analyze text and produce structured analysis data. They should **not** save anything to the database directly.

---

# 1. Module Types

Seshat currently has two main kinds of modules:

```txt
Entity Modules
Link Modules
```

## Entity Modules

Entity modules detect things that exist in the story.

Examples:

```txt
characters
locations
items
skills
factions
quests
```

Current entity modules:

```txt
CharacterModule
LocationModule
```

Entity modules produce:

```python
EntityMention
```

## Link Modules

Link modules detect relationships between entities.

Examples:

```txt
character visits location
character owns item
character knows character
character uses skill
character belongs to faction
```

Current link module:

```txt
VisitModule
```

Link modules produce:

```python
LinkCandidate
```

---

# 2. Current Schema Overview

The analysis data structures are defined in:

```txt
app/schemas/analysis.py
```

## EntityType

```python
EntityType = Literal["character", "location"]
```

This defines which entity categories are currently supported.

When adding a new entity module, update this type.

Example:

```python
EntityType = Literal["character", "location", "item"]
```

## LinkType

```python
LinkType = Literal["visit"]
```

This defines which link categories are currently supported.

When adding a new link module, update this type.

Example:

```python
LinkType = Literal["visit", "ownership"]
```

## EntityMention

```python
@dataclass
class EntityMention:
    id: str
    name: str
    entity_type: EntityType
    label: str
    sentence: str
    start_char: int
    end_char: int
    confidence: float = 0.5
```

An `EntityMention` represents **one detected mention** of an entity in a chapter.

Important: this is not the final database entity.

If Owen appears 5 times, the analysis result may contain 5 `EntityMention` objects with the same ID. The database/data-management layer will later deduplicate them into one persistent entity.

## LinkParticipant

```python
@dataclass
class LinkParticipant:
    entity_id: str
    entity_type: EntityType
    role: str
```

A `LinkParticipant` represents one entity involved in a link.

Example:

```python
LinkParticipant(
    entity_id="character_9f67abfaa618",
    entity_type="character",
    role="visitor",
)
```

The `role` field explains what the entity does inside the link.

## LinkCandidate

```python
@dataclass
class LinkCandidate:
    link_type: LinkType
    chapter_id: str
    sentence: str
    participants: list[LinkParticipant] = field(default_factory=list)
    confidence: float = 0.5
```

A `LinkCandidate` represents a possible relationship found in the text.

Example sentence:

```txt
Owen entered the forest.
```

Possible link:

```python
LinkCandidate(
    link_type="visit",
    chapter_id="chapter_001",
    sentence="Owen entered the forest.",
    participants=[
        LinkParticipant(
            entity_id="character_9f67abfaa618",
            entity_type="character",
            role="visitor",
        ),
        LinkParticipant(
            entity_id="location_3a4064184f71",
            entity_type="location",
            role="visited_location",
        ),
    ],
    confidence=0.5,
)
```

---

# 3. Module Contract

All modules inherit from:

```txt
app/modules/base.py
```

```python
class SeshatModule(ABC):
    name: str
    version: str = "0.1.0"

    @abstractmethod
    def analyze(self, doc: Doc, context: PipelineContext) -> ModuleResult:
        pass
```

Every module must implement:

```python
def analyze(self, doc: Doc, context: PipelineContext) -> ModuleResult:
```

## Parameters

### `doc`

A spaCy `Doc`.

It contains:

```txt
tokens
sentences
entities
lemmas
POS tags
dependency information
```

### `context`

A `PipelineContext`.

It stores temporary analysis data for the current chapter:

```python
context.text
context.chapter_id
context.entities
context.links
```

It also provides helper methods:

```python
context.add_entity(entity)
context.add_link(link)
context.get_entities_by_type("character")
context.get_entities_in_sentence(sentence)
context.get_links_by_type("visit")
```

---

# 4. Entity Module Implementation

An entity module should:

```txt
1. Analyze the spaCy Doc.
2. Detect one type of entity.
3. Create EntityMention objects.
4. Add them to PipelineContext.
5. Return a ModuleResult.
```

## Entity Module Template

```python
from spacy.tokens import Doc

from app.modules.base import SeshatModule
from app.pipeline.context import PipelineContext
from app.schemas import EntityMention, ModuleResult
from app.utils import make_entity_id


class ExampleEntityModule(SeshatModule):
    name = "example_entities"

    def analyze(self, doc: Doc, context: PipelineContext) -> ModuleResult:
        found_entities: list[EntityMention] = []
        warnings: list[str] = []
        errors: list[str] = []

        for ent in doc.ents:
            # Replace this condition with your own extraction rule.
            if ent.label_ != "SOME_LABEL":
                continue

            entity_name = ent.text.strip()

            entity = EntityMention(
                id=make_entity_id("example", entity_name),
                name=entity_name,
                entity_type="example",
                label=ent.label_,
                sentence=ent.sent.text.strip(),
                start_char=ent.start_char,
                end_char=ent.end_char,
                confidence=1.0,
            )

            context.add_entity(entity)
            found_entities.append(entity)

        return ModuleResult(
            module_name=self.name,
            data=found_entities,
            warnings=warnings,
            errors=errors,
        )
```

---

# 5. Existing Entity Modules

## CharacterModule

Path:

```txt
app/modules/entities/characters.py
```

Purpose:

```txt
Detect character mentions.
```

Current rule:

```python
ent.label_ == "PERSON"
```

Output:

```python
EntityMention(
    entity_type="character",
    label="PERSON",
    confidence=1.0,
)
```

This means character detection currently depends on spaCy named entity recognition.

## LocationModule

Path:

```txt
app/modules/entities/locations.py
```

Purpose:

```txt
Detect location mentions.
```

Current rules:

```txt
1. spaCy labels: GPE, LOC, FAC
2. Keyword rules: forest, river, city, castle, etc.
```

spaCy locations receive:

```python
confidence=1.0
```

Keyword locations receive:

```python
confidence=0.6
```

Keyword-based locations are labeled:

```txt
LOCATION_CANDIDATE
```

This allows the future validation/database layer to treat them as uncertain.

---

# 6. Adding a New Entity Module

Example: `ItemModule`

## Step 1 — Update EntityType

In:

```txt
app/schemas/analysis.py
```

Change:

```python
EntityType = Literal["character", "location"]
```

to:

```python
EntityType = Literal["character", "location", "item"]
```

## Step 2 — Create the module file

Create:

```txt
app/modules/entities/items.py
```

Example:

```python
from spacy.tokens import Doc

from app.modules.base import SeshatModule
from app.pipeline.context import PipelineContext
from app.schemas import EntityMention, ModuleResult
from app.utils import make_entity_id


class ItemModule(SeshatModule):
    name = "items"

    ITEM_KEYWORDS = {
        "sword",
        "dagger",
        "shield",
        "ring",
        "book",
        "potion",
        "amulet",
    }

    def analyze(self, doc: Doc, context: PipelineContext) -> ModuleResult:
        found_items: list[EntityMention] = []
        warnings: list[str] = []

        for token in doc:
            item_name = token.text.lower()

            if item_name not in self.ITEM_KEYWORDS:
                continue

            item = EntityMention(
                id=make_entity_id("item", item_name),
                name=item_name,
                entity_type="item",
                label="ITEM_CANDIDATE",
                sentence=token.sent.text.strip(),
                start_char=token.idx,
                end_char=token.idx + len(token.text),
                confidence=0.6,
            )

            context.add_entity(item)
            found_items.append(item)

        if found_items:
            warnings.append(
                f"{len(found_items)} item(s) were detected using keyword rules."
            )

        return ModuleResult(
            module_name=self.name,
            data=found_items,
            warnings=warnings,
        )
```

## Step 3 — Export the module

Update:

```txt
app/modules/entities/__init__.py
```

```python
from app.modules.entities.characters import CharacterModule
from app.modules.entities.locations import LocationModule
from app.modules.entities.items import ItemModule


__all__ = [
    "CharacterModule",
    "LocationModule",
    "ItemModule",
]
```

## Step 4 — Register it in the pipeline

In:

```txt
app/main.py
```

```python
from app.modules.entities import CharacterModule, LocationModule, ItemModule
```

Then:

```python
pipeline.add_module(CharacterModule())
pipeline.add_module(LocationModule())
pipeline.add_module(ItemModule())
pipeline.add_module(VisitModule())
```

Entity modules should usually run before link modules.

---

# 7. Link Module Implementation

A link module should:

```txt
1. Read existing entities from PipelineContext.
2. Detect relationships between them.
3. Create LinkCandidate objects.
4. Add them to PipelineContext.
5. Return a ModuleResult.
```

Link modules usually depend on entity modules running first.

## Link Module Template

```python
from spacy.tokens import Doc

from app.modules.base import SeshatModule
from app.pipeline.context import PipelineContext
from app.schemas import LinkCandidate, LinkParticipant, ModuleResult


class ExampleLinkModule(SeshatModule):
    name = "example_links"

    def analyze(self, doc: Doc, context: PipelineContext) -> ModuleResult:
        links: list[LinkCandidate] = []

        source_entities = context.get_entities_by_type("source_type")
        target_entities = context.get_entities_by_type("target_type")

        for source in source_entities:
            for target in target_entities:
                if source.sentence != target.sentence:
                    continue

                link = LinkCandidate(
                    link_type="example_link",
                    chapter_id=context.chapter_id,
                    sentence=source.sentence,
                    participants=[
                        LinkParticipant(
                            entity_id=source.id,
                            entity_type=source.entity_type,
                            role="source_role",
                        ),
                        LinkParticipant(
                            entity_id=target.id,
                            entity_type=target.entity_type,
                            role="target_role",
                        ),
                    ],
                    confidence=0.5,
                )

                context.add_link(link)
                links.append(link)

        return ModuleResult(
            module_name=self.name,
            data=links,
        )
```

---

# 8. Existing Link Module

## VisitModule

Path:

```txt
app/modules/links/visits.py
```

Purpose:

```txt
Detect simple character-location visit links.
```

Current rule:

```txt
If a character and a location appear in the same sentence, create a visit link.
```

Example:

```txt
Owen woke up in the forest.
```

Produces:

```txt
Owen → visited_location → forest
```

Participant roles:

```txt
visitor
visited_location
```

Current confidence:

```python
confidence=0.5
```

This low confidence is intentional because same-sentence matching can produce false positives.

---

# 9. Adding a New Link Module

Example: `OwnershipModule`

## Step 1 — Update LinkType

In:

```txt
app/schemas/analysis.py
```

Change:

```python
LinkType = Literal["visit"]
```

to:

```python
LinkType = Literal["visit", "ownership"]
```

## Step 2 — Create the module file

Create:

```txt
app/modules/links/ownerships.py
```

Example:

```python
from spacy.tokens import Doc

from app.modules.base import SeshatModule
from app.pipeline.context import PipelineContext
from app.schemas import LinkCandidate, LinkParticipant, ModuleResult


class OwnershipModule(SeshatModule):
    name = "ownerships"

    OWNERSHIP_VERBS = {
        "hold",
        "holds",
        "held",
        "carry",
        "carries",
        "carried",
        "own",
        "owns",
        "owned",
        "take",
        "takes",
        "took",
    }

    def analyze(self, doc: Doc, context: PipelineContext) -> ModuleResult:
        links: list[LinkCandidate] = []

        characters = context.get_entities_by_type("character")
        items = context.get_entities_by_type("item")

        for character in characters:
            for item in items:
                if character.sentence != item.sentence:
                    continue

                if not self._sentence_has_ownership_verb(character.sentence):
                    continue

                link = LinkCandidate(
                    link_type="ownership",
                    chapter_id=context.chapter_id,
                    sentence=character.sentence,
                    participants=[
                        LinkParticipant(
                            entity_id=character.id,
                            entity_type="character",
                            role="owner",
                        ),
                        LinkParticipant(
                            entity_id=item.id,
                            entity_type="item",
                            role="owned_item",
                        ),
                    ],
                    confidence=0.6,
                )

                context.add_link(link)
                links.append(link)

        return ModuleResult(
            module_name=self.name,
            data=links,
        )

    def _sentence_has_ownership_verb(self, sentence: str) -> bool:
        words = {
            word.strip(".,!?;:").lower()
            for word in sentence.split()
        }

        return any(
            verb in words
            for verb in self.OWNERSHIP_VERBS
        )
```

## Step 3 — Export the module

Update:

```txt
app/modules/links/__init__.py
```

```python
from app.modules.links.visits import VisitModule
from app.modules.links.ownerships import OwnershipModule


__all__ = [
    "VisitModule",
    "OwnershipModule",
]
```

## Step 4 — Register it in the pipeline

In:

```txt
app/main.py
```

```python
from app.modules.links import VisitModule, OwnershipModule
```

Then:

```python
pipeline.add_module(CharacterModule())
pipeline.add_module(LocationModule())
pipeline.add_module(ItemModule())
pipeline.add_module(VisitModule())
pipeline.add_module(OwnershipModule())
```

---

# 10. Module Ordering

Module order matters.

Entity modules should run before link modules:

```python
pipeline.add_module(CharacterModule())
pipeline.add_module(LocationModule())
pipeline.add_module(ItemModule())

pipeline.add_module(VisitModule())
pipeline.add_module(OwnershipModule())
```

Bad order:

```python
pipeline.add_module(VisitModule())
pipeline.add_module(CharacterModule())
pipeline.add_module(LocationModule())
```

This would fail logically because `VisitModule` needs character and location mentions to already exist in the context.

---

# 11. IDs

IDs are created with:

```python
make_entity_id(entity_type, name)
```

Defined in:

```txt
app/utils/ids.py
```

Example:

```python
make_entity_id("character", "Owen Androm")
```

The same entity type and normalized name should always produce the same ID.

This is useful because:

```txt
Owen Androm
```

will always map to the same character ID.

However:

```txt
Owen
Owen Androm
the tactician
```

will currently produce different IDs.

Alias resolution is not implemented yet.

---

# 12. Confidence Scores

Confidence scores indicate how reliable a detection is.

Suggested values:

```txt
1.0 = strong detection
0.7 = likely detection
0.5 = uncertain rule-based link
0.3 = weak candidate
```

Examples:

```txt
spaCy PERSON entity → 1.0
spaCy GPE/LOC/FAC entity → 1.0
keyword location → 0.6
same-sentence visit link → 0.5
```

The future database manager can use confidence scores to decide whether to save, ignore, or request validation.

---

# 13. Warnings and Errors

Modules can return warnings and errors through `ModuleResult`.

Example:

```python
return ModuleResult(
    module_name=self.name,
    data=found_locations,
    warnings=[
        "2 location(s) were detected using keyword rules."
    ],
)
```

Warnings are useful when the result is valid but uncertain.

Errors are useful when the module failed to analyze something.

A module should generally avoid crashing the whole pipeline unless the error is critical.

---

# 14. Best Practices

## Keep modules focused

A module should do one job.

Good:

```txt
CharacterModule detects characters.
LocationModule detects locations.
VisitModule detects visits.
```

Bad:

```txt
CharacterModule detects characters, locations, visits, and writes to database.
```

## Do not write to the database inside modules

Modules should only create analysis data.

Correct:

```python
context.add_entity(entity)
context.add_link(link)
```

Incorrect:

```python
database.save_entity(entity)
```

Database saving belongs in the data-management layer.

## Entity modules should not depend on link modules

Entity modules should only detect entities.

Link modules may depend on entity modules because they need entities to already exist in the context.

## Avoid duplicate links

When a link module creates links, it should avoid duplicates.

Example:

```python
seen_links: set[tuple[str, str, str]] = set()
```

Use a stable key such as:

```python
(character.id, location.id, sentence)
```

---

# 15. Current Limitations

The current module system is intentionally simple.

Known limitations:

```txt
No alias resolution
No coreference resolution
No database persistence yet
No validation UI yet
No movement verb detection yet
No dependency-based link extraction yet
```

Example problem:

```txt
Owen left the forest while Loki entered Arcadia.
```

A same-sentence visit module may incorrectly link both characters to both locations.

This will be improved later with more advanced grammar rules.

---

# 16. Recommended Development Flow

When adding a module:

```txt
1. Decide whether it detects an entity or a link.
2. Update EntityType or LinkType if needed.
3. Create the module file.
4. Add module exports in __init__.py.
5. Register the module in main.py.
6. Test on a small input file.
7. Check the AnalysisResult output.
8. Add warnings for uncertain detections.
```

The goal is not perfect accuracy at first.

The goal is to keep modules independent, testable, and easy to replace later.