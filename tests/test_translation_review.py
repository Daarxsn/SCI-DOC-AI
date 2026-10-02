from backend.translation.memory import TranslationMemory
from backend.translation.review import ReviewDecision, TranslationApprovalService, TranslationReviewQueue
from backend.translation.terminology import TerminologyRegistry

def test_review_edit_can_be_approved_to_memory():
    queue = TranslationReviewQueue()
    memory = TranslationMemory()
    terminology = TerminologyRegistry()
    item = queue.add("q1", "force", "बल", 0.4, "low_translation_confidence")
    queue.decide(item.review_id, ReviewDecision.EDIT, "बल")
    TranslationApprovalService(memory, terminology).approve_memory(
        item,
        source_language="en",
        target_language="hi",
        domain="physics",
    )
    assert memory.lookup("force", "en", "hi", "physics").target_text == "बल"

def test_rejected_translation_is_not_added():
    queue = TranslationReviewQueue()
    memory = TranslationMemory()
    item = queue.add("q1", "force", "bad", 0.2, "low_translation_confidence")
    queue.decide(item.review_id, ReviewDecision.REJECT)
    assert item.proposed_text is None
