from abc import ABC, abstractmethod
from pathlib import Path

from backend.ocr.models import OcrPageResult


class OcrAdapter(ABC):
    name: str

    @abstractmethod
    def extract(self, image_path: str | Path) -> OcrPageResult:
        """Extract text and coordinates from one page image."""
        raise NotImplementedError
