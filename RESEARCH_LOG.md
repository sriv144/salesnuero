# Research Log

This log tracks autonomous-research / auto-improvement passes over the
repository. Each entry records what was scored, what was implemented,
and what was deliberately skipped, so future runs can avoid re-doing
work that has already shipped.

## 2026-06-02 — Auto-Researcher v4

> Note: this repo's default branch is `master`, not `main`. Auto-
> researcher branches were created from `master`.

### Resume-worthiness score at start of run

`71 / 100` — ranked #5 of 6.

Breakdown:

- Tech stack prestige: 19 / 25 — CrewAI multi-agent system, LiteLLM,
  ChromaDB, Tavily OSINT, Next.js + React + Tailwind frontend.
- Commit recency: 18 / 25.
- Feature completeness: 16 / 20 — OSINT, Big Five / DISC profiling,
  RAG corpus, FastAPI `/api/run` execution endpoint.
- Stars / visibility: 7 / 15.
- README quality: 11 / 15 — Quick-start works, but no architecture
  diagram, no API contract beyond "see Swagger", no screenshots.

### Implemented on branch `claude/compassionate-keller-MN9a4`

- **docs: seed this `RESEARCH_LOG.md`.** No code or CI changes this
  pass.

### Evaluated and skipped

- Adding a unified CI workflow. Skipped this run because the repo is
  split across `backend/` (Python + CrewAI + LiteLLM + Chroma) and
  `frontend/` (Next.js + npm), each of which needs its own job,
  cache key, and lockfile assumptions. Also, `ingest_rag.py` is
  documented as a required pre-flight step; whether it works without
  network in CI needs to be verified before wiring it in. Queued.
- Migrating LiteLLM → NVIDIA NIM calls to direct Anthropic Claude
  calls. Skipped — changes per-agent prompt behavior in the CrewAI
  pipeline and needs A/B comparison.
- Touching any `backend/` or `frontend/` source. Skipped to keep this
  commit risk-free.

### Candidates for next run

1. Add a backend CI job: `pip install -r backend/requirements.txt`,
   `python -m compileall backend`, and (once verified hermetic)
   `pytest`.
2. Add a frontend CI job: `npm ci` and `npm run build` in
   `frontend/`, with the npm cache keyed on `package-lock.json`.
3. Add `.env.example` files at both `backend/.env.example` and a
   root-level note pointing at them, so the README's `TAVILY_API_KEY`
   / `NVIDIA_API_KEY` setup is self-documenting.
4. Add a Claude-based agent provider (`anthropic` SDK via LiteLLM's
   Anthropic adapter) so the project does not single-source on
   NVIDIA NIM.
5. Architecture diagram + screenshots in the README — a CrewAI
   pipeline visualization would meaningfully lift the visibility
   score.
