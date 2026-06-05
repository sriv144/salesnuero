# Research Log

This file tracks Auto-Researcher passes against this repository: what was
implemented, what was evaluated and skipped, and what is queued for next run.

## 2026-06-05 — Auto-Researcher v4

**Resume score at start of run:** 52 / 100

SalesNeuro already had a respectable README, a working CrewAI multi-agent
pipeline, and a Next.js frontend — but no LICENSE and no CI signal. Those
are cheap, high-trust additions that materially improve the public-facing
impression of the repo without touching agent code.

### Implemented (branch `claude/compassionate-keller-eZfYm`)

- `LICENSE` (MIT) at the repo root so the project is legally usable.
- `.github/workflows/ci.yml` with two parallel jobs:
    - **backend-lint**: ruff `E9,F63,F7,F82` over `backend/` — catches
      real syntax / undefined-name bugs without forcing a style overhaul.
    - **frontend-lint**: `npm ci` + `npm run lint` against `frontend/`
      using the existing eslint config and `package-lock.json` cache.

### Why this was prioritized

The repository already presents well in the README; the missing pieces
were the two universal trust signals reviewers scan for first — a LICENSE
file and a green CI badge. Both are zero-risk additions: no production
code changes, no behavioral changes, no new dependencies that affect
runtime. Maximum legitimacy per byte changed.

### Evaluated and skipped

- **Add a root-level `.env.example`.** The repo already ships
  `backend/.env.example`, which is where the README points readers. A
  duplicate at the root would create a second source of truth for the
  same keys and drift over time. Skipped — the existing layout is fine.
- **Add a `Dockerfile` / `docker-compose.yml`.** The README has a clear
  two-terminal local dev story but no containerized path. Real value, but
  the backend has CrewAI + Chroma + Tavily + an LLM provider, and the
  frontend is Next.js — a half-baked image risks shipping a broken build.
  Deferred to a dedicated branch where it can be tested end-to-end.
- **Replace stray `test_env.py` / `test_gemini.py` smoke scripts with
  proper pytest tests under `backend/tests/`.** Useful refactor, but it
  changes the meaning of "tests" in this repo and is therefore not safe
  to ship sight-unseen.

### Candidates for next run

1. Add a `Dockerfile` for `backend/` and a top-level `docker-compose.yml`
   wiring backend + frontend + Chroma so reviewers can `docker compose up`.
2. Migrate `backend/test_env.py` and `backend/test_gemini.py` into a
   proper `backend/tests/` pytest layout and wire pytest into the CI.
3. Add an architecture diagram (mermaid) to the README showing the
   CrewAI agent graph from Tavily research → OCEAN/DISC profiling →
   personalized outreach generation.
4. Add screenshots of the Next.js UI to the README to lift the showcase.
