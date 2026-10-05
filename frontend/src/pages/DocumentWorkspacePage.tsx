import { useParams } from "react-router-dom";

export function DocumentWorkspacePage() {
  const { documentId } = useParams();
  return (
    <div>
      <p className="eyebrow">Document workspace</p>
      <h1>{documentId ?? "Document"}</h1>
      <p className="lead">OCR, translation, scientific content, validation, review, and reconstruction views will be layered onto this route.</p>
    </div>
  );
}