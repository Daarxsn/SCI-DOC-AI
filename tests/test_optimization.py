from backend.evaluation.batch import BatchBenchmarkRunner, TextBenchmarkInput
from backend.evaluation.models import BenchmarkReport, EvaluationTask, MetricResult
from backend.evaluation.optimization import OptimizationRunner, ProviderResult, summarize_report


def report(provider, value):
    return ProviderResult(provider=provider, report=BenchmarkReport(
        benchmark_id=f"bench-{provider}", task=EvaluationTask.TRANSLATION,
        metrics=[MetricResult(name="translation_token_f1", value=value, threshold=0.80,
                              passed=value >= 0.80, sample_count=2)],
        overall_score=value, passed=value >= 0.80,
    ))


def test_batch_runner_preserves_case_ids():
    result = BatchBenchmarkRunner().text(
        benchmark_id="batch-1", task=EvaluationTask.TRANSLATION,
        metric_name="translation_token_f1",
        cases=[TextBenchmarkInput("c1", "force", "force"), TextBenchmarkInput("c2", "mass", "mass")],
    )
    assert result.passed
    assert result.metadata["case_ids"] == ["c1", "c2"]


def test_optimization_compares_candidates_and_baseline():
    result = OptimizationRunner().compare(
        "opt-1", [report("provider-a", 0.91), report("provider-b", 0.87)],
        baselines={"translation_token_f1": 0.90},
    )
    assert result.best_by_metric["translation_token_f1"] == "provider-a"
    assert result.quality_gate_passed is False
    assert len(result.regressions) == 2


def test_summary_is_machine_readable():
    result = OptimizationRunner().compare("opt-1", [report("provider-a", 0.91)])
    summary = summarize_report(result)
    assert summary["run_id"] == "opt-1"
    assert summary["candidates"][0]["provider"] == "provider-a"
