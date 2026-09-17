# Handbook Core Concepts

Use this when the user needs concepts before using AI in research.

## Core Promise

AI can reduce labor, but it does not remove scholarly responsibility. Researchers remain responsible for citations, data use, methods, interpretation, code, disclosure, and final claims.

## Key Concepts In Plain Language

| Term | Plain meaning | Research example |
| --- | --- | --- |
| LLM | a model that predicts and generates text/code from context | explains a regression table, but may invent citations |
| prompt | one instruction to an AI tool | asks AI to summarize a paper |
| project | persistent AI workspace for a paper or research task | ChatGPT/Claude Project for one empirical paper |
| skill | reusable procedure for repeated tasks | literature matrix, methods audit, Stata debugging |
| agent | AI system that can plan, read/write files, run commands, and report results | Codex helps refactor analysis scripts |
| MCP/connector | bridge between AI and another tool or data source | AI connects to GitHub, Zotero, or a database |
| RAG | retrieval-grounded answering from sources | AI answers from uploaded papers rather than memory |
| context window | material the model can currently use | full paper plus instructions may crowd out details |
| `.gitignore` | file listing things Git should not track | excludes raw data, credentials, licensed extracts |
| branch | separate line of work in Git | AI experiments on a branch before merging |
| pull request | review request before merging code/text | coauthor reviews AI-assisted changes |
| AI-use log | record of AI help and human checks | notes tool, task, accepted output, verification |

## Minimum Safe Setup

For serious research, use:

- one AI project/workspace;
- one GitHub repo;
- `README.md`;
- `DATA.md`;
- `AGENTS.md` or `CLAUDE.md`;
- `AI-USE-LOG.md`;
- `.gitignore`;
- human verification before accepting output.

## What AI Helps With

- explaining unfamiliar code or methods;
- organizing literature and notes;
- drafting careful prose from verified facts;
- debugging Stata/R/Python;
- building toy-data tests;
- preparing seminar questions;
- making slides after claims are verified;
- documenting data and workflows.

## What AI Should Not Decide Alone

- research question importance;
- identification strategy;
- causal interpretation;
- final literature claims;
- whether restricted data can be uploaded;
- referee judgment;
- final paper submission;
- policy or investment recommendation.
