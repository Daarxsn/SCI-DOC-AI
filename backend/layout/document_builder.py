from uuid import uuid4

from backend.layout.structure import StructureAnalyzer
from backend.ocr.models import OcrPageResult
from backend.schemas.udr import (
    BoundingBox,
    DocumentSource,
    ElementType,
    Provenance,
    UdrDocument,
    UdrElement,
    UdrPage,
)


class OcrDocumentBuilder:
    def __init__(self, analyzer: StructureAnalyzer | None = None) -> None:
        self.analyzer = analyzer or StructureAnalyzer()

    def build_page(self, result: OcrPageResult, page_number: int) -> UdrPage:
        elements: list[UdrElement] = []

        for block in sorted(result.blocks, key=lambda item: item.reading_order):
            element_type, metadata = self.analyzer.analyze(block)

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
                    metadata=metadata,
                )
            )

        return UdrPage(
            page_number=page_number,
            width=result.width,
            height=result.height,
            elements=elements,
        )

    def build_document(
        self,
        *,
        document_type: str,
        source_language: str,
        mime_type: str,
        domain: str,
        pages: list[OcrPageResult],
    ) -> UdrDocument:
        return UdrDocument(
            document_id=uuid4(),
            document_type=document_type,
            source=DocumentSource(
                language=source_language,
                mime_type=mime_type,
            ),
            domain=domain,
            pages=[
                self.build_page(result, page_number=index)
                for index, result in enumerate(pages, start=1)
            ],
        )
