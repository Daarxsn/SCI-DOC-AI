import re
from uuid import uuid4

from backend.diagrams.models import DiagramLabel


class DiagramLabelExtractor:
    """Baseline label extractor.

    The production implementation will consume OCR regions and/or a vision
    detector. This baseline identifies short label-like OCR strings.
    """

    LABEL_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_\-]{0,24}$")

    def extract(self, texts: list[dict]) -> list[DiagramLabel]:
        labels: list[DiagramLabel] = []

        for item in texts:
            text = str(item.get("text", "")).strip()
            if not text or not self.LABEL_PATTERN.match(text):
                continue

            labels.append(
                DiagramLabel(
                    label_id=f"lbl-{uuid4().hex[:10]}",
                    text=text,
                    confidence=float(item.get("confidence", 0.5)),
                    x=max(0, float(item.get("x", 0))),
                    y=max(0, float(item.get("y", 0))),
                    width=max(0, float(item.get("width", 0))),
                    height=max(0, float(item.get("height", 0))),
                )
            )

        return labels
