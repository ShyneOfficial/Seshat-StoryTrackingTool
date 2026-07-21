from uuid import UUID
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, ConfigDict, model_validator

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


class AnalysisRunResponse(BaseModel):
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


class AnalysisProposalResponse(BaseModel):
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
