from backend.schemas.udr import UdrDocument
from backend.reconstruction.models import RenderDocument, RenderElement, RenderPage


class UdrRenderMapper:
    def map(self, document: UdrDocument) -> RenderDocument:
        pages: list[RenderPage] = []

        for page in document.pages:
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

            pages.append(
                RenderPage(
                    page_number=page.page_number,
                    width=page.width,
                    height=page.height,
                    elements=elements,
                )
            )

        return RenderDocument(
            document_id=str(document.document_id),
            pages=pages,
        )
