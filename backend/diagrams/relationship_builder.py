from backend.diagrams.models import DiagramLabel, DiagramObject, DiagramRelationship


class DiagramRelationshipBuilder:
    def build(
        self,
        labels: list[DiagramLabel],
        objects: list[DiagramObject],
    ) -> list[DiagramRelationship]:
        relationships: list[DiagramRelationship] = []

        # Baseline only: labels can be attached to explicitly supplied objects.
        for label in labels:
            target_id = next(
                (
                    obj.object_id
                    for obj in objects
                    if obj.object_type.lower() == label.text.lower()
                ),
                None,
            )
            if target_id:
                relationships.append(
                    DiagramRelationship(
                        source_id=label.label_id,
                        relation="labels",
                        target_id=target_id,
                        confidence=min(label.confidence, 0.7),
                    )
                )

        return relationships
