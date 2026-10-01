from pathlib import Path

from backend.preprocessing.image_processor import ImagePreprocessor
from backend.preprocessing.models import PageArtifact
from backend.preprocessing.pdf_processor import PdfPreprocessor


class PreprocessingService:
    def __init__(self, target_dpi: int = 300) -> None:
        self.image_processor = ImagePreprocessor(target_dpi=target_dpi)
        self.pdf_processor = PdfPreprocessor(target_dpi=target_dpi)

    def process(
        self,
        *,
        source_path: str | Path,
        mime_type: str,
        output_dir: str | Path,
    ) -> list[PageArtifact]:
        source = Path(source_path)

        if mime_type == "application/pdf":
            return self.pdf_processor.render_pages(
                source_path=source,
                output_dir=output_dir,
            )

        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)

        return [
            self.image_processor.process(
                source_path=source,
                output_path=output / "page-0001.png",
            )
        ]
