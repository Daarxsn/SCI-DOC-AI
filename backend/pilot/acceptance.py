from dataclasses import dataclass, field
from datetime import datetime, timezone
from statistics import mean


@dataclass(frozen=True)
class PilotAcceptanceCriteria:
    max_processing_seconds: float | None = None
    max_failure_rate: float = 0.10
    max_review_rate: float = 0.50
    min_export_rate: float = 0.90
    min_ocr_score: float | None = None
    min_translation_score: float | None = None
    min_reconstruction_score: float | None = None


@dataclass
class PilotCaseEvidence:
    case_id: str
    processing_seconds: float
    failed: bool
    review_required: bool
    export_allowed: bool
    metrics: dict[str, float] = field(default_factory=dict)
    artifact_ids: list[str] = field(default_factory=list)
    failure_reason: str | None = None


@dataclass
class PilotReport:
    pilot_id: str
    tenant_id: str
    dataset_id: str
    dataset_version: str
    model_versions: dict[str, str]
    cases: list[PilotCaseEvidence]
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    criteria: PilotAcceptanceCriteria = field(default_factory=PilotAcceptanceCriteria)
    metadata: dict = field(default_factory=dict)

    @property
    def case_count(self) -> int:
        return len(self.cases)

    @property
    def failure_rate(self) -> float:
        return mean([1.0 if case.failed else 0.0 for case in self.cases]) if self.cases else 0.0

    @property
    def review_rate(self) -> float:
        return mean([1.0 if case.review_required else 0.0 for case in self.cases]) if self.cases else 0.0

    @property
    def export_rate(self) -> float:
        return mean([1.0 if case.export_allowed else 0.0 for case in self.cases]) if self.cases else 0.0

    @property
    def passed(self) -> bool:
        if not self.cases:
            return False
        if self.failure_rate > self.criteria.max_failure_rate:
            return False
        if self.review_rate > self.criteria.max_review_rate:
            return False
        if self.export_rate < self.criteria.min_export_rate:
            return False
        if self.criteria.max_processing_seconds is not None:
            if max(case.processing_seconds for case in self.cases) > self.criteria.max_processing_seconds:
                return False

        metric_requirements = {
            "ocr_score": self.criteria.min_ocr_score,
            "translation_score": self.criteria.min_translation_score,
            "reconstruction_score": self.criteria.min_reconstruction_score,
        }
        for metric_name, threshold in metric_requirements.items():
            if threshold is not None:
                values = [case.metrics[metric_name] for case in self.cases if metric_name in case.metrics]
                if not values or min(values) < threshold:
                    return False
        return True
