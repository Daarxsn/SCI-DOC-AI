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


DEFAULT_TERMS = {
    ("en", "hi", "mathematics"): {"matrix": "आव्यूह", "vector": "सदिश", "integral": "समाकल"},
    ("en", "mr", "mathematics"): {"matrix": "आव्यूह", "vector": "सदिश", "integral": "समाकल"},
    ("en", "hi", "physics"): {"velocity": "वेग", "acceleration": "त्वरण", "force": "बल", "momentum": "संवेग"},
    ("en", "mr", "physics"): {"velocity": "वेग", "acceleration": "त्वरण", "force": "बल", "momentum": "संवेग"},
    ("en", "hi", "biology"): {"cell": "कोशिका", "tissue": "ऊतक", "photosynthesis": "प्रकाश संश्लेषण", "mitochondria": "माइटोकॉन्ड्रिया"},
    ("en", "mr", "biology"): {"cell": "पेशी", "tissue": "ऊतक", "photosynthesis": "प्रकाशसंश्लेषण", "mitochondria": "माइटोकॉन्ड्रिया"},
}


class TerminologyRegistry:
    def __init__(self, entries=None, load_defaults: bool = True) -> None:
        self._entries: list[TerminologyEntry] = []
        if load_defaults:
            for (source, target, domain), terms in DEFAULT_TERMS.items():
                for source_term, target_term in terms.items():
                    self.add(TerminologyEntry(source_term, target_term, source, target, domain))

        for entry in entries or []:
            self.add(entry)

    def add(self, entry: TerminologyEntry) -> None:
        self._entries = [existing for existing in self._entries if not (
            existing.source_term == entry.source_term and existing.source_language == entry.source_language
            and existing.target_language == entry.target_language and existing.domain == entry.domain
        )]
        self._entries.append(entry)

    def find(self, source_term, source_language, target_language, domain):
        for entry in reversed(self._entries):
            if entry.source_language == source_language and entry.target_language == target_language and entry.domain == domain:
                if entry.case_sensitive and entry.source_term == source_term:
                    return entry
                if not entry.case_sensitive and entry.source_term.lower() == source_term.lower():
                    return entry
        return None

    def entries(self, source_language=None, target_language=None, domain=None):
        return [e for e in self._entries if
                (source_language is None or e.source_language == source_language) and
                (target_language is None or e.target_language == target_language) and
                (domain is None or e.domain == domain)]

    def protect_terms(self, text, source_language, target_language, domain):
        replacements = {}
        protected = text
        candidates = sorted(self.entries(source_language, target_language, domain),
                            key=lambda entry: len(entry.source_term), reverse=True)
        for index, entry in enumerate(candidates):
            token = f"__SCI_TERM_{index}__"
            if entry.source_term.lower() in protected.lower():
                import re
                pattern = re.compile(re.escape(entry.source_term), 0 if entry.case_sensitive else re.IGNORECASE)
                protected = pattern.sub(token, protected, count=1)
                replacements[token] = entry.target_term
        return protected, replacements
