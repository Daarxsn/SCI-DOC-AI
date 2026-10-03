from pathlib import Path

from backend.schemas.udr import UdrDocument
from backend.reconstruction.models import RenderDocument, RenderElement, RenderPage


class UdrRenderMapper:
    def map(
        self,
        document: UdrDocument,
        source_page_paths: list[str | Path] | None = None,
    ) -> RenderDocument:
        pages: list[RenderPage] = []
        source_page_paths = source_page_paths or []

        for page_index, page in enumerate(document.pages):
            elements: list[RenderElement] = []

            for element in page.elements:
                if element.bbox is None:
                    continue

                elements.append(
                    RenderElement(
                        element_id=element.id,
                        element_type=element.type.value,
                        x=element.bbox.x,
                        y=element.bbox.y,
                        width=element.bbox.width,
                        height=element.bbox.height,
                        text=element.target_text or element.text,
                        source_text=element.source_text,
                        confidence=element.confidence,
                        metadata=element.metadata,
                    )
                )

            page_metadata = {}
            if page_index < len(source_page_paths):
                page_metadata["source_page_path"] = str(source_page_paths[page_index])

            pages.append(
                RenderPage(
                    page_number=page.page_number,
                    width=page.width,
                    height=page.height,
                    elements=elements,
                    metadata=page_metadata,
                )
            )

        return RenderDocument(
            document_id=str(document.document_id),
            pages=pages,
        )
