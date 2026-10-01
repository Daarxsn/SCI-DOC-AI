import re

from backend.ocr.models import OcrBlock
from backend.schemas.udr import ElementType


QUESTION_LINE = re.compile(
    r"^(?:Q(?:uestion)?\s*)?(\d{1,3})(?:\s*[.)]|\s*:)?\s+",
    re.IGNORECASE,
)
SUBQUESTION_LINE = re.compile(r"^\(?([a-z])\)?[.)]\s+", re.IGNORECASE)
MARKS_PATTERN = re.compile(r"\[(\d+)\s*(?:marks?|M)\]|\((\d+)\s*(?:marks?|M)\)", re.IGNORECASE)
TABLE_PATTERN = re.compile(r"\|.*\|")


class StructureAnalyzer:
    def analyze(self, block: OcrBlock) -> tuple[ElementType, dict]:
        text = block.text.strip()
        metadata: dict = {}

        question = QUESTION_LINE.match(text)
        if question:
            metadata["question_number"] = int(question.group(1))
            marks = MARKS_PATTERN.search(text)
            if marks:
                metadata["marks"] = int(marks.group(1) or marks.group(2))
            return ElementType.QUESTION, metadata

        subquestion = SUBQUESTION_LINE.match(text)
        if subquestion:
            metadata["subquestion_label"] = subquestion.group(1).lower()
            return ElementType.SUBQUESTION, metadata

        if TABLE_PATTERN.search(text) or text.count("\t") >= 2:
            return ElementType.TABLE, metadata

        if "=" in text and any(char.isdigit() for char in text):
            return ElementType.EQUATION, metadata

        return ElementType.PARAGRAPH, metadata
