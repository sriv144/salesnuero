import type {
  RunRequest,
  RunResponse,
  RunResult,
  JobSubmitResponse,
  JobStatusResponse,
  JobListItem,
} from "./types";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

/** Poll interval in milliseconds */
const POLL_INTERVAL_MS = 3000;
/** Max time to wait for a job to complete before giving up (10 minutes) */
const POLL_TIMEOUT_MS = 10 * 60 * 1000;


// ── v1 backward-compat ─────────────────────────────────────────────────────────

export async function listProspects(): Promise<RunResult[]> {
  const res = await fetch(`${BASE_URL}/api/prospects`);
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return res.json();
}

export async function getProspect(name: string): Promise<RunResponse> {
  const res = await fetch(`${BASE_URL}/api/prospects/${encodeURIComponent(name)}`);
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return res.json();
}


// ── v2 async job API ───────────────────────────────────────────────────────────

/**
 * Submit a pipeline job. Returns immediately with job_id.
 * The backend processes the pipeline asynchronously.
 */
export async function submitJob(request: RunRequest): Promise<JobSubmitResponse> {
  const res = await fetch(`${BASE_URL}/api/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Submit error ${res.status}: ${text}`);
  }
  return res.json();
}

/**
 * Poll job status once.
 */
export async function getJobStatus(jobId: string): Promise<JobStatusResponse> {
  const res = await fetch(`${BASE_URL}/api/jobs/${encodeURIComponent(jobId)}`);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Status error ${res.status}: ${text}`);
  }
  return res.json();
}

/**
 * List all jobs (newest first).
 */
export async function listJobs(limit = 50): Promise<JobListItem[]> {
  const res = await fetch(`${BASE_URL}/api/jobs?limit=${limit}`);
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return res.json();
}

/**
 * Submit a job and poll until it completes or fails.
 * Calls onStatus on each poll so the UI can update elapsed time / status.
 *
 * Returns a RunResponse for backward compatibility with existing UI code.
 */
export async function runPipeline(
  request: RunRequest,
  onStatus?: (status: JobStatusResponse) => void,
): Promise<RunResponse> {
  // 1. Submit
  const submit = await submitJob(request);
  const jobId = submit.job_id;

  // 2. Poll
  const deadline = Date.now() + POLL_TIMEOUT_MS;
  while (Date.now() < deadline) {
    await delay(POLL_INTERVAL_MS);
    const status = await getJobStatus(jobId);

    if (onStatus) onStatus(status);

    if (status.status === "completed") {
      return { status: "success", result: status.result, error: null };
    }
    if (status.status === "failed") {
      return { status: "error", result: null, error: status.error ?? "Pipeline failed" };
    }
    // still pending or running — keep polling
  }

  return {
    status: "error",
    result: null,
    error: "Pipeline timed out after 10 minutes. Check /api/jobs for status.",
  };
}

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
