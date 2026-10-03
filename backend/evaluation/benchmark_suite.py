from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from backend.evaluation.benchmark import BenchmarkRunner
from backend.evaluation.models import DatasetManifest, MetricResult


@dataclass
class ProviderBenchmark:
    provider: str
    metrics: list[MetricResult] = field(default_factory=list)
    elapsed_seconds: float | None = None
    metadata: dict = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return all(metric.passed for metric in self.metrics)


@dataclass
class BenchmarkRun:
    run_id: str
    dataset_id: str
    dataset_version: str
    providers: list[ProviderBenchmark]
    started_at: str
    completed_at: str
    metadata: dict = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return bool(self.providers) and all(provider.passed for provider in self.providers)


class BenchmarkSuite:
    """Reproducible benchmark orchestration without inventing missing data."""

    def __init__(self, runner: BenchmarkRunner | None = None):
        self.runner = runner or BenchmarkRunner()

    def validate_manifest(
        self,
        manifest: DatasetManifest,
        *,
        root: str | Path | None = None,
        require_assets: bool = False,
    ) -> list[str]:
        errors = []
        base = Path(root) if root else None
        seen = set()
        for case in manifest.cases:
            if case.case_id in seen:
                errors.append(f"{case.case_id}: duplicate case_id")
            seen.add(case.case_id)
            if base:
                input_path = base / case.input_path
                if require_assets and not input_path.exists():
                    errors.append(f"{case.case_id}: missing input asset: {input_path}")
                for label, path in (("reference", case.reference_path), ("annotation", case.annotation_path)):
                    if require_assets and path and not (base / path).exists():
                        errors.append(f"{case.case_id}: missing {label} asset: {base / path}")
        return errors

    def run_text_benchmark(
        self,
        *,
        run_id: str,
        manifest: DatasetManifest,
        provider: str,
        predictions: list[str],
        references: list[str],
        task: str = "translation",
        metadata: dict | None = None,
    ) -> BenchmarkRun:
        if len(predictions) != len(references):
            raise ValueError("Predictions and references must have equal length")
        if not predictions:
            raise ValueError("At least one prediction/reference pair is required")
        started = datetime.now(timezone.utc)
        metric_name = "ocr_cer_score" if task == "ocr" else "translation_token_f1"
        metric = self.runner.text_metric(metric_name, predictions, references)
        provider_result = ProviderBenchmark(
            provider=provider,
            metrics=[metric],
            metadata={"task": task, **(metadata or {})},
        )
        completed = datetime.now(timezone.utc)
        return BenchmarkRun(
            run_id=run_id,
            dataset_id=manifest.dataset_id,
            dataset_version=manifest.version,
            providers=[provider_result],
            started_at=started.isoformat(),
            completed_at=completed.isoformat(),
            metadata={"case_count": len(predictions), "task": task},
        )

    def compare_text_providers(
        self,
        *,
        run_id: str,
        manifest: DatasetManifest,
        provider_predictions: dict[str, list[str]],
        references: list[str],
        task: str = "translation",
    ) -> BenchmarkRun:
        if not provider_predictions:
            raise ValueError("At least one provider is required")
        providers = []
        metric_name = "ocr_cer_score" if task == "ocr" else "translation_token_f1"
        for provider, predictions in provider_predictions.items():
            metric = self.runner.text_metric(metric_name, predictions, references)
            providers.append(ProviderBenchmark(provider=provider, metrics=[metric], metadata={"task": task}))
        now = datetime.now(timezone.utc).isoformat()
        return BenchmarkRun(
            run_id=run_id,
            dataset_id=manifest.dataset_id,
            dataset_version=manifest.version,
            providers=providers,
            started_at=now,
            completed_at=now,
            metadata={"case_count": len(references), "task": task},
        )


@dataclass(frozen=True)
class OptimizationTarget:
    provider: str
    metric: str
    value: float
    threshold: float
    gap_to_threshold: float
    reason: str


@dataclass
class OptimizationReport:
    run_id: str
    targets: list[OptimizationTarget]
    regressions: list[dict]
    metadata: dict = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return not any(item["passed"] is False for item in self.regressions)

    def primary_target(self) -> OptimizationTarget | None:
        return self.targets[0] if self.targets else None


class OptimizationPlanner:
    """Turns benchmark output into measurable optimization targets."""

    def plan(
        self,
        run: BenchmarkRun,
        *,
        baselines: dict[str, float] | None = None,
        max_drop: float = 0.02,
    ) -> OptimizationReport:
        targets = []
        regressions = []
        baselines = baselines or {}
        for provider in run.providers:
            for metric in provider.metrics:
                gap = metric.threshold - metric.value
                if gap > 0:
                    targets.append(OptimizationTarget(
                        provider=provider.provider,
                        metric=metric.name,
                        value=metric.value,
                        threshold=metric.threshold,
                        gap_to_threshold=gap,
                        reason="below configured quality threshold",
                    ))
                if metric.name in baselines:
                    baseline = baselines[metric.name]
                    delta = metric.value - baseline
                    regressions.append({
                        "provider": provider.provider,
                        "metric": metric.name,
                        "current": metric.value,
                        "baseline": baseline,
                        "delta": delta,
                        "allowed_drop": max_drop,
                        "passed": delta >= -max_drop,
                    })
        targets.sort(key=lambda item: item.gap_to_threshold, reverse=True)
        return OptimizationReport(
            run_id=run.run_id,
            targets=targets,
            regressions=regressions,
            metadata={"target_count": len(targets)},
        )
