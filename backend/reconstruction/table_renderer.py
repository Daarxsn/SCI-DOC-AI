from backend.reconstruction.models import RenderElement


class TableRenderer:
    """Normalize UDR table data into a renderer-independent grid."""

    def render(self, element: RenderElement) -> dict:
        rows = element.metadata.get("rows", [])
        columns = element.metadata.get("columns", [])

        return {
            "element_id": element.element_id,
            "columns": columns,
            "rows": rows,
            "bbox": {
                "x": element.x,
                "y": element.y,
                "width": element.width,
                "height": element.height,
            },
            "render_status": "grid_adapter_required",
        }
