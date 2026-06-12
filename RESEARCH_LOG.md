# RESEARCH_LOG.md

Persistent memory for the auto-researcher agent. Read top-to-bottom before deciding what to ship on the next pass.

> **Default branch is `master`, not `main`.** All `claude/*` branches must base off `master`.

---

## 2026-06-12 — Auto-Researcher v4

**Resume score at start of run:** 67 / 100 (5th of 6 in the portfolio)

**Score breakdown:**
- Tech stack prestige: 18/25 — CrewAI multi-agent + LiteLLM + ChromaDB + FastAPI + Next.js + Tavily OSINT = credible AI-sales stack.
- Commit recency: 22/25 — updated 2026-05-11.
- Feature completeness: 14/20 — backend + frontend run, RAG ingestion exists, but no tests visible.
- Stars / visibility: 3/15 — 1 star.
- README quality: 10/15 — feature list + setup + Swagger pointer, no architecture diagram or screenshots.

### What was implemented this pass (branch `claude/compassionate-keller-qiarsa`)

- `RESEARCH_LOG.md` — this file. Log-only commit.

### Why no code this pass

The top three repos absorbed this run's safe-change budget. salesnuero is split across a Python backend and a TypeScript / Next.js frontend, which makes safe additive changes (CI, screenshots, even a Mermaid diagram) noticeably more involved than the Python-only repos. The repo already has 9 open `claude/*` PRs (LICENSE, dual-stack CI, `backend/.env.example`, README polish queued), so additional scaffolding would be duplicative.

### Evaluated and skipped

- **Another CI variant** — already in PR #6 (dual-stack ruff + npm-lint).
- **Another `backend/.env.example`** — already in PR #8.
- **README rewrite** — would be the third pass and isn't grounded in newly-discovered content.
- **A real `tests/` directory** — high value but needs to read the CrewAI agent definitions in `backend/` to write a sensible mocked test.

### Next-run candidates (priority order)

1. **Baseline `tests/` directory**: one mocked CrewAI test that asserts the `/api/run` endpoint constructs the expected `Crew` topology. Unblocks the queued CI PRs.
2. **CrewAI agent topology diagram** in README (Mermaid): Researcher -> Psychology Profiler -> Copywriter pipeline, with Tavily and ChromaDB as side dependencies.
3. **Screenshot of the Next.js frontend** in README (`docs/screenshots/dashboard.png`).
4. **Anthropic Claude as the CrewAI default LLM** behind `LITELLM_PROVIDER={nvidia,anthropic}` — clean LiteLLM swap, multi-provider story.
5. **Merge the lowest-risk of the open scaffolding PRs** (LICENSE + `backend/.env.example` + dual-stack CI) into one clean PR.
