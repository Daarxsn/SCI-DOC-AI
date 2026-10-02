from dataclasses import dataclass
from enum import Enum
from uuid import uuid4

class ReviewDecision(str, Enum):
    ACCEPT = "accept"
    EDIT = "edit"
    REJECT = "reject"

@dataclass
class ReviewItem:
    review_id: str
    element_id: str
    source_text: str
    machine_text: str | None
    proposed_text: str | None
    confidence: float | None
    reason: str

class TranslationReviewQueue:
    def __init__(self) -> None:
        self._items = {}

    def add(self, element_id, source_text, machine_text, confidence, reason):
        item = ReviewItem(str(uuid4()), element_id, source_text, machine_text, machine_text, confidence, reason)
        self._items[item.review_id] = item
        return item

    def get(self, review_id):
        return self._items.get(review_id)

    def decide(self, review_id, decision, edited_text=None):
        item = self._items[review_id]
        if decision == ReviewDecision.EDIT:
            if not edited_text:
                raise ValueError("edited_text is required for an edit decision")
            item.proposed_text = edited_text
        elif decision == ReviewDecision.ACCEPT:
            item.proposed_text = item.machine_text
        else:
            item.proposed_text = None
        return item

    def pending(self):
        return list(self._items.values())

class TranslationApprovalService:
    def __init__(self, memory, terminology) -> None:
        self.memory = memory
        self.terminology = terminology

    def approve_memory(self, item, *, source_language, target_language, domain, version="1"):
        if not item.proposed_text:
            raise ValueError("Cannot approve an empty translation")
        from backend.translation.memory import MemoryEntry
        self.memory.add(MemoryEntry(
            source_text=item.source_text,
            target_text=item.proposed_text,
            source_language=source_language,
            target_language=target_language,
            domain=domain,
            version=version,
        ))

    def approve_term(self, source_term, target_term, *, source_language, target_language, domain):
        from backend.translation.terminology import TerminologyEntry
        self.terminology.add(TerminologyEntry(
            source_term=source_term,
            target_term=target_term,
            source_language=source_language,
            target_language=target_language,
            domain=domain,
        ))
