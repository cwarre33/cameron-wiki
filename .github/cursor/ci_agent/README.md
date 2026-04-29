# Cursor CI Agent runner

Minimal runner for the Cursor TypeScript SDK used by
[`../../workflows/cursor-ci-agent.yml`](../../workflows/cursor-ci-agent.yml).

## Environment variables

- `CURSOR_API_KEY` (required): Cursor API key from `cursor.com/dashboard/integrations`
- `REPO_URL` (required): Git repo URL, e.g. `https://github.com/cwarre33/cameron-wiki`
- `STARTING_REF` (optional): branch/ref to start from (default `main`)
- `MODEL_ID` (optional): Cursor model id (default `composer-2`)
- `PROMPT` (required): instructions passed to the agent
- `AUTO_CREATE_PR` (optional): `true|false` (default `true`)

## Local dev

```bash
cd .github/cursor/ci_agent
npm install
export CURSOR_API_KEY="crsr_..."
export REPO_URL="https://github.com/cwarre33/cameron-wiki"
export PROMPT="Explain this repo"
npx tsx src/run.ts
```

