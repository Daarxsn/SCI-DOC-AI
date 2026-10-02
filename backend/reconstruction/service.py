from pathlib import Path

from backend.reconstruction.composer import ReconstructionComposer
from backend.reconstruction.layout import LayoutEngine, LayoutIssue
from backend.reconstruction.pdf_renderer import PdfRenderer
from backend.reconstruction.udr_renderer import UdrRenderMapper
from backend.schemas.udr import UdrDocument


class ReconstructionService:
    def __init__(self, mapper=None, pdf_renderer=None, composer=None, layout_engine=None):
        self.mapper = mapper or UdrRenderMapper()
        self.pdf_renderer = pdf_renderer or PdfRenderer()
        self.composer = composer or ReconstructionComposer()
        self.layout_engine = layout_engine or LayoutEngine()

    def build_render_plan(self, document: UdrDocument) -> list[dict]:
        return self.composer.plan(self.mapper.map(document))

    def validate_layout(self, document: UdrDocument, margin: float = 0) -> list[LayoutIssue]:
        render_document = self.mapper.map(document)
        issues: list[LayoutIssue] = []
        for page in render_document.pages:
            issues.extend(self.layout_engine.validate_page(page, margin=margin))
        return issues

    def render_pdf(self, document: UdrDocument, output_path: str | Path) -> Path:
        render_document = self.mapper.map(document)
        for page in render_document.pages:
            page.elements = self.layout_engine.sort_for_rendering(page)
        return self.pdf_renderer.render(render_document, output_path)
