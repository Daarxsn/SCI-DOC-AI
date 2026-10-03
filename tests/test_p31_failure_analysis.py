from backend.evaluation.phase31 import classify_benchmark_result

def base_result():
    return {
        "execution_status": "EXECUTED",
        "accuracy_claim": True,
        "benchmark": {
            "metrics": [
                {"name": "ocr_cer_score", "value": 0.72, "threshold": 0.90, "passed": False},
                {"name": "translation_token_f1", "value": 0.91, "threshold": 0.80, "passed": True},
                {"name": "equation_exact", "value": 0.94, "threshold": 0.95, "passed": False},
            ],
            "metadata": {
                "validation_passed": False,
                "validation_issues": 2,
                "stage_status": {"ocr": "passed", "validation": "passed"},
            },
        },
    }

def test_phase31_classifies_failed_metrics():
    report = classify_benchmark_result(base_result())
    assert report["status"] == "ANALYZED"
    assert report["scientific_accuracy_claim"] is True
    assert report["category_counts"]["OCR"] == 1
    assert report["category_counts"]["MATHEMATICS"] == 1
    assert report["category_counts"]["VALIDATION"] == 1

def test_phase31_blocks_attribution_for_nonexecuted_result():
    result = {"execution_status": "BLOCKED", "accuracy_claim": False}
    report = classify_benchmark_result(result)
    assert report["attribution_allowed"] is False
    assert report["issues"][0]["code"] == "EXECUTION_BLOCKED"

def test_phase31_detects_stage_failure():
    result = base_result()
    result["benchmark"]["metadata"]["stage_status"]["translation"] = "failed"
    report = classify_benchmark_result(result)
    assert any(i["code"] == "TRANSLATION_STAGE_FAILED" for i in report["issues"])

def test_phase31_preserves_measured_values():
    report = classify_benchmark_result(base_result())
    ocr = next(i for i in report["issues"] if i["code"] == "OCR_BELOW_THRESHOLD")
    assert ocr["value"] == 0.72
    assert ocr["threshold"] == 0.90
