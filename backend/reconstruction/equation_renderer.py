from backend.reconstruction.models import RenderElement
from backend.reconstruction.unicode_renderer import UnicodeTextRenderer


class EquationRenderer:
    """Render equations with a controlled Unicode fallback."""

    SYMBOLS = {
        r"\times": "×", r"\div": "÷", r"\leq": "≤", r"\geq": "≥",
        r"\pm": "±", r"\pi": "π", r"\infty": "∞", r"\alpha": "α",
        r"\beta": "β", r"\gamma": "γ", r"\Delta": "Δ", r"\theta": "θ",
        r"\lambda": "λ", r"\sqrt": "√",
    }

    def __init__(self, unicode_renderer: UnicodeTextRenderer | None = None) -> None:
        self.unicode_renderer = unicode_renderer

    def render(self, element: RenderElement) -> dict:
        latex = element.metadata.get("latex")
        mathml = element.metadata.get("mathml")
        representation = "latex" if latex else "mathml" if mathml else "text"
        value = latex or mathml or element.text or ""
        return {
            "element_id": element.element_id,
            "representation": representation,
            "value": value,
            "bbox": {
                "x": element.x, "y": element.y,
                "width": element.width, "height": element.height,
            },
            "render_status": "adapter_required" if representation != "text" else "text_fallback",
        }

    def _latex_to_unicode(self, value: str) -> str:
        result = value
        for source, target in self.SYMBOLS.items():
            result = result.replace(source, target)
        return result.replace("{", "").replace("}", "")

    def draw(self, pdf, element: RenderElement, page_height: float) -> None:
        value = self._latex_to_unicode(str(element.metadata.get("latex") or element.text or ""))
        if not value:
            return
        if self.unicode_renderer and self.unicode_renderer.draw(
            pdf, element.model_copy(update={"text": value}), page_height,
            font_size=min(18, max(8, int(element.height * 0.55))),
        ):
            return
        y = page_height - element.y - min(element.height, 18)
        pdf.setFont("Helvetica", min(12, max(7, element.height * 0.5)))
        pdf.drawString(element.x, y, value)
