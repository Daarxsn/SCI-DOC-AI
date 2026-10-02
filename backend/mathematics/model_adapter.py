from pathlib import Path
from backend.mathematics.models import Equation, MathRepresentation
from backend.mathematics.normalizer import MathNormalizer
from backend.mathematics.validator import MathValidator


class Pix2TexEquationAdapter:
    """Optional image-to-LaTeX adapter backed by pix2tex."""

    name = "pix2tex"

    def __init__(self, device: str = "auto") -> None:
        self.device = device
        self._model = None

    def _load(self):
        if self._model is None:
            try:
                from pix2tex.cli import LatexOCR
            except ImportError as exc:
                raise RuntimeError("pix2tex is required for image equation recognition.") from exc
            self._model = LatexOCR()
        return self._model

    def recognize_image(self, image_path: str | Path) -> Equation:
        latex = str(self._load()(str(image_path))).strip()
        equation = Equation(
            equation_id=f"eq-pix2tex-{Path(image_path).stem}",
            raw_text=latex,
            latex=latex,
            representation=MathRepresentation.LATEX,
            confidence=0.75 if latex else 0.0,
        )
        return MathValidator().validate(equation)


class HybridEquationService:
    def __init__(self, provider: str = "baseline", device: str = "auto") -> None:
        self.provider = provider
        self.model = Pix2TexEquationAdapter(device) if provider == "pix2tex" else None
        self.baseline = MathNormalizer()
        self.validator = MathValidator()

    def process_text(self, raw_text: str, confidence: float = 0.5) -> Equation:
        from backend.mathematics.recognizer import EquationRecognizer
        return self.validator.validate(EquationRecognizer(self.baseline).recognize(raw_text, confidence))

    def process_image(self, image_path: str | Path) -> Equation:
        if self.model is None:
            raise RuntimeError("Equation image provider is not configured. Set EQUATION_PROVIDER=pix2tex.")
        return self.model.recognize_image(image_path)
