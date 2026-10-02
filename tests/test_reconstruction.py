from uuid import uuid4

from backend.reconstruction.text_fitter import TextFitter
from backend.reconstruction.udr_renderer import UdrRenderMapper
from backend.schemas.udr import (
    BoundingBox,
    DocumentSource,
    ElementType,
    UdrDocument,
    UdrElement,
    UdrPage,
)


def make_document():
    return UdrDocument(
        document_id=uuid4(),
        document_type="question_paper",
        source=DocumentSource(language="en", mime_type="application/pdf"),
        domain="physics",
        pages=[
            UdrPage(
                page_number=1,
                width=800,
                height=1000,
                elements=[
                    UdrElement(
                        id="q1",
                        type=ElementType.QUESTION,
                        bbox=BoundingBox(x=50, y=60, width=500, height=100),
                        source_text="Explain velocity.",
                        target_text="वेग समझाइए।",
                        confidence=0.95,
                    )
                ],
            )
        ],
    )


def test_udr_maps_translated_text():
    rendered = UdrRenderMapper().map(make_document())

    assert rendered.pages[0].elements[0].text == "वेग समझाइए।"
    assert rendered.pages[0].elements[0].source_text == "Explain velocity."


def test_text_fitter_reduces_font_when_required():
    result = TextFitter().fit(
        "A" * 500,
        box_width=100,
        box_height=40,
        base_font_size=12,
    )

    assert result.font_size < 12
