from backend.schemas.udr import UdrDocument
from backend.validation.report import ScientificValidationReport
from backend.validation.scientific import ScientificValidator


class ScientificValidationService:
    def __init__(self, validator: ScientificValidator | None = None) -> None:
        self.validator = validator or ScientificValidator()

    def validate(self, document: UdrDocument) -> ScientificValidationReport:
        issues = self.validator.validate(document)
        return ScientificValidationReport(
            document_id=str(document.document_id),
            issues=issues,
        )
