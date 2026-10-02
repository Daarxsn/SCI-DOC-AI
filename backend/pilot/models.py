from enum import Enum
from pydantic import BaseModel, Field

class PilotStage(str, Enum):
    INGESTION="ingestion"
    PREPROCESSING="preprocessing"
    OCR="ocr"
    TRANSLATION="translation"
    VALIDATION="validation"
    REVIEW="review"
    RECONSTRUCTION="reconstruction"
    COMPLETED="completed"
    FAILED="failed"

class PilotRun(BaseModel):
    run_id: str
    tenant_id: str
    document_id: str
    target_language: str
    domain: str
    stage: PilotStage = PilotStage.INGESTION
    progress: int = Field(default=0, ge=0, le=100)
    review_required: bool = False
    export_allowed: bool = False
    artifact_ids: list[str] = Field(default_factory=list)
    error: str | None = None
    metadata: dict = Field(default_factory=dict)
