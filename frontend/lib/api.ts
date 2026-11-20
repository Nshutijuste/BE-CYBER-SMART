export class ApiRequestError extends Error {
  code: string;
  status: number;

  constructor(code: string, status: number) {
    super(code);
    this.code = code;
    this.status = status;
  }
}

export async function postJson<T>(path: string, body: unknown): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`/api/v1${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  } catch {
    throw new ApiRequestError("network", 0);
  }
  if (!response.ok) {
    const data = await response.json().catch(() => null);
    throw new ApiRequestError(data?.error?.code ?? "server_error", response.status);
  }
  return response.json() as Promise<T>;
}
