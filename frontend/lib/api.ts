export class ApiRequestError extends Error {
  code: string;
  status: number;
  retryAfter?: number;

  constructor(code: string, status: number, retryAfter?: number) {
    super(code);
    this.code = code;
    this.status = status;
    this.retryAfter = retryAfter;
  }
}

function csrfToken(): string | undefined {
  return document.cookie
    .split("; ")
    .find((c) => c.startsWith("csrf_token="))
    ?.split("=")[1];
}

async function request<T>(method: "GET" | "POST", path: string, body?: unknown): Promise<T> {
  const headers: Record<string, string> = {};
  if (body !== undefined) headers["Content-Type"] = "application/json";
  const csrf = csrfToken();
  if (method === "POST" && csrf) headers["X-CSRF-Token"] = csrf;

  let response: Response;
  try {
    response = await fetch(`/api/v1${path}`, {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
    });
  } catch {
    throw new ApiRequestError("network", 0);
  }
  if (!response.ok) {
    const data = await response.json().catch(() => null);
    throw new ApiRequestError(
      data?.error?.code ?? "server_error",
      response.status,
      Number(response.headers.get("Retry-After")) || undefined,
    );
  }
  return response.json() as Promise<T>;
}

export const getJson = <T,>(path: string) => request<T>("GET", path);
export const postJson = <T,>(path: string, body?: unknown) => request<T>("POST", path, body);
