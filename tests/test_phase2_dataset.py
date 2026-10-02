from backend.evaluation.dataset import DatasetValidator, coverage_summary
from backend.evaluation.models import BenchmarkCase, DatasetManifest, DatasetSplit

def test_manifest():
    case=BenchmarkCase(case_id="physics-hi-001",domain="physics",source_language="en",target_language="hi",split=DatasetSplit.TEST,input_path="assets/physics/page.png",reference_path="references/physics/page.json")
    manifest=DatasetManifest(dataset_id="sci-doc-golden",version="0.1.0",description="Initial scientific benchmark",cases=[case])
    assert DatasetValidator().validate(manifest)==[]
    assert coverage_summary(manifest)["by_domain"]["physics"]==1

def test_test_case_requires_reference():
    case=BenchmarkCase(case_id="biology-mr-001",domain="biology",source_language="en",target_language="mr",input_path="assets/biology/page.png")
    manifest=DatasetManifest(dataset_id="sci-doc-golden",version="0.1.0",description="Initial benchmark",cases=[case])
    assert any("requires reference_path" in e for e in DatasetValidator().validate(manifest))
