from abc import ABC, abstractmethod
from dataclasses import dataclass

from backend.schemas.udr import UdrDocument


class DocumentStore(ABC):
    @abstractmethod
    def put(self, tenant_id: str, document_id: str, payload: bytes, content_type: str) -> str: ...
    @abstractmethod
    def get(self, tenant_id: str, document_id: str) -> bytes: ...


class InMemoryDocumentStore(DocumentStore):
    def __init__(self):
        self._items = {}

    def put(self, tenant_id, document_id, payload, content_type):
        self._items[(tenant_id, document_id)] = (payload, content_type)
        return document_id

    def get(self, tenant_id, document_id):
        return self._items[(tenant_id, document_id)][0]


class ModelRegistry(ABC):
    @abstractmethod
    def versions(self) -> dict[str, str]: ...


@dataclass
class StaticModelRegistry(ModelRegistry):
    _versions: dict[str, str]

    def versions(self):
        return dict(self._versions)


class TranslationProvider(ABC):
    @abstractmethod
    def translate(self, document: UdrDocument, target_language: str) -> UdrDocument: ...


class PassthroughTranslationProvider(TranslationProvider):
    def translate(self, document, target_language):
        result = document.model_copy(deep=True)
        result.source.language = target_language
        return result


class ExportProvider(ABC):
    @abstractmethod
    def export(self, document: UdrDocument) -> list[dict]: ...


class ManifestExportProvider(ExportProvider):
    """Pilot-safe artifact contract; real PDF export remains an injected provider."""

    def export(self, document):
        return [{
            "artifact_id": f"{document.document_id}-manifest",
            "format": "udr-json",
            "document_id": str(document.document_id),
        }]
