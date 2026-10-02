from pathlib import Path

from backend.reconstruction.background import BackgroundResolver
from backend.reconstruction.models import RenderPage


def test_background_resolver_returns_existing_asset(tmp_path):
    source = tmp_path / "page.png"
    source.write_bytes(b"placeholder")

    page = RenderPage(
        page_number=1,
        width=800,
        height=1000,
        metadata={"source_page_path": str(source)},
    )

    assert BackgroundResolver().resolve(page) == source


def test_background_resolver_returns_none_without_asset():
    page = RenderPage(page_number=1, width=800, height=1000)
    assert BackgroundResolver().resolve(page) is None
