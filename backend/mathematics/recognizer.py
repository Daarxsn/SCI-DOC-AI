from uuid import uuid4

from backend.mathematics.models import Equation, MathRepresentation, MathSymbol
from backend.mathematics.normalizer import MathNormalizer


class EquationRecognizer:
    """Baseline recognizer.

    Converts OCR equation candidates into a structured representation.
    A vision/math model can later implement the same interface.
    """

    def __init__(self, normalizer: MathNormalizer | None = None) -> None:
        self.normalizer = normalizer or MathNormalizer()

    def recognize(self, raw_text: str, confidence: float = 0.5) -> Equation:
        latex = self.normalizer.to_latex_candidate(raw_text)

        symbols = [
            MathSymbol(symbol=char, normalized=char, confidence=confidence)
            for char in raw_text
            if char in "=+-*/×÷≤≥±π∞√∑∫αβγΔθλ"
        ]

        return Equation(
            equation_id=f"eq-{uuid4().hex[:12]}",
            raw_text=raw_text,
            latex=latex,
            representation=MathRepresentation.LATEX,
            confidence=confidence,
            symbols=symbols,
        )
