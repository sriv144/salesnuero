# Research Log

Autonomous research-agent activity log for SalesNeuro. Each entry
records (a) what was implemented, (b) why it was prioritized, (c)
what was evaluated but skipped, and (d) next-run candidates. Do not
delete prior entries.

---

## 2026-06-03 — Auto-Researcher v4

**Resume-worthiness score at start of run:** 58 / 100

- Stack prestige (25): 16 — CrewAI multi-agent + LiteLLM +
  ChromaDB + Tavily + Next.js / React / Tailwind. Solid full-
  stack agent product.
- Commit recency (25): 18 — 23 days since last push.
- Feature completeness (20): 14 — split backend / frontend layout,
  RAG ingestion step, Swagger surface, Big Five / DISC psychological
  framing.
- Stars / visibility (15): 4 — 1 star, public topics.
- README quality (15): 10 — reasonable feature highlights + two-
  terminal local run guide + prerequisites. No architecture diagram,
  no API surface table, no screenshots, no env-var reference.

### Implemented on `claude/compassionate-keller-oCTQH`

Log-only commit. **No source changes this run.**

### Why no implementation this run

SalesNeuro is the most complex of the six repos (Python backend
+ TypeScript frontend + ChromaDB + CrewAI), but token budget
was spent on the three highest-impact targets (AegisQuant, embodied-
skill-composer, ai_interview_coach). The most useful changes here
— a CrewAI architecture diagram and a screenshot of the Next.js
UI — require either rendering assets or running the stack, which is
out of scope for a single safe commit.

A README polish pass and a frontend CI workflow are clear next-run
candidates.

### Evaluated and skipped

- **README polish pass.** Worth doing (CrewAI agent topology
  diagram, env-var reference table, API surface table, screenshot
  of the Next.js UI). Larger than a quick win; defer.
- **`.github/workflows/ci.yml`.** Needs separate jobs for backend
  (Python + Chroma + Tavily mock) and frontend (`npm run build`).
  Defer.
- **Anthropic Claude provider via LiteLLM.** LiteLLM makes this
  almost a one-line change (`model="anthropic/claude-sonnet-..."`)
  but needs accompanying env-var documentation and a re-ingestion
  check on the RAG corpus. Defer.
- **Replace OpenAI / NVIDIA reliance with a documented multi-
  provider matrix.** Same shape as the Claude addition, slightly
  bigger scope.

### Next-run candidates

1. CrewAI agent topology diagram + `docs/architecture.md`.
2. Add a frontend build CI job (`npm ci && npm run build`) and a
   backend lint + import-compile CI job in `.github/workflows/`.
3. Add an Anthropic Claude provider option via LiteLLM
   (`model="anthropic/claude-sonnet-4-7"`) selectable through env.
4. Add a screenshot of the Next.js prospect intake + outreach
   draft view at the top of the README.
5. Document the `/api/run` request / response schema in the README
   (Swagger is great, but a copy-pasteable curl example raises the
   ceiling for first-time visitors).
