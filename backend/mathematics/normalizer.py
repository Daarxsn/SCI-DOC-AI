import re

UNICODE_TO_LATEX = {
    "×": r"\times",
    "÷": r"\div",
    "≤": r"\leq",
    "≥": r"\geq",
    "±": r"\pm",
    "π": r"\pi",
    "∞": r"\infty",
    "√": r"\sqrt{}",
    "∑": r"\sum",
    "∫": r"\int",
    "α": r"\alpha",
    "β": r"\beta",
    "γ": r"\gamma",
    "Δ": r"\Delta",
    "θ": r"\theta",
    "λ": r"\lambda",
}


class MathNormalizer:
    def to_latex_candidate(self, text: str) -> str:
        normalized = text.strip()

        for source, target in UNICODE_TO_LATEX.items():
            normalized = normalized.replace(source, target)

        normalized = re.sub(r"\s+", " ", normalized)
        return normalized
