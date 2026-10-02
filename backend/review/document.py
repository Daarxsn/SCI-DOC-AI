from backend.schemas.udr import UdrDocument
from backend.review.models import ReviewStatus
from backend.review.service import ReviewService


class ReviewDocumentService:
    """Apply approved reviewer edits back onto the UDR."""

    def __init__(self, reviews: ReviewService) -> None:
        self.reviews = reviews

    def apply_approved(self, document: UdrDocument) -> UdrDocument:
        result = document.model_copy(deep=True)

        for page in result.pages:
            for element in page.elements:
                review_id = element.metadata.get("review_id")
                if not review_id:
                    continue

                item = self.reviews.get(review_id)
                if not item or item.status != ReviewStatus.APPROVED:
                    continue

                if item.reviewed_text is not None:
                    element.target_text = item.reviewed_text
                    element.metadata["review_status"] = ReviewStatus.APPROVED.value
                    element.metadata["reviewer"] = item.assigned_to

        return result

    def unresolved(self, document: UdrDocument) -> list[str]:
        unresolved = []
        for page in document.pages:
            for element in page.elements:
                review_id = element.metadata.get("review_id")
                if not review_id:
                    continue
                item = self.reviews.get(review_id)
                if not item or item.status not in {ReviewStatus.APPROVED, ReviewStatus.SKIPPED}:
                    unresolved.append(review_id)
        return unresolved
