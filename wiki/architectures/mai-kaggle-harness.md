---
title: MAI Harness — Reusable Kaggle Competition Framework
type: architecture
status: active
visibility: public
sources: [repo:Passion/KaggleCompetition/harness]
related: [[kaggle/deep-past-akkadian-translation.md]], [[kaggle/playground-s6e2-heart-disease.md]], [[kaggle/portfolio-overview.md]]
created: 2026-05-20
updated: 2026-05-20
confidence: high
tags: [kaggle, hydra, pytorch, sklearn, harness, mai-harness]
---

# MAI Harness — Reusable Kaggle Competition Framework

**Package:** `mai-harness` v0.1.0 · CLI: `kaggle-harness`

**Repo:** `CleanDevEnvironment/Passion/KaggleCompetition/` — uncommitted `harness/`, `competitions/`, `conf/`, `pyproject.toml` (May 2026 WIP; 15 commits ahead of origin from March 2026 competition work)

## Purpose

Reusable competition scaffold supporting **sklearn + PyTorch** pipelines with **Hydra** configuration — train, predict, and make-submission from a consistent CLI.

## CLI commands

```bash
kaggle-harness research --competition-dir PredictingHeartDisease --slug playground-series-s6e2
kaggle-harness run --competition competitions.playground_series_s6e2.run --action train
kaggle-harness predict --competition competitions.my_comp.run --override trainer.max_epochs=3
kaggle-harness make-submission --competition competitions.my_comp.run
```

## Architecture

```
harness/
├── base.py           BaseTask ABC (model, dataloaders, loss, optimizer)
├── cli.py            argparse entrypoint
├── trainer/          HarnessTrainer
├── hydra_utils.py    compose_config()
├── artifacts.py      run initialization
├── metrics.py
├── research/
│   ├── extract.py    build_context_pack from competition notebooks
│   └── nim_brief.py  NIM-generated research brief
├── llm/nim_client.py NVIDIA NIM integration for research phase
└── augmentation/, distillation/, exporter/  (stubs for extension)

competitions/
├── _template/        task.py, data.py, features.py, pipelines/, run.py
├── playground_series_s6e2/   Heart Disease S6E2 implementation
└── example_competition/      demo task
```

## BaseTask contract

Every competition implements:
- `get_model()` → `torch.nn.Module`
- `get_dataloaders()` → train/val/test `DataLoader`s
- `compute_loss(outputs, targets)` → scalar tensor
- Optional: custom optimizer/scheduler

## Research subcommand

Extracts working solutions from competition notebooks (up to N files/cells), builds a context pack, generates an LLM research brief via NIM — useful for bootstrapping new competition entries from public kernels.

## Dependencies

Hydra, OmegaConf, numpy, pandas, scikit-learn, torch, joblib (Python ≥3.10)

## Relationship to existing Kaggle work

- **Deep Past (ByT5 + MBR):** 8 notebook iterations, score 34.7 — notebooks in `DeepPastTranslation/` (modified, uncommitted)
- **March 2026 commits:** Stanford RNA, March Mania ELO, House Prices leakage study, DeepPast pipeline updates
- Harness generalizes patterns repeated across competitions into one Hydra-configured framework

## Interview angles

- **Competition factory pattern:** Template + BaseTask ABC reduces boilerplate per new competition
- **Research automation:** Extract public kernels → NIM brief → informed feature engineering
- **Config-driven ML:** Hydra overrides enable rapid ablation without code changes
