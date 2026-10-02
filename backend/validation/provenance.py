from dataclasses import dataclass
from backend.schemas.udr import UdrDocument

@dataclass(frozen=True)
class ProvenanceIssue:
    severity: str
    code: str
    element_id: str | None
    message: str

class ProvenanceValidator:
    def validate(self, document: UdrDocument):
        issues = []
        for page in document.pages:
            for element in page.elements:
                if element.provenance is None:
                    issues.append(ProvenanceIssue("warning", "missing_element_provenance", element.id, "Element has no extractor/model provenance."))
                if element.model_version is None and element.type.value != "page_number":
                    issues.append(ProvenanceIssue("info", "missing_model_version", element.id, "Element has no model version recorded."))
        return issues
