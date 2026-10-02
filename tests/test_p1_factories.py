from backend.core.config import Settings
from backend.ocr.factory import create_ocr_adapter
from backend.ocr.tesseract_adapter import TesseractAdapter
from backend.translation.factory import create_translation_adapter
from backend.translation.rule_based_adapter import RuleBasedAdapter


def test_default_ocr_factory_uses_tesseract():
    config = Settings(ocr_provider="tesseract", ocr_language="eng")
    adapter = create_ocr_adapter(config)
    assert isinstance(adapter, TesseractAdapter)


def test_paddle_ocr_factory_is_lazy():
    config = Settings(ocr_provider="paddleocr", ocr_language="en")
    adapter = create_ocr_adapter(config)
    assert adapter.name == "paddleocr"


def test_default_translation_factory_uses_dev_adapter():
    config = Settings(translation_provider="rule-based-dev")
    adapter = create_translation_adapter(config)
    assert isinstance(adapter, RuleBasedAdapter)


def test_nllb_factory_is_lazy():
    config = Settings(
        translation_provider="huggingface-nllb",
        translation_model="facebook/nllb-200-distilled-600M",
    )
    adapter = create_translation_adapter(config)
    assert adapter.name == "huggingface-nllb"
