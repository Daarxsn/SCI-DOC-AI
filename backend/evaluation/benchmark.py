from backend.evaluation.metrics import bbox_iou, cer_score, exact_match, mean, token_f1
from backend.evaluation.models import BenchmarkReport, EvaluationTask, MetricResult


class BenchmarkRunner:
    def __init__(self, thresholds: dict[str, float] | None = None):
        self.thresholds = thresholds or {
            "ocr_cer": 0.90,
            "translation_token_f1": 0.80,
            "layout_iou": 0.85,
            "equation_exact": 0.95,
            "diagram_integrity": 0.95,
            "reconstruction_fidelity": 0.90,
        }

    def text_metric(self, name, predictions, references):
        values = [cer_score(p, r) if name == "ocr_cer" else token_f1(p, r) for p, r in zip(predictions, references)]
        value = mean(values)
        threshold = self.thresholds[name]
        return MetricResult(name=name, value=value, threshold=threshold, passed=value >= threshold, sample_count=len(values))

    def exact_metric(self, name, predictions, references):
        values = [exact_match(p, r) for p, r in zip(predictions, references)]
        value = mean(values)
        threshold = self.thresholds[name]
        return MetricResult(name=name, value=value, threshold=threshold, passed=value >= threshold, sample_count=len(values))

    def layout_metric(self, predictions, references):
        values = [bbox_iou(p, r) for p, r in zip(predictions, references)]
        value = mean(values)
        threshold = self.thresholds["layout_iou"]
        return MetricResult(name="layout_iou", value=value, threshold=threshold, passed=value >= threshold, sample_count=len(values))

    def report(self, benchmark_id, task, metrics, metadata=None):
        score = mean([m.value for m in metrics])
        return BenchmarkReport(
            benchmark_id=benchmark_id,
            task=task,
            metrics=metrics,
            overall_score=score,
            passed=all(m.passed for m in metrics),
            metadata=metadata or {},
        )
