from pathlib import Path

from backend.reconstruction.composer import ReconstructionComposer
from backend.reconstruction.models import RenderDocument, RenderElement, RenderPage


def make_document():
    return RenderDocument(
        document_id="doc-1",
        pages=[
            RenderPage(
                page_number=1,
                width=800,
                height=1000,
                elements=[
                    RenderElement(
                        element_id="eq1",
                        element_type="equation",
                        x=10,
                        y=10,
                        width=200,
                        height=50,
                        text="x = 2",
                        metadata={"latex": "x = 2"},
                    ),
                    RenderElement(
                        element_id="d1",
                        element_type="diagram",
                        x=10,
                        y=80,
                        width=300,
                        height=200,
                        metadata={
                            "domain": "physics",
                            "objects": [{"object_type": "arrow"}],
                            "labels": [{"text": "v"}],
                            "relationships": [],
                        },
                    ),
                    RenderElement(
                        element_id="t1",
                        element_type="table",
                        x=10,
                        y=300,
                        width=300,
                        height=100,
                        metadata={"columns": ["A", "B"], "rows": [["1", "2"]]},
                    ),
                ],
            )
        ],
    )


def test_scientific_elements_get_dedicated_render_plans():
    plan = ReconstructionComposer().plan(make_document())

    assert [item["render_status"] for item in plan] == [
        "adapter_required",
        "adapter_required",
        "grid_adapter_required",
    ]


def test_image_renderer_reports_missing_asset():
    element = RenderElement(
        element_id="img1",
        element_type="image",
        x=0,
        y=0,
        width=100,
        height=100,
        metadata={"asset_path": "/does/not/exist.png"},
    )

    result = ReconstructionComposer().image_renderer.render(element)
    assert result["render_status"] == "asset_missing"
    assert result["asset_path"] is None
