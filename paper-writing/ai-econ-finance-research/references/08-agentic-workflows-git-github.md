# Agentic Workflows, Git, GitHub, And Collaboration

Use this before AI edits files, runs code, or collaborates with coauthors/RAs.

## Zero-To-Agentic Setup

Guide the user through:

1. create GitHub account;
2. create private research repo;
3. add `.gitignore`;
4. add `README.md`, `DATA.md`, `AGENTS.md` or `CLAUDE.md`, and `AI-USE-LOG.md`;
5. create a branch;
6. ask AI for a plan;
7. approve or revise plan;
8. let AI edit files only after approval;
9. review diff;
10. run code/checks;
11. commit;
12. push;
13. open pull request for coauthor or RA review if collaborating.

## Collaboration Rules

Ask who is responsible for:

- uploading data;
- approving AI-generated code;
- checking claims and citations;
- reviewing pull requests;
- merging changes;
- recording AI use;
- deciding whether confidential materials can be used.

## Copy-Ready Instruction

```text
Act as a Git, GitHub, and agentic workflow assistant for an economics/finance research project.

First ask what project stage I am in, whether a Git repo exists, what files are sensitive, who is collaborating, and what commands/checks are available.

Before editing files, inspect the project structure, propose a plan, identify files that must not be touched, and wait for approval.

After changes, summarize the diff, run or specify checks, update the AI-use log, and state what I must verify before commit or pull request.
```

## Required Guardrails

- never use destructive Git commands unless explicitly approved;
- never expose raw/restricted/licensed data;
- use branches for experiments;
- use pull requests for coauthor/RA review;
- use worktrees only when the user understands multiple working directories.
