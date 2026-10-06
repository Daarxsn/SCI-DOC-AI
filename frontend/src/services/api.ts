export type ApiConfig = {
  baseUrl: string;
  apiKey?: string;
};

export type HealthResponse = {
  status: string;
  service: string;
};

export type ReadinessResponse = {
  status: string;
  service: string;
  checks: Record<string, boolean>;
  errors: string[];
};

export type RuntimeResponse = {
  service: string;
  [key: string]: unknown;
};

export type UploadPage = {
  page_number: number;
  mime_type?: string | null;
  size_bytes?: number | null;
  [key: string]: unknown;
};

export type UploadResponse = {
  status: string;
  filename: string;
  mime_type?: string | null;
  size_bytes: number;
  pages: UploadPage[];
};

export type JobStatusResponse = {
  job_id: string;
  status: string;
  progress: number;
  stage: string;
  error?: string | null;
};

export type ResultArtifact = {
  tenant_id: string;
  document_id: string;
  artifact_id: string;
  format: string;
  path: string;
  size_bytes: number;
  checksum?: string | null;
};

export type ResultResponse = {
  document_id: string;
  status: string;
  artifacts: ResultArtifact[];
};

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export const apiConfig: ApiConfig = {
  baseUrl: normalizeBaseUrl(import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000"),
  apiKey: import.meta.env.VITE_API_KEY || undefined,
};

function normalizeBaseUrl(value: string): string {
  const trimmed = value.trim();
  if (!trimmed) throw new Error("VITE_API_BASE_URL must not be empty.");
  try {
    const url = new URL(trimmed);
    if (!["http:", "https:"].includes(url.protocol)) throw new Error("Unsupported API URL protocol.");
    return url.toString().replace(/\/$/, "");
  } catch {
    throw new Error("VITE_API_BASE_URL must be a valid HTTP(S) URL.");
  }
}

async function parseError(response: Response): Promise<string> {
  try {
    const body = (await response.json()) as { detail?: string };
    return body.detail ?? `Request failed with status ${response.status}`;
  } catch {
    return `Request failed with status ${response.status}`;
  }
}

export async function apiFetch<T>(
  path: string,
  init: RequestInit = {},
): Promise<T> {
  const headers = new Headers(init.headers);
  if (apiConfig.apiKey) headers.set("X-API-Key", apiConfig.apiKey);
  if (init.body && !(init.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(new URL(path, apiConfig.baseUrl), {
    ...init,
    headers,
  });

  if (!response.ok) {
    throw new ApiError(await parseError(response), response.status);
  }

  return response.json() as Promise<T>;
}

export const api = {
  health: () => apiFetch<HealthResponse>("/health"),
  ready: () => apiFetch<ReadinessResponse>("/ready"),
  runtime: () => apiFetch<RuntimeResponse>("/runtime"),

  uploadDocument: (file: File) => {
    const body = new FormData();
    body.append("file", file);
    return apiFetch<UploadResponse>("/api/v1/documents/upload", {
      method: "POST",
      body,
    });
  },

  createJob: (request: {
    document_id: string;
    target_language: string;
    domain: string;
    idempotency_key?: string;
  }) =>
    apiFetch<JobStatusResponse>("/v1/jobs", {
      method: "POST",
      body: JSON.stringify(request),
    }),

  getJob: (jobId: string) => apiFetch<JobStatusResponse>(`/v1/jobs/${jobId}`),

  getResults: (documentId: string) =>
    apiFetch<ResultResponse>(`/v1/documents/${documentId}/results`),
};
