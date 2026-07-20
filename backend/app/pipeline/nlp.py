import spacy

from app.modules import SeshatModule
from app.pipeline.schemas import AnalysisResult
from app.pipeline.context import PipelineContext


class NLPPipeline:
    def __init__(self, model_name: str = "en_core_web_sm"):
        self.nlp = spacy.load(model_name)
        self.modules: list[SeshatModule] = []

    def add_module(self, module: SeshatModule) -> None:
        self.modules.append(module)

    def analyze(self, text: str, chapter_id: str) -> AnalysisResult:
        doc = self.nlp(text)

        context = PipelineContext(text=text, chapter_id=chapter_id)

        warnings: dict[str, list[str]] = {}
        errors: dict[str, list[str]] = {}

        for module in self.modules:
            module_result = module.analyze(doc, context)

            if module_result.warnings:
                warnings[module_result.module_name] = module_result.warnings

            if module_result.errors:
                errors[module_result.module_name] = module_result.errors

        return AnalysisResult(
            chapter_id=chapter_id,
            entities=context.entities,
            links=context.links,
            warnings=warnings,
            errors=errors,
        )
