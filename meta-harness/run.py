#!/usr/bin/env python3
import argparse
import os
from pathlib import Path

import yaml

from meta_harness.loop.optimizer import OptimizerLoop
from meta_harness.meta_agent.proposer import MetaAgent


def create_llm_client(provider: str, model: str, config: dict):
    if provider == "nim":
        from openai import OpenAI
        api_key = os.environ.get(config.get("api_key_env", "NVIDIA_NIM_API_KEY"))
        return OpenAI(api_key=api_key, base_url=config.get("base_url"))
    elif provider == "ollama":
        import ollama
        return ollama
    else:
        raise ValueError(f"Unknown provider: {provider}")


def main():
    parser = argparse.ArgumentParser(description="Meta-Harness Optimizer")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    parser.add_argument("--baseline", default=None, help="Path to baseline harness")
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)

    baseline = Path(args.baseline) if args.baseline else None
    loop = OptimizerLoop(config, baseline_harness=baseline)

    meta_config = config["models"]["meta_agent"]
    llm_client = create_llm_client(
        meta_config["provider"],
        meta_config["model"],
        meta_config,
    )
    meta_agent = MetaAgent(llm_client=llm_client)
    loop.set_meta_agent(meta_agent)

    loop.run()


if __name__ == "__main__":
    main()
