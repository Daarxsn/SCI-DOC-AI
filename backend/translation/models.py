from enum import Enum

from pydantic import BaseModel, Field


class TranslationLanguage(str, Enum):
    ENGLISH = "en"
    HINDI = "hi"
    MARATHI = "mr"


class TranslationStatus(str, Enum):
    PENDING = "pending"
    TRANSLATED = "translated"
    SKIPPED = "skipped"
    REVIEW = "review"


class TranslationUnit(BaseModel):
    unit_id: str
    source_text: str
    target_text: str | None = None
    source_language: TranslationLanguage
    target_language: TranslationLanguage
    status: TranslationStatus = TranslationStatus.PENDING
    confidence: float | None = Field(default=None, ge=0, le=1)
    terminology_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, str] = Field(default_factory=dict)
