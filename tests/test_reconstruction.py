from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

from backend.reconstruction.layout import LayoutEngine
from backend.reconstruction.models import ReconstructionArtifact
from backend.reconstruction.service import ReconstructionService
from backend.reconstruction.text_fitter import TextFitter
from backend.reconstruction.udr_renderer import UdrRenderMapper
from backend.schemas.udr import (
    BoundingBox,
    DocumentSource,
    ElementType,
    UdrDocument,
    UdrElement,
    UdrPage,
)


def make_document():
    return UdrDocument(
        document_id=uuid4(),
        document_type="question_paper",
        source=DocumentSource(language="en", mime_type="application/pdf"),
        domain="physics",
        pages=[
            UdrPage(
                page_number=1,
                width=800,
                height=1000,
                elements=[
                    UdrElement(
                        id="q1",
                        type=ElementType.QUESTION,
                        bbox=BoundingBox(x=50, y=60, width=500, height=100),
                        source_text="Explain velocity.",
                        target_text="वेग समझाइए।",
                        confidence=0.95,
                    )
                ],
            )
        ],
    )


def test_udr_maps_translated_text():
    rendered = UdrRenderMapper().map(make_document())
    assert rendered.pages[0].elements[0].text == "वेग समझाइए।"
    assert rendered.pages[0].elements[0].source_text == "Explain velocity."


def test_udr_maps_source_page_paths():
    rendered = UdrRenderMapper().map(
        make_document(), source_page_paths=["/tmp/page-1.png"]
    )
    assert rendered.pages[0].metadata["source_page_path"] == "/tmp/page-1.png"


def test_text_fitter_reduces_font_when_required():
    result = TextFitter().fit(
        "A" * 500,
        box_width=100,
        box_height=40,
        base_font_size=12,
    )
    assert result.font_size < 12


def test_layout_blocks_horizontal_overflow():
    document = make_document()
    document.pages[0].elements[0].bbox = BoundingBox(
        x=750, y=60, width=100, height=50
    )
    rendered = UdrRenderMapper().map(document)
    issues = LayoutEngine().validate_page(rendered.pages[0])
    assert any(issue.code == "horizontal_overflow" and issue.severity == "error" for issue in issues)


def test_export_artifact_contains_integrity_metadata():
    with TemporaryDirectory() as tmp:
        output = Path(tmp) / "reconstructed.pdf"
        artifact = ReconstructionService().export_artifact(make_document(), output)
        assert output.exists()
        assert artifact.size_bytes == output.stat().st_size
        assert len(artifact.sha256) == 64
        assert artifact.page_count == 1
        assert isinstance(artifact, ReconstructionArtifact)
