# Installation and Deployment

This repository is itself the canonical Agent Skills-compatible `research-defense-radar` skill folder.

For the shortest path, download `packages/research-defense-radar.zip` from the repository and upload it through the ChatGPT or Claude Skills interface.

## ChatGPT / Codex

### Codex desktop, CLI, or IDE — personal installation

Clone the repository directly into the personal skill location:

```bash
git clone https://github.com/SuperJayLiu/research-defense-radar.git \
  ~/.agents/skills/research-defense-radar
```

Invoke it in a Codex prompt with:

```text
$research-defense-radar Compare this new working paper with my proposal.
```

### ChatGPT Skills / Work

Build the ZIP:

```bash
python scripts/package_skill.py
```

Import `dist/research-defense-radar.zip` through the Skills interface, enable it, then select it with `@Research Defense Radar`. Workspace policy and product surface may control whether custom skills are available.

## Claude

### Claude Code — personal installation

Clone the repository directly into the personal skill location:

```bash
git clone https://github.com/SuperJayLiu/research-defense-radar.git \
  ~/.claude/skills/research-defense-radar
```

Invoke it with:

```text
/research-defense-radar Compare this new working paper with my proposal.
```

For a project-scoped installation, place the repository contents at `.claude/skills/research-defense-radar/`.

### Claude web / Cowork

Run the packager and upload `dist/research-defense-radar.zip` through Claude's Skills customization interface. Enable it for the account/session before use. The ZIP contains a single `research-defense-radar/` folder at its root.

## Portable prompt-only fallback

On an Agent Skills-compatible host that does not provide an installer, attach this repository directory and instruct the agent to read `SKILL.md` completely before acting. This fallback does not create schedules or grant web/storage permissions.

## Verification

From the repository root:

```bash
python scripts/update_radar_state.py --self-test
python scripts/test_update_radar_state.py
python scripts/package_skill.py --self-test
python scripts/check_distribution.py
```

Install and manually test the skill before creating any unattended schedule.
