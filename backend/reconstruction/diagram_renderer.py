from backend.reconstruction.models import RenderElement


class DiagramRenderer:
    """Build a render plan from the structured diagram graph in UDR."""

    def render(self, element: RenderElement) -> dict:
        objects = element.metadata.get("objects", [])
        labels = element.metadata.get("labels", [])
        relationships = element.metadata.get("relationships", [])

        return {
            "element_id": element.element_id,
            "domain": element.metadata.get("domain", "general"),
            "objects": objects,
            "labels": labels,
            "relationships": relationships,
            "bbox": {
                "x": element.x,
                "y": element.y,
                "width": element.width,
                "height": element.height,
            },
            "render_status": "adapter_required",
        }
