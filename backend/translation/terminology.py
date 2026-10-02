from dataclasses import dataclass


@dataclass(frozen=True)
class TerminologyEntry:
    source_term: str
    target_term: str
    source_language: str
    target_language: str
    domain: str
    case_sensitive: bool = False
    protected: bool = True
    notes: str | None = None


class TerminologyRegistry:
    def __init__(self) -> None:
        self._entries: list[TerminologyEntry] = []

    def add(self, entry: TerminologyEntry) -> None:
        self._entries = [
            existing for existing in self._entries
            if not (
                existing.source_term == entry.source_term
                and existing.source_language == entry.source_language
                and existing.target_language == entry.target_language
                and existing.domain == entry.domain
            )
        ]
        self._entries.append(entry)

    def find(
        self,
        source_term: str,
        source_language: str,
        target_language: str,
        domain: str,
    ) -> TerminologyEntry | None:
        for entry in reversed(self._entries):
            if (
                entry.source_language == source_language
                and entry.target_language == target_language
                and entry.domain == domain
            ):
                if entry.case_sensitive and entry.source_term == source_term:
                    return entry
                if not entry.case_sensitive and entry.source_term.lower() == source_term.lower():
                    return entry
        return None

    def entries(
        self,
        source_language: str | None = None,
        target_language: str | None = None,
        domain: str | None = None,
    ) -> list[TerminologyEntry]:
        return [
            entry for entry in self._entries
            if (source_language is None or entry.source_language == source_language)
            and (target_language is None or entry.target_language == target_language)
            and (domain is None or entry.domain == domain)
        ]

    def protect_terms(
        self,
        text: str,
        source_language: str,
        target_language: str,
        domain: str,
    ) -> tuple[str, dict[str, str]]:
        replacements: dict[str, str] = {}
        protected = text

        candidates = sorted(
            self.entries(source_language, target_language, domain),
            key=lambda entry: len(entry.source_term),
            reverse=True,
        )

        for index, entry in enumerate(candidates):
            token = f"__SCI_TERM_{index}__"
            if entry.source_term in protected:
                protected = protected.replace(entry.source_term, token)
                replacements[token] = entry.target_term

        return protected, replacements
