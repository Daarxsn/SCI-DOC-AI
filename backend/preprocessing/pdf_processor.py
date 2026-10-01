from pathlib import Path

from backend.preprocessing.models import PageArtifact
from backend.preprocessing.image_processor import ImagePreprocessor


class PdfPreprocessor:
    def __init__(self, target_dpi: int = 300) -> None:
        self.target_dpi = target_dpi
        self.image_processor = ImagePreprocessor(target_dpi=target_dpi)

    def render_pages(
        self,
        *,
        source_path: str | Path,
        output_dir: str | Path,
    ) -> list[PageArtifact]:
        try:
            import fitz
        except ImportError as exc:
            raise RuntimeError("PyMuPDF is required for PDF preprocessing") from exc

        source = Path(source_path)
        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)

        document = fitz.open(source)
        artifacts: list[PageArtifact] = []

        try:
            scale = self.target_dpi / 72
            matrix = fitz.Matrix(scale, scale)

            for index, page in enumerate(document, start=1):
                pixmap = page.get_pixmap(matrix=matrix, alpha=False)
                raw_path = output / f"page-{index:04d}-raw.png"
                processed_path = output / f"page-{index:04d}.png"

                pixmap.save(raw_path)

                artifacts.append(
                    self.image_processor.process(
                        source_path=raw_path,
                        output_path=processed_path,
                        page_number=index,
                    )
                )
        finally:
            document.close()

        return artifacts
