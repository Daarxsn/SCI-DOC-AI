from backend.mathematics.models import Equation
from backend.mathematics.recognizer import EquationRecognizer
from backend.mathematics.validator import MathValidator


class MathematicsService:
    def __init__(
        self,
        recognizer: EquationRecognizer | None = None,
        validator: MathValidator | None = None,
    ) -> None:
        self.recognizer = recognizer or EquationRecognizer()
        self.validator = validator or MathValidator()

    def process(self, raw_text: str, confidence: float = 0.5) -> Equation:
        equation = self.recognizer.recognize(raw_text, confidence)
        return self.validator.validate(equation)
