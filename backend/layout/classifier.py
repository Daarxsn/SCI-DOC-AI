import re

from backend.ocr.models import OcrBlock
from backend.schemas.udr import ElementType


QUESTION_PATTERN = re.compile(r"^(?:Q(?:uestion)?\.?\s*)?\d{1,3}[.)]?$", re.IGNORECASE)
OPTION_PATTERN = re.compile(r"^[A-Da-d][.)]$")
EQUATION_PATTERN = re.compile(r"(=|≤|≥|∫|√|∑|π|\^|[A-Za-z]\s*=)")


class LayoutClassifier:
    def classify(self, block: OcrBlock) -> ElementType:
        text = block.text.strip()

        if OPTION_PATTERN.match(text):
            return ElementType.OPTION

        if EQUATION_PATTERN.search(text) and any(char.isdigit() for char in text):
            return ElementType.EQUATION

        if QUESTION_PATTERN.match(text):
            return ElementType.QUESTION

        if len(text) < 100 and text.isupper():
            return ElementType.HEADING

        return ElementType.PARAGRAPH
