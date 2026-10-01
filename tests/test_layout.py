from backend.layout.classifier import LayoutClassifier
from backend.ocr.models import OcrBlock
from backend.schemas.udr import ElementType


def block(text: str) -> OcrBlock:
    return OcrBlock(
        text=text,
        confidence=0.9,
        x=10,
        y=10,
        width=100,
        height=30,
        reading_order=0,
    )


def test_classifier_detects_equation():
    assert LayoutClassifier().classify(block("v = u + at")) == ElementType.EQUATION


def test_classifier_detects_option():
    assert LayoutClassifier().classify(block("A.")) == ElementType.OPTION


def test_classifier_defaults_to_paragraph():
    assert LayoutClassifier().classify(block("This is a scientific question.")) == ElementType.PARAGRAPH
