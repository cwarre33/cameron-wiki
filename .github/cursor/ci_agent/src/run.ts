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

async function main() {
  const apiKey = requireEnv("CURSOR_API_KEY");
  const repoUrl = requireEnv("REPO_URL");
  const startingRef = process.env.STARTING_REF || "main";
  const prompt = requireEnv("PROMPT");
  const modelId = process.env.MODEL_ID || "composer-2";
  const autoCreatePR = boolEnv("AUTO_CREATE_PR", true);

  const agent = await Agent.create({
    apiKey,
    model: { id: modelId },
    cloud: {
      repos: [{ url: repoUrl, startingRef }],
      autoCreatePR,
    },
  });

  const run = await agent.send(prompt);

  // Stream events so the GitHub Actions log has useful breadcrumbs.
  for await (const event of run.stream()) {
    if (event.type === "assistant") {
      for (const block of event.message.content) {
        if (block.type === "text") {
          process.stdout.write(block.text);
        }
      }
    }
  }
}

main().catch((err) => {
  console.error(err?.stack || String(err));
  process.exit(1);
});

