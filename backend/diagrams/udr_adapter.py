from backend.diagrams.models import Diagram
from backend.schemas.udr import UdrElement


class DiagramUdrAdapter:
    def enrich(self, element: UdrElement, diagram: Diagram) -> UdrElement:
        element.metadata.update(
            {
                "diagram_id": diagram.diagram_id,
                "diagram_domain": diagram.domain.value,
                "diagram_labels": [label.model_dump() for label in diagram.labels],
                "diagram_objects": [obj.model_dump() for obj in diagram.objects],
                "diagram_relationships": [
                    relation.model_dump() for relation in diagram.relationships
                ],
            }
        )
        element.confidence = min(element.confidence or 0, diagram.confidence)
        element.model_version = "diagram-baseline-0.1"
        return element
