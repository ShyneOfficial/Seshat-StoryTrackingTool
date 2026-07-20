from app.modules.entities import CharacterModule, LocationModule
from app.modules.links import VisitModule
from app.pipeline.nlp import NLPPipeline


_pipeline: NLPPipeline | None = None


def get_pipeline() -> NLPPipeline:
    global _pipeline

    if _pipeline is None:
        _pipeline = NLPPipeline()
        _pipeline.add_module(CharacterModule())
        _pipeline.add_module(LocationModule())
        _pipeline.add_module(VisitModule())

    return _pipeline
