from abc import ABC, abstractmethod
from backend.results.models import ResultArtifact
class ArtifactStore(ABC):
    @abstractmethod
    def put(self, artifact:ResultArtifact)->ResultArtifact: ...
    @abstractmethod
    def list(self, document_id:str, tenant_id:str)->list[ResultArtifact]: ...
class InMemoryArtifactStore(ArtifactStore):
    def __init__(self): self._items={}
    def put(self, artifact):
        self._items.setdefault((artifact.tenant_id,artifact.document_id),[]).append(artifact); return artifact
    def list(self, document_id, tenant_id): return list(self._items.get((tenant_id,document_id),[]))
