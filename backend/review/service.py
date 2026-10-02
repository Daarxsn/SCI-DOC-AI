from datetime import datetime, timezone

from backend.review.models import (
    ReviewAction,
    ReviewDecision,
    ReviewItem,
    ReviewPriority,
    ReviewStatus,
    ReviewWorkspace,
)


class ReviewService:
    def __init__(self) -> None:
        self._items: dict[str, ReviewItem] = {}
        self._actions: list[ReviewAction] = []

    def create_item(
        self,
        *,
        document_id: str,
        element_id: str,
        source_text: str | None,
        machine_text: str | None,
        confidence: float | None,
        reason: str,
        domain: str,
        target_language: str,
        priority: ReviewPriority = ReviewPriority.NORMAL,
        metadata: dict | None = None,
    ) -> ReviewItem:
        item = ReviewItem(
            review_id=f"review-{len(self._items) + 1}",
            document_id=document_id,
            element_id=element_id,
            source_text=source_text,
            machine_text=machine_text,
            confidence=confidence,
            reason=reason,
            domain=domain,
            target_language=target_language,
            priority=priority,
            metadata=metadata or {},
        )
        self._items[item.review_id] = item
        return item

    def get(self, review_id: str) -> ReviewItem | None:
        return self._items.get(review_id)

    def list(
        self,
        document_id: str | None = None,
        status: ReviewStatus | None = None,
        assigned_to: str | None = None,
    ) -> list[ReviewItem]:
        items = list(self._items.values())
        if document_id:
            items = [x for x in items if x.document_id == document_id]
        if status:
            items = [x for x in items if x.status == status]
        if assigned_to:
            items = [x for x in items if x.assigned_to == assigned_to]

        priority_order = {
            ReviewPriority.CRITICAL: 0,
            ReviewPriority.HIGH: 1,
            ReviewPriority.NORMAL: 2,
            ReviewPriority.LOW: 3,
        }
        return sorted(items, key=lambda x: (priority_order[x.priority], x.created_at))

    def assign(self, review_id: str, reviewer: str) -> ReviewItem:
        item = self._items[review_id]
        item.assigned_to = reviewer
        item.status = ReviewStatus.IN_REVIEW
        item.updated_at = datetime.now(timezone.utc).isoformat()
        return item

    def decide(
        self,
        review_id: str,
        reviewer: str,
        decision: ReviewDecision,
        edited_text: str | None = None,
        comment: str | None = None,
    ) -> ReviewItem:
        item = self._items[review_id]

        if decision == ReviewDecision.EDIT and not edited_text:
            raise ValueError("edited_text is required for an edit decision")

        if decision in {ReviewDecision.ACCEPT, ReviewDecision.EDIT}:
            item.reviewed_text = edited_text if decision == ReviewDecision.EDIT else item.machine_text
            item.status = ReviewStatus.APPROVED
        elif decision == ReviewDecision.REJECT:
            item.reviewed_text = None
            item.status = ReviewStatus.REJECTED
        elif decision == ReviewDecision.SKIP:
            item.status = ReviewStatus.SKIPPED

        item.updated_at = datetime.now(timezone.utc).isoformat()
        self._actions.append(
            ReviewAction(
                review_id=review_id,
                reviewer=reviewer,
                decision=decision,
                edited_text=edited_text,
                comment=comment,
            )
        )
        return item

    def actions(self, review_id: str | None = None) -> list[ReviewAction]:
        if review_id:
            return [x for x in self._actions if x.review_id == review_id]
        return list(self._actions)

    def workspace(self, document_id: str) -> ReviewWorkspace:
        items = self.list(document_id=document_id)
        counts = {status: sum(x.status == status for x in items) for status in ReviewStatus}
        if counts[ReviewStatus.REJECTED]:
            status = ReviewStatus.REJECTED
        elif counts[ReviewStatus.PENDING] or counts[ReviewStatus.IN_REVIEW]:
            status = ReviewStatus.IN_REVIEW
        elif items:
            status = ReviewStatus.APPROVED
        else:
            status = ReviewStatus.APPROVED

        return ReviewWorkspace(
            document_id=document_id,
            status=status,
            total_items=len(items),
            pending_items=counts[ReviewStatus.PENDING] + counts[ReviewStatus.IN_REVIEW],
            approved_items=counts[ReviewStatus.APPROVED],
            rejected_items=counts[ReviewStatus.REJECTED],
            skipped_items=counts[ReviewStatus.SKIPPED],
            items=items,
        )
