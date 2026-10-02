from backend.translation.adapter import TranslationAdapter
from backend.translation.memory import TranslationMemory
from backend.translation.models import TranslationLanguage, TranslationStatus, TranslationUnit
from backend.translation.terminology import TerminologyRegistry


class TranslationService:
    def __init__(
        self,
        adapter: TranslationAdapter,
        terminology: TerminologyRegistry | None = None,
        memory: TranslationMemory | None = None,
    ) -> None:
        self.adapter = adapter
        self.terminology = terminology or TerminologyRegistry()
        self.memory = memory or TranslationMemory()

    def translate(
        self,
        source_text: str,
        source_language: TranslationLanguage,
        target_language: TranslationLanguage,
        domain: str,
        element_type: str = "paragraph",
    ) -> TranslationUnit:
        memory_entry = self.memory.lookup(
            source_text,
            source_language.value,
            target_language.value,
            domain,
        )

        if memory_entry:
            return TranslationUnit(
                source_text=source_text,
                target_text=memory_entry.target_text,
                source_language=source_language,
                target_language=target_language,
                status=TranslationStatus.TRANSLATED,
                confidence=1.0,
                terminology_ids=[],
                metadata={"source": "translation_memory", "memory_version": memory_entry.version},
            )

        protected_text, replacements = self.terminology.protect_terms(
            source_text,
            source_language.value,
            target_language.value,
            domain,
        )

        result = self.adapter.translate(
            protected_text,
            source_language=source_language,
            target_language=target_language,
            domain=domain,
            element_type=element_type,
        )

        translated = result.target_text
        for token, target_term in replacements.items():
            translated = translated.replace(token, target_term)

        result.target_text = translated
        result.terminology_ids = list(replacements.values())

        return result
