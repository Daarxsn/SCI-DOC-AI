"""OCR adapters and services."""

from backend.ocr.factory import create_ocr_adapter
from backend.ocr.paddle_adapter import PaddleOcrAdapter

__all__ = ["PaddleOcrAdapter", "create_ocr_adapter"]
