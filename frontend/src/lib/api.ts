import type { RunRequest, RunResponse, RunResult } from "./types";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function runPipeline(request: RunRequest): Promise<RunResponse> {
  const res = await fetch(`${BASE_URL}/api/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return res.json();
}

export async function listProspects(): Promise<RunResult[]> {
  const res = await fetch(`${BASE_URL}/api/prospects`);
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return res.json();
}
