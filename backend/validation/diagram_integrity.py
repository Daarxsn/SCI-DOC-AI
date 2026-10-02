from dataclasses import dataclass
from backend.schemas.udr import ElementType, UdrDocument

@dataclass(frozen=True)
class DiagramIssue:
    severity: str
    code: str
    element_id: str
    message: str

class DiagramIntegrityValidator:
    def validate(self, document: UdrDocument):
        issues = []
        for page in document.pages:
            for element in page.elements:
                if element.type not in {ElementType.DIAGRAM, ElementType.GRAPH}:
                    continue
                objects = {str(x.get("id")) for x in element.metadata.get("objects", []) if x.get("id") is not None}
                labels = {str(x.get("id")) for x in element.metadata.get("labels", []) if x.get("id") is not None}
                for rel in element.metadata.get("relationships", []):
                    if rel.get("source") is not None and str(rel["source"]) not in objects and str(rel["source"]) not in labels:
                        issues.append(DiagramIssue("error", "missing_relationship_source", element.id, f"Diagram relationship references missing source '{rel['source']}'."))
                    if rel.get("target") is not None and str(rel["target"]) not in objects and str(rel["target"]) not in labels:
                        issues.append(DiagramIssue("error", "missing_relationship_target", element.id, f"Diagram relationship references missing target '{rel['target']}'."))
                for label in element.metadata.get("labels", []):
                    if label.get("source_text") and not label.get("text"):
                        issues.append(DiagramIssue("warning", "diagram_label_translation_missing", element.id, "A diagram label has source text but no translated text."))
        return issues
