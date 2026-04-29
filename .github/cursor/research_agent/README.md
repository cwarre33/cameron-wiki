# Cursor research agent runner

Used by [`../../workflows/cursor-research-agent.yml`](../../workflows/cursor-research-agent.yml).

## Required secrets

- `CURSOR_API_KEY`: Cursor API key (`cursor.com/dashboard/integrations`)
- `GH_PROJECT_NODE_ID` (optional but recommended): GitHub ProjectV2 node id (`PVT_...`). If missing, the workflow exits without doing work.

## Behavior (contract-safe)

This agent is designed to respect `CLAUDE.md`:

- It **may create new files** under `raw/` (new sources only).
- It **must not modify existing `raw/` files**.
- It **appends draft takeaways** into `wiki/open-questions/research-queue.md` rather than mass-editing wiki pages directly.

## Local dev

```bash
cd .github/cursor/research_agent
npm install
export CURSOR_API_KEY="crsr_..."
export REPO_URL="https://github.com/cwarre33/cameron-wiki"
export RESEARCH_ITEMS_JSON='{"projectTitle":"Example","readyStatus":"Ready","items":[{"id":"x","title":"Research topic","body":"...","url":""}]}'
npx tsx src/run.ts
```

