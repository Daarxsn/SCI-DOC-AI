from pathlib import Path
from backend.diagrams.models import DiagramDomain, DiagramObject


class UltralyticsDiagramDetector:
    """Optional YOLO/Ultralytics detector for domain-specific diagram objects."""

    name = "ultralytics"

    def __init__(self, model_path: str, device: str = "auto") -> None:
        self.model_path = model_path
        self.device = device
        self._model = None

    def _load(self):
        if self._model is None:
            try:
                from ultralytics import YOLO
            except ImportError as exc:
                raise RuntimeError("ultralytics is required for diagram detection.") from exc
            if not self.model_path:
                raise RuntimeError("A trained diagram model path is required.")
            self._model = YOLO(self.model_path)
        return self._model

    def detect(self, image_path: str | Path, domain: DiagramDomain) -> list[dict]:
        results = self._load().predict(source=str(image_path), verbose=False, device=None if self.device == "auto" else self.device)
        candidates = []
        for result in results:
            names = result.names or {}
            boxes = getattr(result, "boxes", None)
            if boxes is None:
                continue
            for index in range(len(boxes)):
                cls_id = int(boxes.cls[index].item())
                confidence = float(boxes.conf[index].item())
                xyxy = [float(x) for x in boxes.xyxy[index].tolist()]
                candidates.append({
                    "object_type": str(names.get(cls_id, cls_id)),
                    "confidence": confidence,
                    "attributes": {"bbox": ",".join(map(str, xyxy)), "domain": domain.value},
                })
        return candidates
