## Learned User Preferences

- Prefer Cursor Automations (UI) over repo-hosted GitHub Actions for wiki CI/research agents; remove or avoid committing action-based agent runners once the Cursor automation path is known.
- Automated git commits for this repo should attribute as `cwarre33` / `cwarre33@alumni.uncc.edu` so they count on the GitHub contributions chart.
- On wiki ingest and catch-up plans, discuss top takeaways and wait for explicit confirmation before writing or batch-updating pages.
- Prefer deep Tier A coverage for major FLS production systems (full subsystem split when useful) over thin catalog stubs; keep Jira bulk imports as compact key/status indexes, not raw dumps.
- Prefer one fat initiative page for FLSP-103 for its original epics; for major new ClearView epics (e.g. PIE & Shop Replacement / FLSP-856), prefer a standalone initiative page unless asked to inline.
- When documenting who-did-what history (Jira, PRs, handoffs), use neutral factual timelines — never frame around a colleague's gap or imply blame.
- Do not manually edit `wiki/index.md` (it is auto-regenerated); do not commit unless explicitly asked.
- Research-agent focus spaces for continuous wiki growth: AI/ML engineering, Kaggle, and trading; treat GitHub Projects as the kanban source of truth.
- Keep Jira ticket keys scrubbed from committed wiki pages and filenames; join keys live in `raw/` and private trackers only.
- For ClearView wiki catch-ups after Shop/RMF landed, prioritize Shop/RMF depth first; skip major Zendesk/SellSmart/SofaScope refreshes unless asked or audit flags contradictions.

## Learned Workspace Facts

- This repo is Cameron's Karpathy-style second brain / living work wiki (`cwarre33/cameron-wiki`); `raw/` is immutable after creation and `wiki/` is LLM-owned synthesis.
- Inventory Lookup / ClearView parent initiative is FLSP-103 (not FLSP-159); epic rollup fields can be unreliable — prefer Parent Link trees.
- FLS Jira work for this vault commonly spans projects FLSP, FLSM, FLSI, and ITT.
- GitHub repository secrets cannot contain the substring `GITHUB`, which blocked PAT-style secret names for the secrets-monitor workflow.
- Desired “done” behavior for the notes/research pipeline is a full research suite across all wiki domains, not a single-domain pass.
- FLS Bitbucket workspace is `furniturelandsouth`; primary ClearView repo is `inventory-lookup` (local clone often under `CleanDevEnvironment/NetSuite/Inventory-Lookup`); Bitbucket slug for the utility shed is mistyped as `ja-utlity-shed`.
- PIE & Shop Replacement (FLSP-856) under FLSP-103 is the major post-July ClearView surface: Shop/RMF requests, NetSuite Shop Request records, RMF tab/nav, notifications, and related permissions/attachments work.
