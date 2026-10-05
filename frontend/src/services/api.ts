export type ApiConfig = {
  baseUrl: string;
};

export const apiConfig: ApiConfig = {
  baseUrl: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000",
};

export async function apiFetch<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const response = await fetch(new URL(path, apiConfig.baseUrl), init);
  if (!response.ok) {
    throw new Error(`SCI-DOC AI API request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export type HealthResponse = {
  status: string;
  service: string;
};

export const api = {
  health: () => apiFetch<HealthResponse>("/health"),
};