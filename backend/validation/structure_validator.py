from backend.schemas.udr import UdrDocument, ElementType
from backend.validation.models import ValidationIssue, ValidationSeverity


class StructureValidator:
    def validate(self, document: UdrDocument) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        question_numbers: list[int] = []

        for page in document.pages:
            for element in page.elements:
                if element.type != ElementType.QUESTION:
                    continue

                number = element.metadata.get("question_number")
                if isinstance(number, int):
                    question_numbers.append(number)

        seen: set[int] = set()
        for number in question_numbers:
            if number in seen:
                issues.append(
                    ValidationIssue(
                        code="DUPLICATE_QUESTION_NUMBER",
                        severity=ValidationSeverity.CRITICAL,
                        message=f"Question number {number} appears more than once.",
                    )
                )
            seen.add(number)

        if question_numbers:
            expected = list(range(min(question_numbers), max(question_numbers) + 1))
            missing = sorted(set(expected) - set(question_numbers))

            if missing:
                issues.append(
                    ValidationIssue(
                        code="MISSING_QUESTION_NUMBER",
                        severity=ValidationSeverity.WARNING,
                        message=f"Question numbering has gaps: {missing}.",
                    )
                )

        return issues
