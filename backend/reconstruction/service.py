import hashlib
from pathlib import Path

from backend.reconstruction.composer import ReconstructionComposer
from backend.reconstruction.layout import LayoutEngine, LayoutIssue
from backend.reconstruction.models import ReconstructionArtifact
from backend.reconstruction.pdf_renderer import PdfRenderer
from backend.reconstruction.udr_renderer import UdrRenderMapper
from backend.schemas.udr import UdrDocument


class ReconstructionService:
    def __init__(self, mapper=None, pdf_renderer=None, composer=None, layout_engine=None):
        self.mapper = mapper or UdrRenderMapper()
        self.pdf_renderer = pdf_renderer or PdfRenderer()
        self.composer = composer or ReconstructionComposer()
        self.layout_engine = layout_engine or LayoutEngine()

    def build_render_plan(
        self,
        document: UdrDocument,
        source_page_paths: list[str | Path] | None = None,
    ) -> list[dict]:
        return self.composer.plan(self.mapper.map(document, source_page_paths))

    def validate_layout(
        self,
        document: UdrDocument,
        margin: float = 0,
        source_page_paths: list[str | Path] | None = None,
    ) -> list[LayoutIssue]:
        render_document = self.mapper.map(document, source_page_paths)
        issues: list[LayoutIssue] = []
        for page in render_document.pages:
            issues.extend(self.layout_engine.validate_page(page, margin=margin))
        return issues

    def render_pdf(
        self,
        document: UdrDocument,
        output_path: str | Path,
        *,
        source_page_paths: list[str | Path] | None = None,
        require_layout_pass: bool = True,
    ) -> Path:
        render_document = self.mapper.map(document, source_page_paths)
        issues: list[LayoutIssue] = []
        for page in render_document.pages:
            issues.extend(self.layout_engine.validate_page(page))
            page.elements = self.layout_engine.sort_for_rendering(page)

        blocking = [issue for issue in issues if issue.severity == "error"]
        if require_layout_pass and blocking:
            details = "; ".join(f"{i.code}:{i.element_id}" for i in blocking[:10])
            raise ValueError(f"Reconstruction layout validation failed: {details}")

        return self.pdf_renderer.render(render_document, output_path)

    def export_artifact(
        self,
        document: UdrDocument,
        output_path: str | Path,
        *,
        source_page_paths: list[str | Path] | None = None,
        require_layout_pass: bool = True,
    ) -> ReconstructionArtifact:
        path = self.render_pdf(
            document,
            output_path,
            source_page_paths=source_page_paths,
            require_layout_pass=require_layout_pass,
        )
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        issues = self.validate_layout(
            document,
            source_page_paths=source_page_paths,
        )
        return ReconstructionArtifact(
            document_id=str(document.document_id),
            format="pdf",
            path=str(path),
            size_bytes=path.stat().st_size,
            sha256=digest,
            page_count=len(document.pages),
            layout_warnings=sum(1 for issue in issues if issue.severity == "warning"),
        )
