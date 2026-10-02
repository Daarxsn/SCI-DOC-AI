from dataclasses import dataclass
from hashlib import sha256


@dataclass(frozen=True)
class MemoryEntry:
    source_text: str
    target_text: str
    source_language: str
    target_language: str
    domain: str
    context: str | None = None
    version: str = "1"


class TranslationMemory:
    """Deterministic exact-match translation memory for approved translations."""

    def __init__(self) -> None:
        self._entries: dict[str, MemoryEntry] = {}

    @staticmethod
    def _key(source_text: str, source_language: str, target_language: str, domain: str) -> str:
        raw = "\x1f".join([
            source_language.lower().strip(),
            target_language.lower().strip(),
            domain.lower().strip(),
            source_text.strip(),
        ])
        return sha256(raw.encode("utf-8")).hexdigest()

    def add(self, entry: MemoryEntry) -> str:
        key = self._key(
            entry.source_text,
            entry.source_language,
            entry.target_language,
            entry.domain,
        )
        self._entries[key] = entry
        return key

    def lookup(
        self,
        source_text: str,
        source_language: str,
        target_language: str,
        domain: str,
    ) -> MemoryEntry | None:
        return self._entries.get(
            self._key(source_text, source_language, target_language, domain)
        )

    def __len__(self) -> int:
        return len(self._entries)
