import re

from backend.mathematics.models import Equation


class MathValidator:
    def validate(self, equation: Equation) -> Equation:
        errors: list[str] = []
        latex = equation.latex or ""

        if not latex.strip():
            errors.append("empty mathematical representation")

        if latex.count("{") != latex.count("}"):
            errors.append("unbalanced LaTeX braces")

        if latex.count("(") != latex.count(")"):
            errors.append("unbalanced parentheses")

        if re.search(r"\[a-zA-Z]+\s*$", latex):
            errors.append("incomplete LaTeX command")

        equation.validation_errors = errors
        return equation
