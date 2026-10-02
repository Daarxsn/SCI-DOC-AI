from backend.reconstruction.models import RenderElement


class EquationRenderer:
    """Render equations without coupling reconstruction to one math engine."""

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
