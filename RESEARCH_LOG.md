# Research Log

Persistent memory used by the auto-researcher agent. Each run appends a dated
section so future runs can see what was evaluated, what shipped, and what was
deliberately skipped.

Note: this repo's default branch is `master` (not `main`), which the
auto-researcher's hard-constraint list tracks explicitly.

## 2026-04-23 - Auto-Researcher v4

**Resume-worthiness score at start of run: 55 / 100**
- Tech stack prestige: 12/25 (TypeScript web CRM - commodity stack)
- Commit recency: 22/25 (last push 2026-04-14)
- Feature completeness: 10/20 (functional but not a standout)
- Stars / visibility: 5/15 (1 star, 2 open issues)
- README quality: 6/15 (minimal)

### Branch
`claude/compassionate-keller-ONkrp`

### Status this run
**Not selected for implementation.** Repo ranked 6th of 6. A TypeScript
CRM is the hardest category to make resume-worthy without a concrete
vertical differentiator (e.g. AI deal-scoring, unusual data source,
multi-tenant infra). The existing `auto-research/2026-04-14-v2` and
`auto-research/2026-04-15` branches also hold prior auto-researcher
work that should be reviewed before stacking more branches.

### Prior branches observed (unmerged on master)
- `auto-research/2026-04-14-v2`
- `auto-research/2026-04-15`

Contents not re-inspected this run to stay in token budget.

### Why this repo scored lowest
CRMs are a crowded commodity category. To justify a "resume-worthy"
claim this repo needs one of:
1. An AI-native differentiator (e.g. pipeline-stage prediction, call-
   transcript summarisation, lead scoring with calibrated confidence).
2. Visible multi-tenant infra (postgres row-level security, org-scoped
   auth, rate limiting, audit log) that signals production-readiness.
3. A polished live demo.

Without at least one of these, incremental polish will not move the
needle on the 0-100 scale.

### Evaluated and skipped
- **Generic README polish**: low ROI without the above.
- **Adding CI for Next.js / tsc**: useful but already on deck via one
  of the open `auto-research/*` branches - no reason to double up.
- **E2E tests with Playwright**: strong signal but needs dev
  fixtures + seeded DB that do not exist in the repo today.

### Next-run candidates
1. Review and merge / close the two existing `auto-research/*` branches
   so master has a clean baseline.
2. Ship one flagship AI feature (e.g. `POST /api/leads/:id/score`
   returning a calibrated probability plus top-3 reasons via Claude)
   and make it the headline in the README.
3. Add a public demo deploy (Vercel) with a seeded dataset.
4. Add a short demo gif / MP4 showing the flagship feature.
5. Add Playwright smoke tests once the seeded dataset exists.
