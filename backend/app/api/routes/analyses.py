from uuid import UUID
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, ConfigDict, model_validator
from fastapi import APIRouter, status

from app.api.errors import database_not_configured


router = APIRouter(tags=["analyses"])

class AnalysisStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REVIEWED = "reviewed"
    APPLIED = "applied"
    STALE = "stale"

class ProposalStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EDITED = "edited"
    APPLIED = "applied"

class ProposalDecision(str, Enum):
    ACCEPT = "accept"
    REJECT = "reject"
    EDIT = "edit"

class AnalysisResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    chapter_id: UUID
    chapter_revision: int
    status: AnalysisStatus

    result: dict[str, Any] | None = None
    warnings: dict[str, list[str]] = Field(default_factory=dict)
    errors: dict[str, list[str]] = Field(default_factory=dict)

    created_at: datetime
    completed_at: datetime | None = None
    applied_at: datetime | None = None

class AnalysisProposalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    analysis_id: UUID

    module_key: str
    object_kind: str
    operation: str

    payload: dict[str, Any]
    edited_payload: dict[str, Any] | None = None
    status: ProposalStatus

    created_at: datetime
    reviewed_at: datetime | None = None


class ProposalReviewRequest(BaseModel):
    decision: ProposalDecision
    edited_payload: dict[str, Any] | None = None

    @model_validator(mode="after")
    def validate_edited_payload(self) -> "ProposalReviewRequest":
        if self.decision == ProposalDecision.EDIT and self.edited_payload is None:
            raise ValueError("edited_payload is required when decision is 'edit'")

        if self.decision != ProposalDecision.EDIT and self.edited_payload is not None:
            raise ValueError("edited_payload can only be provided when decision is 'edit'")

        return self

@router.post("/chapters/{chapter_id}/analyses", response_model=AnalysisResult, status_code=status.HTTP_201_CREATED, summary="Analyze a saved chapter")
def create_chapter_analysis(chapter_id: UUID) -> AnalysisResult:
    database_not_configured("analysis")


@router.get("/analyses/{analysis_id}", response_model=AnalysisResult, summary="Get an analysis")
def get_analysis(analysis_id: UUID) -> AnalysisResult:
    database_not_configured("analysis")


@router.get("/analyses/{analysis_id}/proposals", response_model=list[AnalysisProposalRead], summary="List analysis proposals")
def list_analysis_proposals(analysis_id: UUID) -> list[AnalysisProposalRead]:
    database_not_configured("analysis proposal")


@router.patch("/analyses/{analysis_id}/proposals/{proposal_id}", response_model=AnalysisProposalRead, summary="Review an analysis proposal")
def review_analysis_proposal(analysis_id: UUID, proposal_id: UUID, request: ProposalReviewRequest) -> AnalysisProposalRead:
    database_not_configured("analysis proposal")


@router.post("/analyses/{analysis_id}/apply", response_model=AnalysisResult, summary="Apply accepted analysis proposals")
def apply_analysis(analysis_id: UUID) -> AnalysisResult:
    database_not_configured("analysis")
