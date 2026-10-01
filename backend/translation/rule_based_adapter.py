from backend.translation.adapter import TranslationAdapter
from backend.translation.models import TranslationLanguage


class RuleBasedAdapter(TranslationAdapter):
    """Deterministic development adapter.

    This is deliberately not positioned as production-quality translation.
    It provides predictable behavior for pipeline and integration testing.
    """

    name = "rule-based-dev"

    def translate(
        self,
        text: str,
        *,
        source_language: TranslationLanguage,
        target_language: TranslationLanguage,
        context: str | None = None,
    ) -> tuple[str, float]:
        if source_language == target_language:
            return text, 1.0

        # Preserve source text when no translation model is configured.
        # Downstream code can still exercise validation/review workflows.
        return text, 0.1
