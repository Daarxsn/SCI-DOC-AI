from backend.evaluation.benchmark import BenchmarkRunner
from backend.evaluation.golden import GoldenCase, GoldenDataset
from backend.evaluation.metrics import bbox_iou, cer_score, token_f1
from backend.evaluation.regression import RegressionGate

def test_text_metrics():
    assert cer_score("F = ma","F = ma")==1.0
    assert token_f1("force mass","force mass")==1.0

def test_bbox_iou():
    assert bbox_iou({"x":0,"y":0,"width":10,"height":10},{"x":0,"y":0,"width":10,"height":10})==1.0

def test_golden_dataset():
    dataset=GoldenDataset()
    dataset.add(GoldenCase("case-1","physics","en","hi","input.pdf","reference.pdf"))
    assert dataset.validate()==[]
    assert len(dataset.list("physics"))==1

def test_regression_gate():
    result=RegressionGate(max_drop=0.02).compare("translation",0.79,0.80)
    assert result.passed
    assert not RegressionGate(max_drop=0.02).compare("translation",0.77,0.80).passed

def test_benchmark_report():
    runner=BenchmarkRunner()
    metric=runner.text_metric("translation_token_f1",["force"],["force"])
    report=runner.report("b1","translation",[metric])
    assert report.passed
