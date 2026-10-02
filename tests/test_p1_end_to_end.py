from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image, ImageDraw

from backend.core.config import Settings
from backend.pipeline.end_to_end import ScientificDocumentPipeline


def test_p1_optional_runtime_path_is_configurable():
    config = Settings(
        ocr_provider="paddleocr",
        translation_provider="huggingface-nllb",
    )
    assert config.ocr_provider == "paddleocr"
    assert config.translation_provider == "huggingface-nllb"


def test_input_validation():
    config = Settings(ocr_provider="tesseract", translation_provider="rule-based-dev")
    try:
        ScientificDocumentPipeline(config).run("/definitely/missing/document.pdf")
    except FileNotFoundError:
        return
    raise AssertionError("Missing input should fail before the pipeline starts")
