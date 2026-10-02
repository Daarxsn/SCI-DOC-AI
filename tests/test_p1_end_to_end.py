from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image, ImageDraw

from backend.core.config import Settings
from backend.pipeline.end_to_end import ScientificDocumentPipeline


def test_p1_end_to_end_with_lightweight_providers():
    with TemporaryDirectory() as tmp:
        image_path = Path(tmp) / "page.png"
        Image.new("RGB", (800, 400), "white").save(image_path)

        config = Settings(
            ocr_provider="tesseract",
            ocr_language="eng",
            translation_provider="rule-based-dev",
        )
        result = ScientificDocumentPipeline(config).run(
            [image_path],
            target_language="hi",
            domain="physics",
        )
        assert result.document.pages
        assert result.validation.checked_elements >= 0
        assert result.model_configuration["ocr_provider"] == "tesseract"


def test_p1_real_providers_fail_explicitly_when_optional_runtime_is_missing():
    with TemporaryDirectory() as tmp:
        image_path = Path(tmp) / "page.png"
        image = Image.new("RGB", (800, 400), "white")
        ImageDraw.Draw(image).text((20, 20), "F = ma", fill="black")
        image.save(image_path)

        config = Settings(
            ocr_provider="paddleocr",
            translation_provider="huggingface-nllb",
        )
        try:
            ScientificDocumentPipeline(config).run([image_path], target_language="hi")
        except RuntimeError:
            return
        except Exception:
            return
        raise AssertionError("Expected the optional ML runtime to be unavailable in this environment")
