# Co-math architecture & process

The `co-math-init` project runs a small team of Claude Code sub-agents against a
single living paper (`paper.tex`), under hooks that refuse to let work be marked
"complete" without an explicit reviewer approval. The diagrams below render
natively on GitHub (Mermaid). Edit the source blocks to adjust.

Architecture follows Zheng et al. (2026), *AI Co-Mathematician* (Google DeepMind).

---

## 1. System architecture

Who talks to whom, and where the artifacts live.

```mermaid
flowchart TD
    User(["👤 User"])

    subgraph FrontDoor["Front door"]
        direction TB
        PC["<b>project-coordinator</b><br/><i>reads goals, formalizes intent,<br/>dispatches &amp; steers workstreams</i>"]
        Goals[/"goals.md"/]
        Cfg[/"co-math-config.json<br/>strict_mode · review_policy"/]
        Dec[/"decisions.md"/]
    end

    subgraph Workers["Workstream agents"]
        direction TB
        Lit["<b>literature-reviewer</b><br/><i>cited, verified reports</i>"]
        Prover["<b>prover</b><br/><i>drafts proofs · strict discipline<br/>every gap flagged UNPROVEN</i>"]
        Coder["<b>coder</b><br/><i>Python · tests · golden values</i>"]
        Lean["<b>lean-prover</b><br/><i>Lean 4 · lake build</i>"]
    end

    Gate{"<b>paper-reviewer</b><br/>adversarial gate"}
    Read["<b>proof-readability</b> pass<br/><i>exposition only —<br/>prover in readability mode</i>"]
    Paper[/"<b>paper.tex</b> — living paper<br/>UNPROVEN · LEANPROVED · margin notes"/]

    subgraph Hooks["Discipline hooks — .claude/settings.json"]
        direction TB
        H1["paper_tex_guard.py<br/><i>theorem needs proof / leanproved / unproven</i>"]
        H2["workstream_complete_guard.py<br/><i>no 'complete' without approval file</i>"]
        H3["blocked_workstreams_notice.py<br/><i>surfaces blocked work on Stop</i>"]
    end

    User <-->|sounding board| PC
    PC <--> Goals
    PC --- Cfg
    PC --- Dec
    PC ==>|dispatch workstream| Lit
    PC ==>|dispatch workstream| Prover
    PC ==>|dispatch workstream| Coder
    PC ==>|dispatch workstream| Lean

    Lit -->|"report.md · status: review"| Gate
    Prover -->|"report.md · status: review"| Gate
    Coder -->|"report.md · status: review"| Gate
    Lean -->|"report.md · status: review"| Gate

    Gate -->|"APPROVE → approval file in .co-math/approvals/"| Paper
    Gate -.->|"REJECT / changes requested"| PC
    Paper -.->|"after approval (optional)"| Read
    Read -->|"re-review: plumbing only"| Gate
    Lean -.->|"green build → LEANPROVED, no informal proof needed"| Paper

    H1 -.->|guards| Paper
    H2 -.->|guards| Gate
    H3 -.->|watches| Workers

    classDef agent fill:#dbe9ff,stroke:#3b6cb7,color:#11243f;
    classDef gate fill:#ffe0e0,stroke:#c0392b,color:#3a0d0a;
    classDef artifact fill:#fff6da,stroke:#caa23a,color:#3a2f0a;
    classDef hook fill:#e7f6f2,stroke:#2a9d8f,color:#0c2b27;
    class PC,Lit,Prover,Coder,Lean,Read agent;
    class Gate gate;
    class Goals,Cfg,Dec,Paper artifact;
    class H1,H2,H3 hook;
```

---

## 2. Workstream lifecycle

Every unit of work is a `workstreams/W{NNN}-{slug}/` directory
(`instructions.md`, `status.md`, `log.md`, `report.md`). Its status moves
through these states — nothing reaches `complete` without a `paper-reviewer`
approval file.

```mermaid
stateDiagram-v2
    [*] --> dispatched: coordinator opens workstream
    dispatched --> running: agent picks it up
    running --> review: report.md written
    running --> blocked: missing toolchain / not formalizable / unprovable
    blocked --> running: unblocked by user or coordinator
    review --> approved: paper-reviewer APPROVE + approval file
    review --> running: REJECT — fix and resubmit
    approved --> readability: optional exposition pass
    readability --> review: re-review (content preservation + plumbing only)
    approved --> complete: workstream_complete_guard allows
    complete --> [*]
```

---

## 3. Verification ladder

Three levels of "proven", weakest to strongest — and the exposition pass that
runs after any of them.

```mermaid
flowchart LR
    A["<b>informal proof</b><br/>prover<br/><i>gaps flagged UNPROVEN</i>"] --> B["<b>machine-checked</b><br/>lean-prover<br/><i>lake build green → LEANPROVED</i>"]
    A --> C["<b>readable</b><br/>proof-readability<br/><i>exposition only,<br/>never changes the math</i>"]
    B --> C

    classDef step fill:#dbe9ff,stroke:#3b6cb7,color:#11243f;
    class A,B,C step;
```

A `lean-prover` build that exits 0 with no `sorry` is accepted by
`paper-reviewer` with only plumbing checks — the compiler has verified the
mathematics, so the theorem is closed with `\leanproved{}` instead of an
informal `\proof`. The `proof-readability` pass never alters mathematical
content; a suspected gap routes the workstream back to the `prover` rather than
getting quietly patched.
