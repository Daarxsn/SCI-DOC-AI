from uuid import uuid4

from backend.diagrams.label_extractor import DiagramLabelExtractor
from backend.diagrams.models import Diagram, DiagramDomain
from backend.diagrams.object_detector import DiagramObjectDetector
from backend.diagrams.relationship_builder import DiagramRelationshipBuilder


class DiagramService:
    def __init__(
        self,
        label_extractor: DiagramLabelExtractor | None = None,
        object_detector: DiagramObjectDetector | None = None,
        relationship_builder: DiagramRelationshipBuilder | None = None,
    ) -> None:
        self.label_extractor = label_extractor or DiagramLabelExtractor()
        self.object_detector = object_detector or DiagramObjectDetector()
        self.relationship_builder = relationship_builder or DiagramRelationshipBuilder()

    def analyze(
        self,
        *,
        domain: DiagramDomain,
        source_image_path: str | None = None,
        label_candidates: list[dict] | None = None,
        object_candidates: list[dict] | None = None,
        confidence: float = 0.5,
    ) -> Diagram:
        labels = self.label_extractor.extract(label_candidates or [])
        objects = self.object_detector.detect(object_candidates or [])
        relationships = self.relationship_builder.build(labels, objects)

        return Diagram(
            diagram_id=f"diag-{uuid4().hex[:12]}",
            domain=domain,
            confidence=confidence,
            labels=labels,
            objects=objects,
            relationships=relationships,
            source_image_path=source_image_path,
        )
