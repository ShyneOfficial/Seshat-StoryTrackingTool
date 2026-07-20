from dataclasses import asdict

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.api.dependencies import get_pipeline


router = APIRouter(prefix="/analysis", tags=["analysis"])


class AnalyzeRequest(BaseModel):
    chapter_id: str = Field(..., examples=["chapter_001"])
    text: str = Field(..., min_length=1)


@router.post("/run")
def run_analysis(request: AnalyzeRequest) -> dict:
    pipeline = get_pipeline()

    result = pipeline.analyze(
        text=request.text,
        chapter_id=request.chapter_id,
    )

    return asdict(result)
