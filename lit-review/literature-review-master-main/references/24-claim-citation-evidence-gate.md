# Claim Citation Evidence Gate

## Purpose

This protocol is used in Pass 2 of Mode E. It verifies whether each extracted claim is supported by the attached citation, source, corpus item, table, figure, proof, appendix or simulation output.

The evidence gate does not reward plausible claims. It only verifies traceable claims.

## Verification ladder

Check claims in this order.

```text
1. Does the cited or attached source exist?
2. Is the source version correct?
3. Does the source discuss the relevant object?
4. Does the source support the exact claim?
5. Does the source support the strength of the wording?
6. Does the source include boundary conditions omitted by the manuscript?
7. Is the citation being used as direct support, background support, contrast, or method precedent?
8. Is manual inspection required?
```

## Source version control

Treat different versions as different evidence objects.

```text
SSRN working paper
arXiv preprint
Conference paper
Accepted manuscript
Publisher version
Online appendix
Erratum or corrigendum
Retracted or withdrawn version
```

If the manuscript cites a published version but the claim is only visible in a working paper version, mark wrong version risk.

## Support classifications

Use these decisions.

| Decision | Meaning | Typical action |
|---|---|---|
| Verified | The source directly supports the claim. | Keep. |
| Verified with interpretation | The source supports the claim through a transparent inference. | Keep but phrase carefully. |
| Background only | The source is relevant but does not support the specific claim. | Add a stronger source or weaken the claim. |
| Partially supported | The source supports a narrower claim. | Rewrite the claim. |
| Misleading | The manuscript omits a crucial condition, limitation or contrary result. | Add the boundary condition or change the citation. |
| Overclaimed | The source is weaker than the manuscript wording. | Remove strong words such as first, all, always, shows, proves or validates. |
| Contradicted | The source says the opposite or materially different thing. | Correct or remove. |
| Citation not found | The source cannot be located. | Replace or mark unresolved. |
| Metadata verified only | The source exists but support cannot be checked. | Manual PDF check required. |
| Not in corpus | Source-only mode cannot trace the claim. | Remove, cite from corpus, or ask to expand corpus. |

## Claim strength audit

Watch for these overclaiming signals.

```text
first
novel
no prior work
few studies
always
generally
robustly
proves
validates
demonstrates in practice
empirically shows
```

For no-data theory and simulation papers, replace empirical overclaiming.

Unsafe wording.

```text
The simulations validate the real-world effect.
Our empirical results show...
The model proves that firms should always...
```

Safer wording.

```text
The numerical experiments illustrate the mechanism within the model.
The analysis shows that the result arises under the stated assumptions.
The simulations quantify the parameter regions in which the mechanism is strongest.
```

## Evidence source hierarchy by claim type

Use the right authority for the claim.

| Claim type | Preferred evidence |
|---|---|
| Theoretical result | Original model paper, theorem, proposition or proof. |
| Equilibrium concept | Original source or closest modelling precedent. |
| Literature gap | Direct predecessor matrix plus recent survey or closest papers. |
| Empirical fact | Original empirical paper, dataset, official statistics or credible report. |
| Algorithmic claim | Original algorithm paper, benchmark paper, code documentation or experiment table. |
| Journal scope claim | Official journal page or verified journal database. |
| ABS rating | Embedded ABS AJG 2024 database or provided AJG source. |
| Retraction status | Publisher page, Crossmark, Retraction Watch, PubMed where relevant, or official notice. |
| Simulation result | Manuscript table, code output, seed log, appendix or reproducibility file. |

## Required output for each claim

```text
Claim ID:
Claim:
Location:
Cited evidence:
Evidence location:
Support decision:
Risk:
Required fix:
Safer wording if needed:
Manual check needed:
```

## Final verdict rules

Use these thresholds.

```text
PASS
No high-risk unsupported claims. Minor metadata issues only.

PASS WITH MINOR FIXES
Several weak or incomplete citations, but no central contribution claim is unsafe.

MAJOR REPAIR REQUIRED
A central gap, novelty, contribution, theory or numerical claim is unsupported or overclaimed.

UNSAFE FOR SUBMISSION
Multiple central claims are unsupported, contradicted, fabricated, or dependent on sources that cannot be located.
```
