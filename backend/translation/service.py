from uuid import uuid4
from backend.translation.adapter import TranslationAdapter
from backend.translation.memory import TranslationMemory
from backend.translation.models import TranslationLanguage, TranslationStatus, TranslationUnit
from backend.translation.terminology import TerminologyRegistry

class TranslationService:
    def __init__(self, adapter: TranslationAdapter, terminology=None, memory=None) -> None:
        self.adapter = adapter
        self.terminology = terminology or TerminologyRegistry()
        self.memory = memory or TranslationMemory()

    def translate(self, source_text: str, source_language: TranslationLanguage, target_language: TranslationLanguage, domain: str, element_type: str = "paragraph") -> TranslationUnit:
        memory_entry = self.memory.lookup(source_text, source_language.value, target_language.value, domain)
        if memory_entry:
            return TranslationUnit(unit_id=str(uuid4()), source_text=source_text, target_text=memory_entry.target_text, source_language=source_language, target_language=target_language, status=TranslationStatus.TRANSLATED, confidence=1.0, metadata={"source": "translation_memory", "memory_version": memory_entry.version})
        protected_text, replacements = self.terminology.protect_terms(source_text, source_language.value, target_language.value, domain)
        translated, confidence = self.adapter.translate(protected_text, source_language=source_language, target_language=target_language, context=element_type)
        for token, target_term in replacements.items():
            translated = translated.replace(token, target_term)
        status = TranslationStatus.TRANSLATED if confidence >= 0.8 else TranslationStatus.REVIEW
        return TranslationUnit(unit_id=str(uuid4()), source_text=source_text, target_text=translated, source_language=source_language, target_language=target_language, status=status, confidence=confidence, terminology_ids=list(replacements.values()), metadata={"source": self.adapter.name, "element_type": element_type})
