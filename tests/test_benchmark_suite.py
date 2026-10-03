from backend.evaluation.benchmark_suite import BenchmarkSuite, OptimizationPlanner
from backend.evaluation.models import BenchmarkCase, DatasetManifest

def manifest():
    return DatasetManifest(dataset_id="sci-doc-golden", version="0.1.0", description="fixture", cases=[
        BenchmarkCase(case_id="physics-hi-001", domain="physics", source_language="en", target_language="hi", input_path="assets/physics/physics-hi-001.png")
    ])

def test_manifest_validation_does_not_claim_missing_assets_when_not_required(tmp_path):
    assert BenchmarkSuite().validate_manifest(manifest(), root=tmp_path) == []

def test_manifest_validation_detects_missing_assets_when_required(tmp_path):
    errors=BenchmarkSuite().validate_manifest(manifest(), root=tmp_path, require_assets=True)
    assert "missing input asset" in errors[0]

def test_provider_comparison_is_reproducible():
    run=BenchmarkSuite().compare_text_providers(run_id="run-001", manifest=manifest(),
        provider_predictions={"provider-a":["force"],"provider-b":["force mass"]}, references=["force"], task="translation")
    assert len(run.providers)==2
    assert run.providers[0].metrics[0].value==1.0
    assert run.providers[1].metrics[0].value<1.0

def test_optimization_planner_finds_quality_gap_and_regression():
    run=BenchmarkSuite().run_text_benchmark(run_id="run-002", manifest=manifest(), provider="provider-a",
        predictions=["force mass"], references=["force"], task="translation")
    report=OptimizationPlanner().plan(run, baselines={"translation_token_f1":0.9}, max_drop=0.02)
    assert report.primary_target() is not None
    assert report.regressions[0]["passed"] is False
    assert report.passed is False
