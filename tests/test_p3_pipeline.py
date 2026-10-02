from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image

from backend.core.config import Settings
from backend.ocr.models import OcrPageResult, OcrBlock
from backend.pipeline import end_to_end


class FakeOcr:
    def extract(self, path):
        return OcrPageResult(
            width=800,
            height=400,
            blocks=[OcrBlock(text="Force F = ma", confidence=0.99, x=20, y=20, width=200, height=30, words=[])],
            engine="fake",
            engine_version="test",
        )


class FakeEnrichment:
    def __init__(self, **kwargs):
        pass

    def apply(self, document, image_paths):
        return document


class FakeTranslation:
    def __init__(self, **kwargs):
        pass

    def translate_document(self, document, target):
        for page in document.pages:
            for element in page.elements:
                element.target_text = element.source_text
                element.text = element.source_text
        return document


class FakeValidation:
    def validate(self, document):
        class Report:
            export_allowed = True
            checked_elements = sum(len(p.elements) for p in document.pages)
        return Report()


def test_p3_real_document_orchestration(monkeypatch):
    monkeypatch.setattr(end_to_end, "create_ocr_adapter", lambda config: FakeOcr())
    monkeypatch.setattr(end_to_end, "ScientificEnrichment", FakeEnrichment)
    monkeypatch.setattr(end_to_end, "DocumentTranslationService", FakeTranslation)
    monkeypatch.setattr(end_to_end, "UnifiedValidationService", FakeValidation)

    with TemporaryDirectory() as tmp:
        source = Path(tmp) / "input.png"
        Image.new("RGB", (800, 400), "white").save(source)

        config = Settings(ocr_provider="tesseract", translation_provider="rule-based-dev")
        result = end_to_end.ScientificDocumentPipeline(config).run(
            source,
            target_language="hi",
            domain="physics",
        )

        assert result.stage_status == {
            "input": "passed",
            "preprocessing": "passed",
            "ocr": "passed",
            "udr": "passed",
            "scientific_enrichment": "passed",
            "translation": "passed",
            "validation": "passed",
            "reconstruction": "skipped",
        }
        assert result.document.pages
        assert result.validation.checked_elements == 1


def test_p3_detects_input_type():
    assert end_to_end.ScientificDocumentPipeline._mime_type(Path("paper.pdf")) == "application/pdf"
    assert end_to_end.ScientificDocumentPipeline._mime_type(Path("paper.jpg")) == "image/jpeg"
    assert end_to_end.ScientificDocumentPipeline._mime_type(Path("paper.png")) == "image/png"
