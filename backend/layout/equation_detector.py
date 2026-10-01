import re

from backend.ocr.models import OcrBlock


MATH_SYMBOLS = set("=≤≥∫√∑π∞±×÷")


class EquationCandidateDetector:
    def detect(self, blocks: list[OcrBlock]) -> list[OcrBlock]:
        candidates: list[OcrBlock] = []

        for block in blocks:
            text = block.text
            symbol_score = sum(char in MATH_SYMBOLS for char in text)
            has_relation = "=" in text or "≤" in text or "≥" in text
            has_digit = any(char.isdigit() for char in text)

            if has_relation and has_digit:
                candidates.append(block)
            elif symbol_score >= 2 and has_digit:
                candidates.append(block)

        return candidates
