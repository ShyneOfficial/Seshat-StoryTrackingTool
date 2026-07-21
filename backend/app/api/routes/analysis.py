from uuid import UUID

from fastapi import APIRouter, status

from app.api.errors import database_not_configured
from app.api.schemas import AnalysisRunResponse, AnalysisProposalResponse, ProposalReviewRequest


router = APIRouter(tags=["analysis"])


@router.post("/chapters/{chapter_id}/analysis", response_model=AnalysisRunResponse, status_code=status.HTTP_201_CREATED, summary="Analyze a saved chapter")
def create_chapter_analysis(chapter_id: UUID) -> AnalysisRunResponse:
    database_not_configured("analysis")


@router.get("/analysis/{analysis_id}", response_model=AnalysisRunResponse, summary="Get an analysis")
def get_analysis(analysis_id: UUID) -> AnalysisRunResponse:
    database_not_configured("analysis")


@router.get("/analysis/{analysis_id}/proposals", response_model=list[AnalysisProposalResponse], summary="List analysis proposals")
def list_analysis_proposals(analysis_id: UUID) -> list[AnalysisProposalResponse]:
    database_not_configured("analysis proposal")


@router.patch("/analysis/{analysis_id}/proposals/{proposal_id}", response_model=AnalysisProposalResponse, summary="Review an analysis proposal")
def review_analysis_proposal(analysis_id: UUID, proposal_id: UUID, request: ProposalReviewRequest) -> AnalysisProposalResponse:
    database_not_configured("analysis proposal")


@router.post("/analysis/{analysis_id}/apply", response_model=AnalysisRunResponse, summary="Apply accepted analysis proposals")
def apply_analysis(analysis_id: UUID) -> AnalysisRunResponse:
    database_not_configured("analysis")
