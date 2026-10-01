from backend.diagrams.models import DiagramDomain
from backend.diagrams.service import DiagramService


def test_diagram_label_extraction():
    diagram = DiagramService().analyze(
        domain=DiagramDomain.BIOLOGY,
        label_candidates=[
            {"text": "Nucleus", "confidence": 0.9, "x": 20, "y": 30, "width": 60, "height": 20},
            {"text": "123!!!", "confidence": 0.9, "x": 1, "y": 1, "width": 10, "height": 10},
        ],
    )

    assert len(diagram.labels) == 1
    assert diagram.labels[0].text == "Nucleus"


def test_diagram_objects_and_relationships():
    diagram = DiagramService().analyze(
        domain=DiagramDomain.PHYSICS,
        label_candidates=[
            {"text": "A", "confidence": 0.9},
        ],
        object_candidates=[
            {"object_type": "A", "confidence": 0.8},
        ],
    )

    assert len(diagram.objects) == 1
    assert len(diagram.relationships) == 1
    assert diagram.relationships[0].relation == "labels"
