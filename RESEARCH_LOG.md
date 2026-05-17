# Research Log

This file tracks autonomous research and improvement runs against this
repository.

## 2026-05-17 — Auto-Researcher v4

**Resume-worthiness score at start of run: 72 / 100** (rank 5 of 6).

| Signal | Score |
| --- | --- |
| Tech stack prestige (CrewAI multi-agent + Next.js + FastAPI + ChromaDB) | 19 / 25 |
| Commit recency (updated 2026-05-11) | 22 / 25 |
| Feature completeness (Tavily OSINT + Big Five / DISC + cold-email gen) | 15 / 20 |
| Stars + visibility | 5 / 15 |
| README quality (short, no diagram, no LICENSE) | 11 / 15 |

### Implemented this run (branch: `claude/compassionate-keller-Quaj7`, off `master`)

- **docs(LICENSE): add MIT LICENSE.** Was the top open snPHW next-run
  candidate. Zero-risk and matches the rest of the portfolio's posture.
  Linked from a new `## License` section in the README.
- **docs(readme): CrewAI agent architecture diagram.** Inserted a new
  `## Architecture` section between Features and Prerequisites with a Mermaid
  `flowchart LR` covering `/api/run` -> CrewAI orchestrator -> OSINT,
  profiler, and copywriter agents -> ChromaDB RAG + LiteLLM completions ->
  personalized email response. The remaining README sections (Features,
  Prerequisites, Running Locally, Using The API Direct) are preserved
  verbatim.

### Why this was prioritized

The snPHW research log called out the weak README as the biggest single
resume lever for this repo. A Mermaid diagram makes the multi-agent story
legible without reading source, and LICENSE removes the "can I even use
this?" friction. Both are pure docs and ship safely without a local run.

Kept narrowly scoped because the bigger snPHW recommendation — a worked
example with a redacted prospect profile and the resulting email — needs a
live run to produce.

### Evaluated and skipped

- **README walkthrough with one redacted prospect + resulting cold email.**
  Needs a live Tavily + NVIDIA NIM run to produce authentic output. Worth
  doing once those keys are at hand.
- **CI workflow (`npm run build` + `pytest`).** Two-job workflow is straight
  forward but needs a verification pass to confirm Next.js and pytest
  install cleanly in CI before committing to it.
- **Root-level `.env.example`.** Backend already has one; a root-level
  duplicate could drift. Decided to leave a single source of truth.

### Next-run candidates

1. Worked-example README block: one redacted prospect input + the generated
   psychological profile + the final cold email side by side.
2. CI: a single workflow running `npm --prefix frontend run build` and
   `pytest backend/` against pinned Node/Python.
3. Add a root `.env.example` if and only if it points cleanly to the backend
   one (or replaces it).
4. Add a small smoke-test script that exercises `/api/run` against the
   ChromaDB corpus without hitting Tavily or the LLM.

### Prior research-log context

Previous runs (most recent first, none merged to `master`):

- `claude/compassionate-keller-snPHW` (2026-04-27) — seeded research log
  only; no code.
