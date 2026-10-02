from enum import Enum
from pydantic import BaseModel, Field


class EvaluationTask(str, Enum):
    OCR = "ocr"
    LAYOUT = "layout"
    TRANSLATION = "translation"
    MATHEMATICS = "mathematics"
    DIAGRAM = "diagram"
    RECONSTRUCTION = "reconstruction"
    END_TO_END = "end_to_end"


class MetricResult(BaseModel):
    name: str
    value: float = Field(ge=0, le=1)
    threshold: float = Field(ge=0, le=1)
    passed: bool
    sample_count: int = Field(ge=0)
    details: dict = Field(default_factory=dict)


class BenchmarkCase(BaseModel):
    case_id: str
    domain: str
    source_language: str
    target_language: str | None = None
    input_path: str
    reference_path: str | None = None
    metadata: dict = Field(default_factory=dict)


class BenchmarkReport(BaseModel):
    benchmark_id: str
    task: EvaluationTask
    metrics: list[MetricResult] = Field(default_factory=list)
    overall_score: float = Field(ge=0, le=1)
    passed: bool
    metadata: dict = Field(default_factory=dict)
