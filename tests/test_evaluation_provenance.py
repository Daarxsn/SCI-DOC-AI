from backend.evaluation.provenance import build_provenance


def test_provenance_fingerprint_is_deterministic():
    kwargs = {
        "dataset_id": "sci-doc-golden",
        "dataset_version": "0.1.0",
        "provider": "nllb",
        "model_version": "facebook/nllb-200-distilled-600M",
        "configuration": {"device": "cpu", "batch_size": 4},
        "case_ids": ["case-2", "case-1"],
    }
    first = build_provenance(**kwargs).fingerprint()
    second = build_provenance(**kwargs).fingerprint()
    assert first == second
    assert len(first) == 64


def test_provenance_changes_when_model_changes():
    base = build_provenance(
        dataset_id="sci-doc-golden",
        dataset_version="0.1.0",
        provider="nllb",
        model_version="model-a",
        configuration={},
        case_ids=["case-1"],
    )
    changed = build_provenance(
        dataset_id="sci-doc-golden",
        dataset_version="0.1.0",
        provider="nllb",
        model_version="model-b",
        configuration={},
        case_ids=["case-1"],
    )
    assert base.fingerprint() != changed.fingerprint()
