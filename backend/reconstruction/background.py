from pathlib import Path

from backend.reconstruction.models import RenderPage


class BackgroundResolver:
    """Resolve a source-page raster used as the visual reconstruction baseline."""

    def resolve(self, page: RenderPage) -> Path | None:
        value = page.metadata.get("source_page_path") if hasattr(page, "metadata") else None
        if not value:
            return None
        path = Path(value)
        return path if path.exists() else None
