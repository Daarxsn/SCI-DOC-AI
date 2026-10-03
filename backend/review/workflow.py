from dataclasses import dataclass

from backend.review.document import ReviewDocumentService
from backend.review.models import ReviewDecision, ReviewItem, ReviewPriority, ReviewStatus
from backend.review.service import ReviewService
from backend.validation.unified import UnifiedValidationReport, UnifiedValidationService


@dataclass
class ReviewRun:
    document: object
    validation: UnifiedValidationReport
    workspace: object
    unresolved: list[str]


class ReviewWorkflowService:
    """Canonical human-review workflow for validation findings."""

    def __init__(
        self,
        reviews: ReviewService | None = None,
        validator: UnifiedValidationService | None = None,
    ):
        self.reviews = reviews or ReviewService()
        self.validator = validator or UnifiedValidationService()
        self.document_service = ReviewDocumentService(self.reviews)

    def create_from_validation(
        self,
        document,
        report: UnifiedValidationReport,
        *,
        target_language: str,
        default_priority: ReviewPriority = ReviewPriority.NORMAL,
    ) -> list[ReviewItem]:
        created = []
        for issue in report.issues:
            if issue.severity not in {"critical", "error", "warning"}:
                continue
            if not issue.element_id:
                continue

            element = self._find_element(document, issue.element_id)
            if element is None:
                continue

            priority = (
                ReviewPriority.CRITICAL
                if issue.severity == "critical"
                else ReviewPriority.HIGH
                if issue.severity == "error"
                else default_priority
            )
            item = self.reviews.create_item(
                document_id=str(document.document_id),
                element_id=issue.element_id,
                source_text=element.source_text,
                machine_text=element.target_text,
                confidence=element.confidence,
                reason=f"{issue.stage}:{issue.code} — {issue.message}",
                domain=document.domain,
                target_language=target_language,
                priority=priority,
                metadata={"validation_code": issue.code, "validation_stage": issue.stage},
            )
            element.metadata["review_id"] = item.review_id
            created.append(item)

        return created

    def decide(
        self,
        review_id: str,
        reviewer: str,
        decision: ReviewDecision,
        *,
        edited_text: str | None = None,
        comment: str | None = None,
    ) -> ReviewItem:
        return self.reviews.decide(
            review_id,
            reviewer,
            decision,
            edited_text=edited_text,
            comment=comment,
        )

    def apply_and_revalidate(
        self,
        document,
        *,
        target_language: str,
    ) -> ReviewRun:
        unresolved = self.document_service.unresolved(document)
        if unresolved:
            return ReviewRun(
                document=document,
                validation=self.validator.validate(document),
                workspace=self.reviews.workspace(str(document.document_id)),
                unresolved=unresolved,
            )

        reviewed = self.document_service.apply_approved(document)
        validation = self.validator.validate(reviewed)
        return ReviewRun(
            document=reviewed,
            validation=validation,
            workspace=self.reviews.workspace(str(document.document_id)),
            unresolved=[],
        )

    @staticmethod
    def _find_element(document, element_id: str):
        for page in document.pages:
            for element in page.elements:
                if element.id == element_id:
                    return element
        return None

    def can_export(self, run: ReviewRun) -> bool:
        return not run.unresolved and run.validation.export_allowed
