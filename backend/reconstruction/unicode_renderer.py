from pathlib import Path
from tempfile import NamedTemporaryFile

from backend.reconstruction.models import RenderElement


class UnicodeTextRenderer:
    """Render Unicode text through Pillow for scripts needing shaping."""

    def __init__(self, font_path: str | None = None) -> None:
        self.font_path = font_path

    def available(self) -> bool:
        return bool(self.font_path and Path(self.font_path).exists())

    def render_image(self, text: str, font_size: int, max_width: int):
        if not self.available():
            raise RuntimeError("A Unicode-capable font_path is required")

        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError as exc:
            raise RuntimeError("Pillow is required for Unicode reconstruction") from exc

        font = ImageFont.truetype(self.font_path, font_size)
        probe = Image.new("RGBA", (max(max_width, 1), max(font_size * 2, 2)), (255, 255, 255, 0))
        draw = ImageDraw.Draw(probe)

        bbox = draw.multiline_textbbox(
            (0, 0), text, font=font, spacing=max(1, font_size // 4)
        )
        width = max(1, min(max_width, bbox[2] - bbox[0] + 8))
        height = max(font_size + 8, bbox[3] - bbox[1] + 8)

        image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        ImageDraw.Draw(image).multiline_text(
            (4, 2),
            text,
            font=font,
            fill=(0, 0, 0, 255),
            spacing=max(1, font_size // 4),
        )

        with NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            image.save(tmp.name, format="PNG")
            return Path(tmp.name), width, height

    def draw(self, pdf, element: RenderElement, page_height: float, font_size: int = 12) -> bool:
        if not element.text or not self.available():
            return False

        image_path, width, height = self.render_image(
            element.text, font_size, max(1, int(element.width))
        )
        y = page_height - element.y - min(element.height, height)

        pdf.drawImage(
            str(image_path),
            element.x,
            y,
            width=min(element.width, width),
            height=min(element.height, height),
            preserveAspectRatio=True,
            anchor="sw",
            mask="auto",
        )
        image_path.unlink(missing_ok=True)
        return True
