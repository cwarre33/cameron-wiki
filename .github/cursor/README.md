# Cursor agents for CI/CD

This repo includes GitHub Actions workflows that can launch Cursor SDK agents to help
keep CI/CD green and to run kanban-driven research.

## Required GitHub secret

Create a repository secret:

- `CURSOR_API_KEY`: Cursor API key from `Cursor dashboard → Integrations` (`cursor.com/dashboard/integrations`)

Notes:
- This secret name/value avoids the PAT restriction you hit earlier (no `GITHUB_*` PAT secret required).
- Use a service account API key if you want the automation to be shared/rotatable across machines.

## Workflows

- `cursor-ci-agent.yml`: On failure of selected workflows, launches a Cursor Cloud Agent run to diagnose and open a PR with the smallest fix.
- `cursor-research-agent.yml`: Scheduled/manual workflow that polls GitHub Projects for “Ready” research items and launches a research run.

