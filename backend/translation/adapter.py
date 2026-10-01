from abc import ABC, abstractmethod

from backend.translation.models import TranslationLanguage


class TranslationAdapter(ABC):
    name: str

    @abstractmethod
    def translate(
        self,
        text: str,
        *,
        source_language: TranslationLanguage,
        target_language: TranslationLanguage,
        context: str | None = None,
    ) -> tuple[str, float]:
        """Return translated text and confidence."""
        raise NotImplementedError
