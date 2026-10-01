"""Universal Document Representation models.

M0 contract: stable, serializable models for document/page/element data.
"""

from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class ElementType(str, Enum):
    DOCUMENT = "document"
    PAGE = "page"
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    QUESTION = "question"
    SUBQUESTION = "subquestion"
    OPTION = "option"
    TABLE = "table"
    EQUATION = "equation"
    DIAGRAM = "diagram"
    GRAPH = "graph"
    IMAGE = "image"
    LABEL = "label"
    CAPTION = "caption"
    HEADER = "header"
    FOOTER = "footer"
    PAGE_NUMBER = "page_number"


class BoundingBox(BaseModel):
    x: float = Field(ge=0)
    y: float = Field(ge=0)
    width: float = Field(ge=0)
    height: float = Field(ge=0)


class Provenance(BaseModel):
    source_type: str
    source_id: str | None = None
    extractor: str | None = None
    extractor_version: str | None = None


class ValidationStatus(str, Enum):
    UNCHECKED = "unchecked"
    PASSED = "passed"
    WARNING = "warning"
    FAILED = "failed"


class ValidationResult(BaseModel):
    status: ValidationStatus = ValidationStatus.UNCHECKED
    checks: list[str] = Field(default_factory=list)
    messages: list[str] = Field(default_factory=list)


class UdrElement(BaseModel):
    id: str
    type: ElementType
    bbox: BoundingBox | None = None
    text: str | None = None
    source_text: str | None = None
    target_text: str | None = None
    confidence: float | None = Field(default=None, ge=0, le=1)
    provenance: Provenance | None = None
    model_version: str | None = None
    validation: ValidationResult = Field(default_factory=ValidationResult)
    children: list[str] = Field(default_factory=list)
    relationships: dict[str, list[str]] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class UdrPage(BaseModel):
    page_number: int = Field(ge=1)
    width: float = Field(ge=0)
    height: float = Field(ge=0)
    elements: list[UdrElement] = Field(default_factory=list)


class DocumentSource(BaseModel):
    language: str = Field(min_length=2, max_length=10)
    mime_type: str


class UdrDocument(BaseModel):
    schema_version: str = "0.1.0"
    document_id: UUID
    document_type: str
    source: DocumentSource
    domain: str
    pages: list[UdrPage] = Field(default_factory=list)

    @field_validator("pages")
    @classmethod
    def unique_page_numbers(cls, pages: list[UdrPage]) -> list[UdrPage]:
        numbers = [page.page_number for page in pages]
        if len(numbers) != len(set(numbers)):
            raise ValueError("page_number values must be unique")
        return pages
