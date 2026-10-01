from pathlib import Path

import pytest

from backend.preprocessing.image_processor import ImagePreprocessor
from backend.preprocessing.models import ImageMode


def test_image_preprocessor_normalizes_page(tmp_path: Path):
    pil = pytest.importorskip("PIL")
    from PIL import Image

    source = tmp_path / "source.jpg"
    output = tmp_path / "processed.png"

    Image.new("RGB", (1200, 800), (240, 240, 240)).save(source)

    artifact = ImagePreprocessor(target_dpi=300).process(
        source_path=source,
        output_path=output,
    )

    assert output.exists()
    assert artifact.width == 1200
    assert artifact.height == 800
    assert artifact.image_mode == ImageMode.GRAYSCALE
    assert artifact.dpi == 300
    assert "grayscale" in artifact.preprocessing_steps
    assert "autocontrast" in artifact.preprocessing_steps
