from pathlib import Path

from backend.reconstruction.composer import ReconstructionComposer
from backend.reconstruction.pdf_renderer import PdfRenderer
from backend.reconstruction.udr_renderer import UdrRenderMapper
from backend.schemas.udr import UdrDocument


class ReconstructionService:
    def __init__(
        self,
        mapper: UdrRenderMapper | None = None,
        pdf_renderer: PdfRenderer | None = None,
        composer: ReconstructionComposer | None = None,
    ) -> None:
        self.mapper = mapper or UdrRenderMapper()
        self.pdf_renderer = pdf_renderer or PdfRenderer()
        self.composer = composer or ReconstructionComposer()

    def build_render_plan(self, document: UdrDocument) -> list[dict]:
        render_document = self.mapper.map(document)
        return self.composer.plan(render_document)

    def render_pdf(
        self,
        document: UdrDocument,
        output_path: str | Path,
    ) -> Path:
        render_document = self.mapper.map(document)
        return self.pdf_renderer.render(render_document, output_path)
