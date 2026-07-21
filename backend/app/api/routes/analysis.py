from dataclasses import asdict
from typing import Any

from pydantic import BaseModel, Field, field_validator
from fastapi import APIRouter, Depends

from app.api.dependencies import get_nlp_pipeline
from app.pipeline.nlp import NLPPipeline
from app.api.schemas import ChapterId


router = APIRouter(prefix="/analysis", tags=["analysis"])

class AnalysisRunRequest(BaseModel):
    chapter_id: ChapterId = Field(examples=["chapter_001"])
    text: str = Field(min_length=1, examples=["Owen entered the forest."])

    @field_validator("text")
    @staticmethod
    def validate_text(value: str) -> str:
        if not value.strip():
            raise ValueError("text must not be empty")

        return value


@router.post("/run", summary="Run the NLP pipeline")
def run_analysis(request: AnalysisRunRequest, pipeline: NLPPipeline = Depends(get_nlp_pipeline)) -> dict[str, Any]:
    result = pipeline.run(text=request.text, chapter_id=request.chapter_id)

    return asdict(result)
