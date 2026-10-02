"""Translation adapters and scientific terminology services."""

from backend.translation.factory import create_translation_adapter
from backend.translation.huggingface_adapter import HuggingFaceNllbAdapter

__all__ = ["HuggingFaceNllbAdapter", "create_translation_adapter"]
