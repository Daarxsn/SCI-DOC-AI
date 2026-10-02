from dataclasses import dataclass, field
from backend.reconstruction.layout import LayoutEngine
from backend.reconstruction.udr_renderer import UdrRenderMapper
from backend.schemas.udr import UdrDocument
from backend.validation.diagram_integrity import DiagramIntegrityValidator
from backend.validation.mathematics import MathematicalEquivalenceValidator
from backend.validation.provenance import ProvenanceValidator
from backend.validation.scientific import ScientificValidator
from backend.validation.translation_consistency import TranslationConsistencyValidator

@dataclass(frozen=True)
class UnifiedIssue:
    severity: str
    code: str
    element_id: str | None
    message: str
    stage: str

@dataclass
class UnifiedValidationReport:
    document_id: str
    issues: list[UnifiedIssue] = field(default_factory=list)
    checked_elements: int = 0
    @property
    def passed(self): return not any(i.severity in {"critical","error"} for i in self.issues)
    @property
    def requires_review(self): return any(i.severity in {"critical","error","warning"} for i in self.issues)
    @property
    def export_allowed(self): return self.passed and not self.requires_review
    def count(self, severity): return sum(i.severity == severity for i in self.issues)

class UnifiedValidationService:
    def __init__(self):
        self.scientific=ScientificValidator()
        self.math=MathematicalEquivalenceValidator()
        self.diagram=DiagramIntegrityValidator()
        self.translation=TranslationConsistencyValidator()
        self.provenance=ProvenanceValidator()
        self.layout=LayoutEngine()
        self.mapper=UdrRenderMapper()
    def validate(self, document: UdrDocument):
        issues=[]
        def add(stage, items):
            for item in items:
                issues.append(UnifiedIssue(item.severity,item.code,getattr(item,"element_id",None),item.message,stage))
        add("scientific",self.scientific.validate(document))
        add("mathematics",self.math.validate(document))
        add("diagrams",self.diagram.validate(document))
        add("translation",self.translation.validate(document))
        add("provenance",self.provenance.validate(document))
        for page in self.mapper.map(document).pages:
            for issue in self.layout.validate_page(page):
                issues.append(UnifiedIssue("error" if issue.severity=="error" else "warning",issue.code,issue.element_id,issue.message,"reconstruction_layout"))
        return UnifiedValidationReport(str(document.document_id),issues,sum(len(p.elements) for p in document.pages))
