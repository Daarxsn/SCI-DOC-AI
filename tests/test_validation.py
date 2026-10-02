from uuid import uuid4

from backend.schemas.udr import (
    DocumentSource,
    ElementType,
    UdrDocument,
    UdrElement,
    UdrPage,
)
from backend.validation.service import ValidationService
from backend.validation.models import ValidationSeverity
from backend.validation.review_gate import ReviewGate


def document_with_elements(elements):
    return UdrDocument(
        document_id=uuid4(),
        document_type="question_paper",
        source=DocumentSource(language="en", mime_type="application/pdf"),
        domain="physics",
        pages=[
            UdrPage(
                page_number=1,
                width=1000,
                height=1400,
                elements=elements,
            )
        ],
    )


def test_missing_equation_source_is_critical():
    element = UdrElement(
        id="eq1",
        type=ElementType.EQUATION,
        source_text=None,
    )

    report = ValidationService().validate(document_with_elements([element]))

    assert report.passed is False
    assert report.critical_issues == 1


def test_duplicate_questions_are_critical():
    elements = [
        UdrElement(
            id="q1",
            type=ElementType.QUESTION,
            source_text="Q1 Explain.",
            metadata={"question_number": 1},
        ),
        UdrElement(
            id="q2",
            type=ElementType.QUESTION,
            source_text="Q1 Explain again.",
            metadata={"question_number": 1},
        ),
    ]

    report = ValidationService().validate(document_with_elements(elements))

    assert any(
        issue.code == "DUPLICATE_QUESTION_NUMBER"
        and issue.severity == ValidationSeverity.CRITICAL
        for issue in report.issues
    )


def test_low_confidence_requires_review():
    element = UdrElement(
        id="p1",
        type=ElementType.PARAGRAPH,
        source_text="Scientific text",
        confidence=0.3,
    )

    report = ValidationService().validate(document_with_elements([element]))

    assert ReviewGate().requires_human_review(report)
    assert not ReviewGate().can_auto_export(report)
