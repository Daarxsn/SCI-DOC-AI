from pathlib import Path

from backend.reconstruction.models import RenderElement


class ImageRenderer:
    """Resolve and draw image assets referenced by a UDR element."""

    def resolve(self, element: RenderElement) -> Path | None:
        value = element.metadata.get("asset_path") or element.metadata.get("image_path")
        if not value:
            return None
        path = Path(value)
        return path if path.exists() else None

    def render(self, element: RenderElement) -> dict:
        path = self.resolve(element)

        return {
            "element_id": element.element_id,
            "asset_path": str(path) if path else None,
            "bbox": {
                "x": element.x,
                "y": element.y,
                "width": element.width,
                "height": element.height,
            },
            "render_status": "ready" if path else "asset_missing",
        }

    def draw(self, pdf, element: RenderElement, page_height: float) -> None:
        path = self.resolve(element)
        if not path:
            return

        y = page_height - element.y - element.height
        pdf.drawImage(
            str(path),
            element.x,
            y,
            width=element.width,
            height=element.height,
            preserveAspectRatio=True,
            anchor="c",
            mask="auto",
        )
