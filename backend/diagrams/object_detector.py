from uuid import uuid4

from backend.diagrams.models import DiagramObject


class DiagramObjectDetector:
    """Domain-neutral baseline object detector.

    Actual object detection is intentionally model-adapter based and can later
    use YOLO, DETR, or a specialized scientific vision model.
    """

    def detect(self, candidates: list[dict]) -> list[DiagramObject]:
        objects: list[DiagramObject] = []

        for candidate in candidates:
            object_type = str(candidate.get("object_type", "")).strip()
            if not object_type:
                continue

            objects.append(
                DiagramObject(
                    object_id=f"obj-{uuid4().hex[:10]}",
                    object_type=object_type,
                    confidence=float(candidate.get("confidence", 0.5)),
                    attributes={
                        str(key): str(value)
                        for key, value in candidate.get("attributes", {}).items()
                    },
                )
            )

        return objects
