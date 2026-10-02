from uuid import uuid4

from backend.schemas.udr import (
    BoundingBox,
    DocumentSource,
    ElementType,
    UdrDocument,
    UdrElement,
    UdrPage,
)
from backend.validation.scientific_service import ScientificValidationService


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
                        bbox=BoundingBox(x=10, y=10, width=300, height=50),
                        source_text="What is force?",
                        metadata={"question_number": "1"},
                    ),
                    UdrElement(
                        id="eq1",
                        type=ElementType.EQUATION,
                        bbox=BoundingBox(x=10, y=80, width=300, height=50),
                        source_text="F = ma",
                        metadata={"latex": r"F = ma"},
                    ),
                ],
            )
        ],
    )


def test_valid_scientific_document_has_no_blocking_issues():
    report = ScientificValidationService().validate(make_document())
    assert report.passed
    assert report.export_allowed


def test_duplicate_question_is_blocking():
    document = make_document()
    document.pages[0].elements.append(
        UdrElement(
            id="q2",
            type=ElementType.QUESTION,
            source_text="Another question",
            metadata={"question_number": "1"},
        )
    )

    report = ScientificValidationService().validate(document)
    assert any(issue.code == "duplicate_question_number" for issue in report.issues)
    assert report.export_allowed is False


def test_broken_latex_is_blocking():
    document = make_document()
    document.pages[0].elements[1].metadata["latex"] = r"F = rac{ma"
    report = ScientificValidationService().validate(document)
    assert any(issue.code == "unbalanced_latex" for issue in report.issues)
    assert report.export_allowed is False
