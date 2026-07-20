from abc import ABC, abstractmethod
from spacy.tokens import Doc

from app.pipeline.schemas import ModuleResult
from app.pipeline.context import PipelineContext


class SeshatModule(ABC):
    name: str
    version: str = "0.1.0"

    @abstractmethod
    def analyze(self, doc: Doc, context: PipelineContext) -> ModuleResult:
        pass
