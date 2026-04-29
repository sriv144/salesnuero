# Research Log

## 2026-04-29 — Auto-Researcher v4

**Resume score at start of run:** 64 / 100. Multi-agent CrewAI system with a
Next.js frontend and FastAPI backend; concept (Big Five + DISC psychological
profiling for B2B outreach) is novel, but README is light on architectural
detail and the project is the smaller of the two TypeScript stacks under
review.

**Branch:** `claude/compassionate-keller-dI8Uk` (cut from `master`, not
`main` — this repo's default branch is `master`).

### What was implemented
No code or config changes this run. Seeded this `RESEARCH_LOG.md` so future
autonomous runs have memory.

### Why this was the deferred outcome
Resume-impact ranking placed embodied-skill-composer (85), AegisQuant (82),
Autonomous-SRE-Agent (80), and ai_interview_coach (53, showcase rescue) ahead
of salesnuero this run. Salesnuero scores well on novelty but the cheapest
resume lift available here is a README-architecture pass plus the standard
LICENSE/CI bundle, and that is best done in a single dedicated run rather
than crammed into an over-budget multi-repo run.

### Evaluated and skipped
- **README architecture diagram.** The current README lists features but
  does not show how the CrewAI agents fan out, how Tavily OSINT feeds the
  profiling step, or where ChromaDB sits. High value, deferred to next run.
- **CI workflow.** Backend (`pytest`) + frontend (`npm run lint`,
  `npm run build`) split. Worth doing, but needs the repo's actual test
  scripts inspected first.
- **`LICENSE`.** Trivial add, deferred for the same batch as the README pass.
- **Switching LiteLLM/NVIDIA-NIM to Anthropic Claude.** Touches
  `app/main.py` and the CrewAI agent definitions; out of scope for a
  docs-pass run.

### Next-run candidates
- Architecture diagram + tech-stack table in README.
- `.github/workflows/ci.yml` covering Python backend (`pytest`) and the
  Next.js frontend (`npm ci && npm run build`).
- `LICENSE` (MIT).
- Add screenshots / GIF of the Next.js UI to the README.
- Optional: Anthropic Claude provider behind LiteLLM.
