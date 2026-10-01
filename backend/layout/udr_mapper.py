from uuid import uuid4

from backend.layout.classifier import LayoutClassifier
from backend.ocr.models import OcrPageResult
from backend.schemas.udr import (
    BoundingBox,
    ElementType,
    Provenance,
    UdrElement,
    UdrPage,
)


class UdrMapper:
    def __init__(self, classifier: LayoutClassifier | None = None) -> None:
        self.classifier = classifier or LayoutClassifier()

    def map_page(self, result: OcrPageResult, page_number: int) -> UdrPage:
        elements: list[UdrElement] = []

        for block in sorted(result.blocks, key=lambda item: item.reading_order):
            element_type = self.classifier.classify(block)

            elements.append(
                UdrElement(
                    id=f"el-{uuid4().hex[:12]}",
                    type=element_type,
                    bbox=BoundingBox(
                        x=block.x,
                        y=block.y,
                        width=block.width,
                        height=block.height,
                    ),
                    text=block.text,
                    source_text=block.text,
                    confidence=block.confidence,
                    provenance=Provenance(
                        source_type="ocr",
                        extractor=result.engine,
                        extractor_version=result.engine_version,
                    ),
                    model_version=result.engine_version,
                )
            )

        return UdrPage(
            page_number=page_number,
            width=result.width,
            height=result.height,
            elements=elements,
        )
