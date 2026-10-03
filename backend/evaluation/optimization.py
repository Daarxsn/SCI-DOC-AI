from dataclasses import dataclass, field
from datetime import datetime, timezone

from backend.evaluation.models import BenchmarkReport
from backend.evaluation.regression import RegressionGate, RegressionResult


@dataclass(frozen=True)
class ProviderResult:
    provider: str
    report: BenchmarkReport


@dataclass
class OptimizationReport:
    run_id: str
    generated_at: str
    candidates: list[ProviderResult] = field(default_factory=list)
    regressions: list[RegressionResult] = field(default_factory=list)
    best_by_metric: dict[str, str] = field(default_factory=dict)
    quality_gate_passed: bool = True
    metadata: dict = field(default_factory=dict)


class OptimizationRunner:
    def __init__(self, regression_gate: RegressionGate | None = None):
        self.regression_gate = regression_gate or RegressionGate()

    def compare(self, run_id, candidates, *, baselines=None, metadata=None):
        baselines = baselines or {}
        metric_values = {}
        regressions = []
        for candidate in candidates:
            for metric in candidate.report.metrics:
                metric_values.setdefault(metric.name, []).append((candidate.provider, metric.value))
                if metric.name in baselines:
                    regressions.append(self.regression_gate.compare(
                        f"{candidate.provider}:{metric.name}", metric.value, baselines[metric.name]
                    ))
        best_by_metric = {
            name: max(values, key=lambda item: item[1])[0]
            for name, values in metric_values.items() if values
        }
        return OptimizationReport(
            run_id=run_id,
            generated_at=datetime.now(timezone.utc).isoformat(),
            candidates=candidates,
            regressions=regressions,
            best_by_metric=best_by_metric,
            quality_gate_passed=all(r.passed for r in regressions) and all(c.report.passed for c in candidates),
            metadata=metadata or {},
        )


def summarize_report(report: OptimizationReport) -> dict:
    return {
        "run_id": report.run_id,
        "generated_at": report.generated_at,
        "quality_gate_passed": report.quality_gate_passed,
        "best_by_metric": dict(sorted(report.best_by_metric.items())),
        "regressions": [
            {"metric": r.metric, "current": r.current, "baseline": r.baseline,
             "delta": r.delta, "passed": r.passed}
            for r in report.regressions
        ],
        "candidates": [
            {
                "provider": c.provider,
                "benchmark_id": c.report.benchmark_id,
                "task": c.report.task.value,
                "overall_score": c.report.overall_score,
                "passed": c.report.passed,
                "metrics": [
                    {"name": m.name, "value": m.value, "threshold": m.threshold,
                     "passed": m.passed, "sample_count": m.sample_count}
                    for m in c.report.metrics
                ],
            }
            for c in report.candidates
        ],
        "metadata": dict(sorted(report.metadata.items())),
    }
