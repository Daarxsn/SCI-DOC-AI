import { useRef, useState } from "react";
import { Badge, Button, Card } from "../components/ui";
import { ApiError, api, type UploadResponse } from "../services/api";

const MAX_FILE_SIZE = 50 * 1024 * 1024;
const ACCEPTED_TYPES = new Set([
  "application/pdf",
  "image/png",
  "image/jpeg",
  "image/tiff",
  "image/webp",
]);

export function DocumentsPage() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [result, setResult] = useState<UploadResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);

  const validate = (file: File) => {
    if (file.size > MAX_FILE_SIZE) return "File exceeds the 50 MB upload limit.";
    if (!ACCEPTED_TYPES.has(file.type)) return "Unsupported file type. Use PDF, PNG, JPEG, TIFF, or WebP.";
    return null;
  };

  const selectFile = (file?: File) => {
    if (!file) return;
    setResult(null);
    const validationError = validate(file);
    if (validationError) {
      setSelectedFile(null);
      setError(validationError);
      return;
    }
    setSelectedFile(file);
    setError(null);
  };

  const upload = async () => {
    if (!selectedFile) return;
    setUploading(true);
    setError(null);
    try {
      const response = await api.uploadDocument(selectedFile);
      setResult(response);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Unable to upload the document.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <header className="page-header">
        <p className="eyebrow">Document intake</p>
        <h1>Upload a scientific document</h1>
        <p className="lead">
          Submit a source document to the SCI-DOC AI ingestion API. The current
          backend inspects the uploaded file and returns accepted metadata and page information.
        </p>
      </header>

      <Card className="upload-card">
        <div
          className="upload-dropzone"
          role="button"
          tabIndex={0}
          onClick={() => inputRef.current?.click()}
          onKeyDown={(event) => {
            if (event.key === "Enter" || event.key === " ") inputRef.current?.click();
          }}
        >
          <div className="upload-icon" aria-hidden="true">↑</div>
          <strong>{selectedFile ? selectedFile.name : "Choose a document"}</strong>
          <span>PDF, PNG, JPEG, TIFF, or WebP · up to 50 MB</span>
          <input
            ref={inputRef}
            type="file"
            accept=".pdf,.png,.jpg,.jpeg,.tif,.tiff,.webp"
            hidden
            onChange={(event) => selectFile(event.target.files?.[0])}
          />
        </div>

        {selectedFile ? (
          <div className="upload-selection">
            <div>
              <strong>{selectedFile.name}</strong>
              <span>{formatBytes(selectedFile.size)} · {selectedFile.type || "unknown type"}</span>
            </div>
            <Badge tone="success">Validated</Badge>
          </div>
        ) : null}

        {error ? (
          <div className="status-panel status-panel--error" role="alert">
            <strong>Upload unavailable</strong>
            <p>{error}</p>
          </div>
        ) : null}

        <div className="page-actions">
          <Button
            size="lg"
            onClick={() => void upload()}
            disabled={!selectedFile || uploading}
          >
            {uploading ? "Uploading…" : "Upload and inspect"}
          </Button>
          {selectedFile ? (
            <Button
              variant="ghost"
              onClick={() => {
                setSelectedFile(null);
                setResult(null);
                setError(null);
                if (inputRef.current) inputRef.current.value = "";
              }}
              disabled={uploading}
            >
              Clear
            </Button>
          ) : null}
        </div>
      </Card>

      {result ? <UploadResult result={result} /> : null}
    </div>
  );
}

function UploadResult({ result }: { result: UploadResponse }) {
  return (
    <section className="upload-result">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Ingestion response</p>
          <h2>Document accepted</h2>
        </div>
        <Badge tone="success">{result.status}</Badge>
      </div>

      <div className="system-grid">
        <Card>
          <div className="system-card__label">Filename</div>
          <div className="system-card__value upload-value">{result.filename}</div>
        </Card>
        <Card>
          <div className="system-card__label">File size</div>
          <div className="system-card__value">{formatBytes(result.size_bytes)}</div>
        </Card>
        <Card>
          <div className="system-card__label">Inspected pages</div>
          <div className="system-card__value">{result.pages.length}</div>
        </Card>
      </div>

      {result.pages.length ? (
        <Card className="page-list">
          <div className="section-heading">
            <h3>Page inspection</h3>
            <Badge tone="info">{result.pages.length} pages</Badge>
          </div>
          <div className="page-list__items">
            {result.pages.map((page) => (
              <div className="page-row" key={page.page_number}>
                <strong>Page {page.page_number}</strong>
                <span>{page.mime_type ?? "Metadata returned by backend"}</span>
                {page.size_bytes != null ? <span>{formatBytes(page.size_bytes)}</span> : null}
              </div>
            ))}
          </div>
        </Card>
      ) : null}

      <p className="result-note">
        The current upload contract does not return a document ID. Job creation and
        document workspace lifecycle will be connected when the backend exposes that identifier.
      </p>
    </section>
  );
}

function formatBytes(bytes: number) {
  if (bytes < 1024) return `${bytes} B`;
  const units = ["KB", "MB", "GB"];
  let value = bytes / 1024;
  let unit = units[0];
  for (let index = 1; value >= 1024 && index < units.length; index += 1) {
    value /= 1024;
    unit = units[index];
  }
  return `${value.toFixed(value >= 10 ? 0 : 1)} ${unit}`;
}
