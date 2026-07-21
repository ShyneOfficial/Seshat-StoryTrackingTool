from typing import Annotated
from functools import lru_cache

from fastapi import Depends

from app.pipeline.nlp import NLPPipeline
from app.pipeline.factory import create_nlp_pipeline


@lru_cache
def get_nlp_pipeline() -> NLPPipeline:
    return create_nlp_pipeline()

PipelineDependency = Annotated[
    NLPPipeline,
    Depends(get_nlp_pipeline),
]
