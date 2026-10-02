from backend.review.models import ReviewDecision, ReviewPriority, ReviewStatus
from backend.review.service import ReviewService


def test_review_lifecycle():
    service = ReviewService()
    item = service.create_item(
        document_id="doc-1",
        element_id="q1",
        source_text="What is force?",
        machine_text="बल क्या है?",
        confidence=0.62,
        reason="low_translation_confidence",
        domain="physics",
        target_language="hi",
        priority=ReviewPriority.HIGH,
    )

    service.assign(item.review_id, "reviewer-1")
    updated = service.decide(
        item.review_id,
        "reviewer-1",
        ReviewDecision.EDIT,
        edited_text="बल क्या है?",
        comment="Verified terminology.",
    )

    assert updated.status == ReviewStatus.APPROVED
    assert updated.reviewed_text == "बल क्या है?"
    assert len(service.actions(item.review_id)) == 1


def test_workspace_counts():
    service = ReviewService()
    item = service.create_item(
        document_id="doc-1",
        element_id="q1",
        source_text="Q",
        machine_text="प्रश्न",
        confidence=0.4,
        reason="low_confidence",
        domain="biology",
        target_language="hi",
    )
    assert service.workspace("doc-1").pending_items == 1
    service.decide(item.review_id, "reviewer", ReviewDecision.ACCEPT)
    workspace = service.workspace("doc-1")
    assert workspace.approved_items == 1
    assert workspace.pending_items == 0
