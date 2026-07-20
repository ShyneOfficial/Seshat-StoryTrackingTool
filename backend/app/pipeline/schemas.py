from dataclasses import dataclass, field
from typing import Any, Literal


EntityType = Literal["character", "location"]
LinkType = Literal["visit"]


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


@dataclass
class LinkParticipant:
    entity_id: str
    entity_type: EntityType
    role: str


@dataclass
class LinkCandidate:
    link_type: LinkType
    chapter_id: str
    sentence: str
    participants: list[LinkParticipant] = field(default_factory=list)
    confidence: float = 0.5


@dataclass
class ModuleResult:
    module_name: str
    data: Any
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass
class AnalysisResult:
    chapter_id: str
    entities: list[EntityMention] = field(default_factory=list)
    links: list[LinkCandidate] = field(default_factory=list)
    warnings: dict[str, list[str]] = field(default_factory=dict)
    errors: dict[str, list[str]] = field(default_factory=dict)
