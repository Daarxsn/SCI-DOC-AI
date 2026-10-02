from backend.schemas.udr import UdrDocument
from backend.validation.element_validator import ElementValidator
from backend.validation.models import (
    ValidationIssue,
    ValidationReport,
    ValidationSeverity,
)
from backend.validation.structure_validator import StructureValidator


class ValidationService:
    def __init__(
        self,
        element_validator: ElementValidator | None = None,
        structure_validator: StructureValidator | None = None,
    ) -> None:
        self.element_validator = element_validator or ElementValidator()
        self.structure_validator = structure_validator or StructureValidator()

    def validate(self, document: UdrDocument) -> ValidationReport:
        issues: list[ValidationIssue] = []

        for page in document.pages:
            for element in page.elements:
                issues.extend(self.element_validator.validate(element))

        issues.extend(self.structure_validator.validate(document))

        critical = sum(
            issue.severity == ValidationSeverity.CRITICAL
            for issue in issues
        )
        warnings = sum(
            issue.severity == ValidationSeverity.WARNING
            for issue in issues
        )

        return ValidationReport(
            passed=critical == 0,
            issues=issues,
            checked_elements=sum(len(page.elements) for page in document.pages),
            critical_issues=critical,
            warning_count=warnings,
        )
