from pathlib import Path

from backend.ingestion.file_validator import validate_file_metadata
from backend.ingestion.page_extractor import PageMetadata, inspect_image, inspect_pdf


class IngestionProcessor:
    def inspect(
        self,
        *,
        path: str | Path,
        filename: str,
        mime_type: str,
        size_bytes: int,
    ) -> list[PageMetadata]:
        validate_file_metadata(filename, mime_type, size_bytes)

        if mime_type == "application/pdf":
            return inspect_pdf(path)

        return [inspect_image(path)]
