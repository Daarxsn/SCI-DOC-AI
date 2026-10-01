from backend.mathematics.models import Equation
from backend.schemas.udr import UdrElement


class MathUdrAdapter:
    def enrich(self, element: UdrElement, equation: Equation) -> UdrElement:
        element.metadata.update(
            {
                "equation_id": equation.equation_id,
                "latex": equation.latex,
                "mathml": equation.mathml,
                "math_representation": equation.representation.value,
                "math_symbols": [
                    {
                        "symbol": symbol.symbol,
                        "normalized": symbol.normalized,
                        "confidence": symbol.confidence,
                    }
                    for symbol in equation.symbols
                ],
                "math_validation_errors": equation.validation_errors,
            }
        )
        element.confidence = min(element.confidence or 0, equation.confidence)
        element.model_version = "math-baseline-0.1"
        return element
