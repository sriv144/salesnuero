# Research Log

This file tracks autonomous research and improvement runs against this
repository.

## 2026-04-27 — Auto-Researcher v4

**Resume score at start of run:** 60 / 100 — ranked 5 of 6 in the portfolio.

**Branch:** `claude/compassionate-keller-snPHW` (off `master`).

### Implemented this run

No code changes. This commit only seeded the research log.

### Next-run candidates (priority order)

1. README rewrite with example output (one full prospect profile + email).
2. CI: `npm run build` for frontend + `pytest` for backend.
3. CrewAI agent architecture diagram in README.
4. LICENSE.

## 2026-05-14 — Auto-Researcher v4

**Resume score at start of run:** 60 / 100 — still ranked 5 of 6, but the
zero-implementation status from 2026-04-27 plus a defined CI + LICENSE +
root-`.env.example` backlog make this the cleanest place to land safe wins
this run.

**Branch:** `claude/compassionate-keller-5vVWf` (off `master`).

### Implemented

- **CI workflow** at `.github/workflows/ci.yml` with two parallel jobs:
  - `frontend`: `npm ci` + `npm run lint` (if present) + `npm run build` on
    Node 20, with `NEXT_PUBLIC_API_BASE` set to a localhost placeholder so
    any build-time env reads succeed.
  - `backend`: `pip install -r backend/requirements.txt` on Python 3.11 plus
    `python -m compileall` of `crew_pipeline.py`, `ingest_rag.py`, and
    `app/`. The throwaway `backend/test_env.py` and `backend/test_gemini.py`
    scripts are excluded because they require live API keys; they aren't
    real pytest tests despite the filename.
- **Root `.env.example`** documenting the backend secrets (`ANTHROPIC_API_KEY`,
  `TAVILY_API_KEY`, optional `NVIDIA_API_KEY`) and the frontend's
  `NEXT_PUBLIC_API_BASE`. The previous file lived only under `backend/`, so
  the secret surface wasn't obvious from the repo root. The backend env file
  is preserved.
- **MIT `LICENSE`.**

### Why this was prioritized

The 2026-04-27 next-run list explicitly named: README rewrite, CI, agent
diagram, LICENSE. CI and LICENSE are the two zero-risk items — they touch no
application code and improve signal immediately. The root `.env.example` was
a bonus high-value fix because it surfaces the secret contract on the front
page of the repo without forcing a reader into `backend/`.

README rewrite + CrewAI architecture diagram were deliberately held back: an
authentic walkthrough requires running a real prospect through the agents to
capture sample output, and the architecture diagram needs to follow the
actual agent topology in `crew_pipeline.py`. Both are next-run candidates.

### Evaluated and skipped

- **README rewrite with real prospect example:** needs a redacted real run
  output, which a one-shot autonomous pass cannot produce safely.
- **Replacing `npm run lint` from CI with an `eslint` job that gates on
  errors:** the `frontend/package.json` only ships a placeholder `lint`
  script; gating before the lint config is dialed in would create
  immediate CI red. Used `--if-present` so it runs once a real script
  exists.
- **Adding actual pytest tests for `crew_pipeline.py`:** the pipeline calls
  LLMs at every step. Mocking it properly is a real refactor.

### Next-run candidates

1. README rewrite with one full redacted prospect run — profile + cold
   email + agent trace.
2. CrewAI agent architecture diagram (Mermaid in README is fine).
3. Refactor `crew_pipeline.py` to inject the LLM client so a mocked
   pytest suite can replace today's `compileall`-only backend CI.
4. Frontend ESLint config + a real `lint` script that CI can gate on.
