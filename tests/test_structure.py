from backend.layout.structure import StructureAnalyzer
from backend.ocr.models import OcrBlock
from backend.schemas.udr import ElementType


def make_block(text: str) -> OcrBlock:
    return OcrBlock(
        text=text,
        confidence=0.95,
        x=10,
        y=20,
        width=300,
        height=40,
        reading_order=0,
    )


def test_question_number_and_marks():
    element_type, metadata = StructureAnalyzer().analyze(make_block("Q12. Explain refraction [5 marks]"))
    assert element_type == ElementType.QUESTION
    assert metadata["question_number"] == 12
    assert metadata["marks"] == 5


def test_subquestion():
    element_type, metadata = StructureAnalyzer().analyze(make_block("(b) Calculate the force."))
    assert element_type == ElementType.SUBQUESTION
    assert metadata["subquestion_label"] == "b"


def test_table_candidate():
    element_type, _ = StructureAnalyzer().analyze(make_block("| A | B | C |"))
    assert element_type == ElementType.TABLE


def test_equation_candidate():
    element_type, _ = StructureAnalyzer().analyze(make_block("F = ma"))
    assert element_type == ElementType.EQUATION
