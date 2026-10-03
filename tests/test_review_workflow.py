from uuid import uuid4

from backend.review.models import ReviewDecision, ReviewPriority, ReviewStatus
from backend.review.workflow import ReviewWorkflowService
from backend.schemas.udr import BoundingBox, DocumentSource, ElementType, UdrDocument, UdrElement, UdrPage
from backend.validation.unified import UnifiedValidationReport, UnifiedIssue


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
                        bbox=BoundingBox(x=20, y=20, width=400, height=80),
                        source_text="Explain force.",
                        target_text="बल बताइए।",
                        confidence=0.55,
                    )
                ],
            )
        ],
    )


def test_validation_finding_becomes_review_item():
    document = make_document()
    report = UnifiedValidationReport(
        document_id=str(document.document_id),
        issues=[UnifiedIssue("warning", "translation_warning", "q1", "Check translation", "translation")],
        checked_elements=1,
    )
    workflow = ReviewWorkflowService()
    items = workflow.create_from_validation(document, report, target_language="hi")
    assert len(items) == 1
    assert items[0].element_id == "q1"
    assert document.pages[0].elements[0].metadata["review_id"] == items[0].review_id


def test_approved_edit_is_applied_and_revalidated():
    document = make_document()
    workflow = ReviewWorkflowService()
    report = UnifiedValidationReport(
        document_id=str(document.document_id),
        issues=[UnifiedIssue("warning", "translation_warning", "q1", "Check translation", "translation")],
        checked_elements=1,
    )
    items = workflow.create_from_validation(document, report, target_language="hi")
    workflow.decide(items[0].review_id, "reviewer-1", ReviewDecision.EDIT, edited_text="बल को समझाइए।")
    run = workflow.apply_and_revalidate(document, target_language="hi")
    assert run.unresolved == []
    assert run.document.pages[0].elements[0].target_text == "बल को समझाइए।"


def test_unresolved_review_blocks_export():
    document = make_document()
    workflow = ReviewWorkflowService()
    report = UnifiedValidationReport(
        document_id=str(document.document_id),
        issues=[UnifiedIssue("error", "translation_error", "q1", "Translation error", "translation")],
        checked_elements=1,
    )
    items = workflow.create_from_validation(document, report, target_language="hi")
    run = workflow.apply_and_revalidate(document, target_language="hi")
    assert items[0].status == ReviewStatus.PENDING
    assert run.unresolved == [items[0].review_id]
    assert workflow.can_export(run) is False
