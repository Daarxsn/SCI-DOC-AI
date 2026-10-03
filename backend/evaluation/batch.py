from dataclasses import dataclass

from backend.evaluation.benchmark import BenchmarkRunner
from backend.evaluation.models import BenchmarkReport, EvaluationTask


@dataclass(frozen=True)
class TextBenchmarkInput:
    case_id: str
    prediction: str
    reference: str


class BatchBenchmarkRunner:
    def __init__(self, runner: BenchmarkRunner | None = None):
        self.runner = runner or BenchmarkRunner()

    def text(self, *, benchmark_id: str, task: EvaluationTask, metric_name: str,
             cases: list[TextBenchmarkInput], metadata: dict | None = None) -> BenchmarkReport:
        predictions = [c.prediction for c in cases]
        references = [c.reference for c in cases]
        if metric_name in {"ocr_cer_score", "translation_token_f1"}:
            metric = self.runner.text_metric(metric_name, predictions, references)
        else:
            metric = self.runner.exact_metric(metric_name, predictions, references)
        return self.runner.report(
            benchmark_id, task, [metric],
            metadata={**(metadata or {}), "case_ids": [c.case_id for c in cases]},
        )
