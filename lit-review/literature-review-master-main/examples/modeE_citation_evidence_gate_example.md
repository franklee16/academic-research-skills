# Mode E Citation Evidence Gate Example

## User request

```text
Please audit the related work section before submission.
Use source-only mode for the uploaded papers and flag every unsupported gap, novelty and equilibrium claim.
```

## Agent sequence

```text
Literature Orchestrator Agent
Claim Extraction Agent
Citation Verification Agent
Evidence Gate Agent
Numerical and Table Verification Agent
Source-Only Verification Agent when a fixed corpus is provided
Integration Editor Agent
```

## Expected output

1. Scope lock.
2. Pass 1 claim extraction table.
3. Metadata and version-risk table.
4. Evidence gate table.
5. Numerical and table audit if relevant.
6. Final submission safety verdict.

## Example verdict language

```text
Final verdict is MAJOR REPAIR REQUIRED.
The central gap claim is currently overclaimed. The cited sources support a narrower statement about static pricing models, but they do not support the manuscript's claim that no prior work studies joint pricing and service decisions under strategic consumer response. The claim should be weakened or additional direct predecessors must be added.
```
