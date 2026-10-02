from dataclasses import dataclass
from backend.schemas.udr import ElementType, UdrDocument

@dataclass(frozen=True)
class TranslationConsistencyIssue:
    severity: str
    code: str
    element_id: str
    message: str

class TranslationConsistencyValidator:
    TEXT_TYPES = {ElementType.HEADING, ElementType.PARAGRAPH, ElementType.QUESTION, ElementType.SUBQUESTION, ElementType.OPTION, ElementType.CAPTION, ElementType.HEADER, ElementType.FOOTER, ElementType.LABEL}
    def validate(self, document: UdrDocument):
        issues = []
        for page in document.pages:
            for element in page.elements:
                if element.type in self.TEXT_TYPES and element.source_text and not element.target_text:
                    issues.append(TranslationConsistencyIssue("warning", "missing_target_text", element.id, "Translatable element has source text but no target text."))
                status = element.metadata.get("translation_status")
                if status == "review" and not element.metadata.get("review_id"):
                    issues.append(TranslationConsistencyIssue("error", "review_without_review_id", element.id, "Element is marked for review without a review identifier."))
                confidence = element.metadata.get("translation_confidence")
                if confidence is not None and (not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1):
                    issues.append(TranslationConsistencyIssue("error", "invalid_translation_confidence", element.id, "Translation confidence must be between 0 and 1."))
        return issues
