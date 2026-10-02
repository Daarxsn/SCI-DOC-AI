from backend.reconstruction.models import RenderElement


class TableRenderer:
    """Render a UDR table using simple, deterministic PDF primitives."""

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
            "render_status": "grid_adapter_required" if not rows else "ready",
        }

    def draw(self, pdf, element: RenderElement, page_height: float) -> None:
        rows = element.metadata.get("rows", [])
        columns = element.metadata.get("columns", [])
        if not rows and not columns:
            return

        matrix = [columns] + rows if columns else rows
        column_count = max((len(row) for row in matrix), default=0)
        if column_count == 0:
            return

        row_height = element.height / max(len(matrix), 1)
        column_width = element.width / column_count
        top = page_height - element.y

        pdf.setLineWidth(0.5)
        for row_index, row in enumerate(matrix):
            for column_index in range(column_count):
                x = element.x + column_index * column_width
                y = top - (row_index + 1) * row_height
                pdf.rect(x, y, column_width, row_height, stroke=1, fill=0)

                if column_index < len(row) and row[column_index] is not None:
                    value = str(row[column_index])
                    pdf.setFont("Helvetica", min(9, max(6, row_height * 0.45)))
                    pdf.drawString(x + 3, y + row_height * 0.3, value[:80])
