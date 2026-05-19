# Research Log

A running log of automated research-and-development passes against this
repository. Each entry records the resume-worthiness score at start,
what was implemented, what was evaluated and skipped, and the next-run
candidate list.

## 2026-05-19 — Auto-Researcher v4

**Resume-worthiness score at start of run: 70 / 100** (rank 5 of 6).

| Signal | Score |
| --- | --- |
| Tech stack prestige (CrewAI multi-agent + Next.js + FastAPI + ChromaDB + Tavily) | 19 / 25 |
| Commit recency (updated 2026-05-11) | 22 / 25 |
| Feature completeness (Tavily OSINT + Big Five / DISC + cold-email gen, full FE) | 15 / 20 |
| Stars + visibility (1 star) | 4 / 15 |
| README quality (decent on main; richer rewrites sitting on sibling claude branches) | 10 / 15 |

### Implemented this run (branch: `claude/compassionate-keller-lpd1a`, off `master`)

- **`.github/workflows/ci.yml`.** First CI workflow on this repo. Two
  jobs:
  - `backend-compile-check`: `python -m compileall -q backend` on
    Python 3.11. Deliberately does **not** `pip install` the backend
    requirements — `crewai`, `crewai-tools`, `litellm`, `chromadb`, and
    `sentence-transformers` are heavy and several have known cold-CI
    install pain. Compile-only is the safe first step: it catches
    Python syntax errors, accidental imports of removed modules, and
    typos across `backend/app/**` without risking a flaky first CI run.
  - `frontend-build`: `npm ci` + `npm run build` against `frontend/`
    (Next.js 16 + React 19). Cached on `package-lock.json`.
  Both jobs cancel-in-progress on the same ref and finish well under
  20 minutes total.
- **Seeded this `RESEARCH_LOG.md`.**

### Why this was prioritized

The `claude/compassionate-keller-Quaj7` (2026-05-17) log explicitly listed
the two-job CI workflow as the next-run #2 candidate, and `jnSqo`
(2026-04-28) noted the same gap. salesnuero is the only repo across the
six-target portfolio with **no** CI gate at all today — every other repo
has at least one workflow on an open `claude/*` branch. Closing that gap
is the highest-leverage zero-risk change available.

The scope was tightly bounded:
- The backend job is compile-only, not pytest, because the existing
  backend has no real pytest tests yet (`test_env.py` and `test_gemini.py`
  are env-checks) and pulling in CrewAI on a cold runner is brittle.
- The frontend job builds the existing Next.js 16 app as-is. If the
  upstream Next.js 16 + React 19 toolchain has cold-CI issues, the
  failure will be surfaced loudly and can be fixed in a one-line follow-up
  rather than discovered weeks later by a contributor.

### Evaluated and skipped

- **A real pytest suite + `pytest` step in the backend job.** The
  current `backend/test_env.py` and `backend/test_gemini.py` are
  configuration smoke checks, not unit tests. Writing meaningful
  pytest coverage around `crew_pipeline.py` requires mocking out
  CrewAI's `Crew.kickoff` plus Tavily + LiteLLM — a focused PR, not
  a CI-wiring run.
- **`pip install -r backend/requirements.txt` in CI.** CrewAI and
  ChromaDB have heavy install footprints and several prior
  auto-researcher runs deferred this for the same reason. Once a
  mocked test layer exists, install + pytest can land together.
- **Worked-example README block (redacted prospect input + generated
  profile + final cold email).** Highest-impact README polish, but
  needs a live Tavily + NVIDIA NIM / Anthropic Claude run to produce
  authentic output.
- **LICENSE, Mermaid architecture diagram, root-level `.env.example`.**
  All already implemented on sibling unmerged branches
  (`Quaj7` 2026-05-17 added LICENSE + Mermaid; `jnSqo` 2026-04-28 added
  the root-level `.env.example`). Re-shipping them would violate the
  no-duplicate-work guardrail.
- **Switching CrewAI / LiteLLM to Anthropic Claude.** Touches
  `crew_pipeline.py` and the agent definitions — multi-file behavior
  change that deserves its own dedicated branch.

### Next-run candidates (priority order)

1. Add a mocked pytest layer that exercises `/api/run` and
   `crew_pipeline.py` with a stubbed `Crew.kickoff`, then promote the
   backend CI job from compile-only to `pip install` + `pytest`.
2. Worked-example README block: one redacted prospect input + the
   generated psychological profile + the final cold email side by side.
3. Add an Anthropic-backed CrewAI provider option behind an env-var
   switch alongside the current NVIDIA NIM / OpenAI-compatible path,
   defaulting to `claude-sonnet-4-6`.
4. Add a Dockerfile + docker-compose stack covering both the FastAPI
   backend and the Next.js frontend.
5. Persist run results to SQLite so prospect reports survive restarts.

### Prior research-log context

Previous runs on unmerged `claude/compassionate-keller-*` branches (most
recent first, none merged to `master`):

- `Quaj7` (2026-05-17) — MIT LICENSE + CrewAI Mermaid architecture
  diagram inserted into README.
- `Ow84F` (2026-05-16) — seeded log only; no code.
- `dI8Uk` (2026-04-29) — seeded log only; no code.
- `jnSqo` (2026-04-28) — README expansion (architecture diagram, project
  tree, API surface, configuration table) + top-level `.env.example`.
- `snPHW` (2026-04-27) — seeded log only; no code.
