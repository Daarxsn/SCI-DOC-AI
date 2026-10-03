from enum import Enum

from pydantic import BaseModel, Field


class OutputFormat(str, Enum):
    PDF = "pdf"
    PNG = "png"


class RenderElement(BaseModel):
    element_id: str
    element_type: str
    x: float = Field(ge=0)
    y: float = Field(ge=0)
    width: float = Field(ge=0)
    height: float = Field(ge=0)
    text: str | None = None
    source_text: str | None = None
    confidence: float | None = Field(default=None, ge=0, le=1)
    metadata: dict = Field(default_factory=dict)


class RenderPage(BaseModel):
    page_number: int = Field(ge=1)
    width: float = Field(gt=0)
    height: float = Field(gt=0)
    elements: list[RenderElement] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)


class RenderDocument(BaseModel):
    document_id: str
    pages: list[RenderPage]
    output_format: OutputFormat = OutputFormat.PDF
    metadata: dict = Field(default_factory=dict)


class ReconstructionArtifact(BaseModel):
    document_id: str
    format: OutputFormat
    path: str
    size_bytes: int = Field(ge=0)
    sha256: str = Field(min_length=64, max_length=64)
    page_count: int = Field(ge=0)
    layout_warnings: int = Field(ge=0, default=0)
