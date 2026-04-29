import { Agent } from "@cursor/sdk";

function requireEnv(name: string): string {
  const v = process.env[name];
  if (!v) throw new Error(`Missing required env var: ${name}`);
  return v;
}

function boolEnv(name: string, defaultValue = false): boolean {
  const raw = process.env[name];
  if (!raw) return defaultValue;
  return ["1", "true", "yes", "y", "on"].includes(raw.toLowerCase());
}

function buildPrompt(): string {
  const itemsJson = requireEnv("RESEARCH_ITEMS_JSON");

  return [
    "You are a continuous research agent for this repo.",
    "",
    "Focus areas (top 3 spaces):",
    "- AI/ML engineering (agents, evals, RAG, tooling)",
    "- Kaggle competitions (approaches, lessons, top solution writeups)",
    "- Trading research (market structure, strategies, execution)",
    "",
    "Input kanban batch (GitHub Projects is the source of truth):",
    itemsJson,
    "",
    "Hard constraints (repo contract):",
    "- NEVER modify any existing files under raw/ after creation.",
    "- You MAY add NEW files under raw/ to ingest new sources.",
    "- Do NOT mass-edit wiki/ pages. The ingest workflow requires discussing 3–5 takeaways with Cameron BEFORE writing wiki pages.",
    "",
    "Your outputs for this run:",
    "1) Add 0–N new source files under raw/ that directly support the kanban items.",
    "   - Prefer durable sources (official docs, papers, high-quality blog posts).",
    "   - Each source must be saved in an appropriate raw/ subfolder (raw/blogs, raw/papers, raw/kaggle, raw/trading, raw/repos, etc.).",
    "2) Append a draft 'research queue' entry to wiki/open-questions/research-queue.md that contains:",
    "   - which kanban items were addressed",
    "   - for each new raw source: 3–5 draft takeaways",
    "   - suggested wiki pages to create/update AFTER Cameron reviews takeaways",
    "",
    "Be conservative: if you cannot find a high-quality source quickly, record what you looked for and leave a TODO in the queue entry.",
  ].join("\n");
}

async function main() {
  const apiKey = requireEnv("CURSOR_API_KEY");
  const repoUrl = requireEnv("REPO_URL");
  const startingRef = process.env.STARTING_REF || "main";
  const modelId = process.env.MODEL_ID || "composer-2";
  const workOnCurrentBranch = boolEnv("WORK_ON_CURRENT_BRANCH", true);
  const autoCreatePR = boolEnv("AUTO_CREATE_PR", false);

  const prompt = buildPrompt();

  const agent = await Agent.create({
    apiKey,
    model: { id: modelId },
    cloud: {
      repos: [{ url: repoUrl, startingRef }],
      workOnCurrentBranch,
      autoCreatePR,
    },
  });

  const run = await agent.send(prompt);

  for await (const event of run.stream()) {
    if (event.type === "text") process.stdout.write(event.text);
  }
}

main().catch((err) => {
  console.error(err?.stack || String(err));
  process.exit(1);
});

