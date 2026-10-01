from pydantic import BaseModel, Field


class TerminologyEntry(BaseModel):
    term_id: str
    source_term: str
    target_term: str
    language: str
    domain: str
    preserve_original: bool = False
    notes: str | None = None


class TerminologyRegistry:
    def __init__(self, entries: list[TerminologyEntry] | None = None) -> None:
        self.entries = entries or []

    def add(self, entry: TerminologyEntry) -> None:
        self.entries.append(entry)

    def find(self, term: str, *, language: str, domain: str) -> list[TerminologyEntry]:
        normalized = term.casefold().strip()

        return [
            entry
            for entry in self.entries
            if entry.language == language
            and entry.domain == domain
            and entry.source_term.casefold().strip() == normalized
        ]

    def apply(self, text: str, *, language: str, domain: str) -> tuple[str, list[str]]:
        used: list[str] = []
        result = text

        for entry in self.entries:
            if entry.language != language or entry.domain != domain:
                continue

            if entry.source_term.casefold() in result.casefold():
                if entry.preserve_original:
                    continue

                result = result.replace(entry.source_term, entry.target_term)
                used.append(entry.term_id)

        return result, used
