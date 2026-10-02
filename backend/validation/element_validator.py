from backend.schemas.udr import ElementType, UdrElement
from backend.validation.models import ValidationIssue, ValidationSeverity


class ElementValidator:
    def validate(self, element: UdrElement) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []

        if element.type == ElementType.EQUATION:
            if not element.source_text:
                issues.append(
                    ValidationIssue(
                        code="MATH_SOURCE_MISSING",
                        severity=ValidationSeverity.CRITICAL,
                        message="Equation has no source representation.",
                        element_id=element.id,
                    )
                )

            errors = element.metadata.get("math_validation_errors", [])
            for error in errors:
                issues.append(
                    ValidationIssue(
                        code="MATH_VALIDATION_ERROR",
                        severity=ValidationSeverity.CRITICAL,
                        message=str(error),
                        element_id=element.id,
                    )
                )

        if element.type in {ElementType.QUESTION, ElementType.SUBQUESTION}:
            if not element.source_text:
                issues.append(
                    ValidationIssue(
                        code="QUESTION_TEXT_MISSING",
                        severity=ValidationSeverity.CRITICAL,
                        message="Question element has no source text.",
                        element_id=element.id,
                    )
                )

        translation_status = element.metadata.get("translation_status")
        if translation_status == "review":
            issues.append(
                ValidationIssue(
                    code="TRANSLATION_REVIEW_REQUIRED",
                    severity=ValidationSeverity.WARNING,
                    message="Translation requires human review.",
                    element_id=element.id,
                )
            )

        if element.confidence is not None and element.confidence < 0.5:
            issues.append(
                ValidationIssue(
                    code="LOW_CONFIDENCE",
                    severity=ValidationSeverity.WARNING,
                    message="Element confidence is below the automatic acceptance threshold.",
                    element_id=element.id,
                )
            )

        return issues
