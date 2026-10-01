from pathlib import Path

from backend.layout.document_builder import OcrDocumentBuilder
from backend.ocr.base import OcrAdapter
from backend.preprocessing.image_processor import ImagePreprocessor
from backend.schemas.udr import UdrDocument


class OcrToUdrPipeline:
    def __init__(
        self,
        *,
        ocr_adapter: OcrAdapter,
        preprocessor: ImagePreprocessor | None = None,
        document_builder: OcrDocumentBuilder | None = None,
    ) -> None:
        self.ocr_adapter = ocr_adapter
        self.preprocessor = preprocessor
        self.document_builder = document_builder or OcrDocumentBuilder()

    def process_pages(
        self,
        *,
        image_paths: list[str | Path],
        document_type: str,
        source_language: str,
        mime_type: str,
        domain: str,
    ) -> UdrDocument:
        results = []

        for image_path in image_paths:
            path = Path(image_path)
            if self.preprocessor:
                processed_path = path.with_name(f"{path.stem}-ocr.png")
                self.preprocessor.process(
                    source_path=path,
                    output_path=processed_path,
                )
                path = processed_path

            results.append(self.ocr_adapter.extract(path))

        return self.document_builder.build_document(
            document_type=document_type,
            source_language=source_language,
            mime_type=mime_type,
            domain=domain,
            pages=results,
        )
