from pathlib import Path

import pytest

from backend.ingestion.file_validator import validate_file_metadata
from backend.ingestion.page_extractor import inspect_image


def test_file_validation_accepts_pdf():
    result = validate_file_metadata("paper.pdf", "application/pdf", 1024)
    assert result.mime_type == "application/pdf"


def test_file_validation_rejects_unknown_type():
    with pytest.raises(ValueError, match="unsupported MIME"):
        validate_file_metadata("paper.txt", "text/plain", 100)


def test_image_inspection(tmp_path: Path):
    pytest.importorskip("PIL")
    from PIL import Image

    image_path = tmp_path / "page.png"
    Image.new("RGB", (800, 600)).save(image_path)

    metadata = inspect_image(image_path)
    assert metadata.page_number == 1
    assert metadata.width == 800
    assert metadata.height == 600
