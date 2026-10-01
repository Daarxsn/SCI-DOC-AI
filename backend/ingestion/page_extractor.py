from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PageMetadata:
    page_number: int
    width: int
    height: int


def inspect_image(path: str | Path) -> PageMetadata:
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("Pillow is required for image inspection") from exc

    with Image.open(path) as image:
        width, height = image.size

    return PageMetadata(page_number=1, width=width, height=height)


def inspect_pdf(path: str | Path) -> list[PageMetadata]:
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("PyMuPDF is required for PDF inspection") from exc

    document = fitz.open(path)
    try:
        return [
            PageMetadata(
                page_number=index + 1,
                width=float(page.rect.width),
                height=float(page.rect.height),
            )
            for index, page in enumerate(document)
        ]
    finally:
        document.close()
