from backend.validation.models import ValidationReport, ValidationSeverity


class ReviewGate:
    def requires_human_review(self, report: ValidationReport) -> bool:
        return any(
            issue.severity in {
                ValidationSeverity.CRITICAL,
                ValidationSeverity.WARNING,
            }
            for issue in report.issues
        )

    def can_auto_export(self, report: ValidationReport) -> bool:
        return report.passed and not self.requires_human_review(report)
