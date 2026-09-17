# Reproducibility and Code Reuse

Use this reference when the user asks whether a paper can be reproduced, implemented, reused, or integrated into a project.

## Repository Checklist

- Official status: author-linked, project-page-linked, Papers with Code linked, or third-party.
- License: permissive, copyleft, research-only, missing, or unclear.
- Framework: PyTorch, JAX, TensorFlow, sklearn, custom C++/CUDA, or other.
- Environment: Python version, CUDA version, dependency pins, installation scripts.
- Data: public dataset, private dataset, generated data, preprocessing scripts, splits.
- Checkpoints: pretrained weights, model cards, download URLs, expected file layout.
- Entry points: training, evaluation, inference/demo, data preparation.
- Configuration: config files, seeds, hyperparameters, ablation settings.
- Expected metrics: paper tables, README claims, reproduced logs.
- Maintenance: commit dates, issue activity, broken links, archived status.

## Reuse Judgment

Prefer the smallest reusable unit:

- Equation or algorithmic idea.
- Data preprocessing rule.
- Loss function or metric.
- Model module.
- Prompt/evaluation protocol.
- Config and hyperparameters.
- Checkpoint.
- Full pipeline only when packaging, license, and dependencies are clean.

## Risk Categories

- Dependency risk: old CUDA, unpinned packages, conflicting frameworks.
- Data risk: private data, missing splits, undocumented preprocessing.
- Compute risk: training cost exceeds user's resources.
- Evaluation risk: metric mismatch, hidden test set, weak baselines.
- License risk: missing or incompatible license.
- Code quality risk: fragile scripts, global paths, undocumented assumptions.
- Scientific risk: method depends on a narrow dataset or construct proxy.

## Minimal Verification Plan

```text
1. Environment smoke test: import package or run help command.
2. Data path test: run preprocessing on one small sample.
3. Model path test: forward pass or inference on one example.
4. Metric test: compute one metric on a tiny fixture.
5. Reproduction test: run the smallest official evaluation or compare a logged result.
```

Do not recommend running untrusted installers, training scripts, or download scripts without first inspecting them.
