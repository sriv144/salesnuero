# Research Log

A running record of auto-researcher passes against this repo.

## 2026-05-25 -- Auto-Researcher v4

**Resume score at start:** 72/100. Recent activity, CrewAI + LiteLLM
+ Next.js stack reads well, README covers setup and a Swagger demo.
Weak spots are limited deep-dive without reading the CrewAI flow and
the frontend in detail, which is more than this pass's token budget
can safely absorb.

**Implemented on branch `claude/compassionate-keller-FVAfQ`:**

- MIT `LICENSE`.
- Seeded this `RESEARCH_LOG.md`.

**Why nothing larger this pass:** Higher-impact options (docker compose
that coordinates Next.js frontend + FastAPI + Chroma, a Tavily-key
fallback, an end-to-end smoke test) all need to read the CrewAI flow
and frontend in detail to avoid breakage. Better to do it well in a
dedicated pass than half-do it here.

**Evaluated and skipped:**

- `docker-compose.yml` wiring frontend + backend + ChromaDB: requires
  understanding the Next.js build (`npm run dev` vs `build && start`)
  and the precise CrewAI agent boot sequence. Punted.
- Replacing NVIDIA NIM with Anthropic Claude: same provider-abstraction
  concern as the sibling repos.
- Adding a Tavily quota guard: the codebase apparently calls Tavily but
  doesn't show retry / cap behavior in the README; needs code reading.

**Next-run candidates:**

- End-to-end docker compose (Next.js + FastAPI + Chroma).
- Provider abstraction for LiteLLM (Anthropic Claude path).
- README screenshots + a 30-second GIF of the outreach flow.
- Tavily call accounting / per-prospect cost surfaced in the UI.
