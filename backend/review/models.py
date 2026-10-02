from enum import Enum
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class ReviewStatus(str, Enum):
    PENDING = "pending"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    SKIPPED = "skipped"


class ReviewDecision(str, Enum):
    ACCEPT = "accept"
    EDIT = "edit"
    REJECT = "reject"
    SKIP = "skip"


class ReviewPriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"


class ReviewItem(BaseModel):
    review_id: str
    document_id: str
    element_id: str
    source_text: str | None = None
    machine_text: str | None = None
    reviewed_text: str | None = None
    status: ReviewStatus = ReviewStatus.PENDING
    priority: ReviewPriority = ReviewPriority.NORMAL
    confidence: float | None = Field(default=None, ge=0, le=1)
    reason: str
    domain: str
    target_language: str
    assigned_to: str | None = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: dict = Field(default_factory=dict)


class ReviewAction(BaseModel):
    review_id: str
    reviewer: str
    decision: ReviewDecision
    edited_text: str | None = None
    comment: str | None = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ReviewWorkspace(BaseModel):
    document_id: str
    status: ReviewStatus
    total_items: int = 0
    pending_items: int = 0
    approved_items: int = 0
    rejected_items: int = 0
    skipped_items: int = 0
    items: list[ReviewItem] = Field(default_factory=list)
