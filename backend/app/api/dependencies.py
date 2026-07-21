from functools import lru_cache

from app.modules.entities import CharacterModule, LocationModule
from app.modules.links import VisitModule
from app.pipeline.nlp import NLPPipeline


@lru_cache
def get_nlp_pipeline() -> NLPPipeline:
    pipeline = NLPPipeline()

    ############################################################
    #####  Entity modules MUST execute before link modules #####
    ############################################################
    pipeline.add_module(CharacterModule())
    pipeline.add_module(LocationModule())

    pipeline.add_module(VisitModule())

    return pipeline
