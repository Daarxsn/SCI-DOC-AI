from backend.reconstruction.models import RenderElement


class EquationRenderer:
    """Render equations with a deterministic text fallback.

    A future MathJax/LaTeX renderer can replace draw() without changing UDR.
    """

    def render(self, element: RenderElement) -> dict:
        latex = element.metadata.get("latex")
        mathml = element.metadata.get("mathml")

        if latex:
            representation = "latex"
            value = latex
        elif mathml:
            representation = "mathml"
            value = mathml
        else:
            representation = "text"
            value = element.text or ""

        return {
            "element_id": element.element_id,
            "representation": representation,
            "value": value,
            "bbox": {
                "x": element.x,
                "y": element.y,
                "width": element.width,
                "height": element.height,
            },
            "render_status": "adapter_required" if representation != "text" else "text_fallback",
        }

    def draw(self, pdf, element: RenderElement, page_height: float) -> None:
        value = element.metadata.get("latex") or element.text
        if not value:
            return

        # Explicit fallback: draw source/math text rather than silently
        # pretending that LaTeX has been typeset.
        y = page_height - element.y - min(element.height, 18)
        pdf.setFont("Helvetica", min(12, max(7, element.height * 0.5)))
        pdf.drawString(element.x, y, str(value))
