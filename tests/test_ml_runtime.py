from backend.core.ml_runtime import runtime_status


def test_runtime_status_is_boolean_map():
    status = runtime_status()
    assert set(status) == {
        "paddleocr",
        "torch",
        "transformers",
        "sentencepiece",
        "pytesseract",
    }
    assert all(isinstance(value, bool) for value in status.values())
