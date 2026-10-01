from uuid import uuid4

import pytest
from pydantic import ValidationError

from backend.schemas.udr import (
    BoundingBox,
    DocumentSource,
    ElementType,
    UdrDocument,
    UdrElement,
    UdrPage,
)


def test_udr_document_accepts_scientific_elements():
    document = UdrDocument(
        document_id=uuid4(),
        document_type="question_paper",
        source=DocumentSource(language="en", mime_type="application/pdf"),
        domain="physics",
        pages=[
            UdrPage(
                page_number=1,
                width=1240,
                height=1754,
                elements=[
                    UdrElement(
                        id="q1",
                        type=ElementType.QUESTION,
                        text="Calculate the velocity.",
                        bbox=BoundingBox(x=10, y=20, width=300, height=80),
                        confidence=0.98,
                    ),
                    UdrElement(
                        id="eq1",
                        type=ElementType.EQUATION,
                        source_text="v = u + at",
                    ),
                ],
            )
        ],
    )

    assert document.pages[0].elements[1].type == ElementType.EQUATION
    assert document.pages[0].elements[0].confidence == 0.98


def test_udr_rejects_duplicate_page_numbers():
    with pytest.raises(ValidationError, match="unique"):
        UdrDocument(
            document_id=uuid4(),
            document_type="question_paper",
            source=DocumentSource(language="en", mime_type="application/pdf"),
            domain="physics",
            pages=[
                UdrPage(page_number=1, width=100, height=100),
                UdrPage(page_number=1, width=100, height=100),
            ],
        )
