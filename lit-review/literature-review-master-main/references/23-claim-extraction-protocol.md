# Claim Extraction Protocol

## Purpose

This protocol is used in Pass 1 of Mode E. Its only task is to extract claims. It must not verify, correct, rewrite, merge, delete or defend them.

The output of Pass 1 becomes the fixed input for Pass 2.

## Extraction rule

Extract a claim when the sentence or phrase makes an assertion that requires support from a citation, a source corpus, the manuscript itself, an appendix, proof material, a table, a figure, code output, or simulation results.

Do not extract purely rhetorical transitions unless they carry a factual or literature-positioning assertion.

## Claim types for academic manuscripts

Use these categories.

| Type | Extract when the manuscript says |
|---|---|
| Literature claim | Prior studies examine, focus on, assume, find or neglect something. |
| Gap claim | A research gap, underexplored relationship or missing mechanism is asserted. |
| Novelty claim | The paper is first, among the first, new, novel or distinct. |
| Contribution claim | The paper contributes to a specific literature or theory. |
| Framework-difference claim | The paper differs from prior work through primitives, timing, information, objective, constraint, solution concept or evidence. |
| Method claim | A method, model class, algorithm, estimator or approach is common, rare, new or used in prior work. |
| Theory claim | A construct, theory, mechanism or proposition is attributed to prior work. |
| Equilibrium claim | Prior work uses, assumes, proves, selects or compares an equilibrium concept. |
| Statistical claim | A number, percentage, count, coefficient, probability, credible interval, p-value, estimate or distributional fact is asserted. |
| Numerical simulation claim | A simulation result, robustness claim, benchmark comparison, parameter range or regime pattern is asserted. |
| Table or figure claim | A table, figure, chart or visual object is described or interpreted. |
| Causal claim | X causes, leads to, increases, reduces, drives, affects or results in Y. |
| Comparative claim | X is larger, smaller, faster, more robust, less efficient or more profitable than Y. |
| Temporal claim | A claim is tied to a year, period, trend or sequence. |
| Ranking claim | First, largest, leading, top, dominant, canonical or seminal status is asserted. |
| Definition of a construct | A field-specific construct, mechanism, solution concept, modelling object or theory term is defined. |
| Direct quotation | Text is quoted or closely paraphrased from a source. |
| Internal reproducibility claim | The manuscript states what was solved, simulated, estimated, benchmarked, coded, assumed or proved. |

## Claims not normally extracted

Do not extract the following unless they carry field-specific or source-dependent meaning.

```text
Purely stylistic sentences
Author opinions explicitly marked as opinion
Acknowledgements
Questions that do not assert an answer
Hypothetical examples with no factual assertion
Common-language definitions with no disciplinary content
```

## Special rules for theory and simulation papers

Definitions of constructs, solution concepts and modelling assumptions often need support. Extract them when they are used to position the paper in a literature.

Examples that must be extracted.

```text
Strategic consumers are forward-looking buyers who time purchases in response to expected future prices.
This literature typically assumes a unique equilibrium.
Most analytical models treat advertising as exogenous to operational capacity.
The numerical experiments show that the reversal persists across broad parameter ranges.
```

## Extraction output

Use this format.

| Claim ID | Claim text | Claim type | Location | Attached citation or evidence | Verification target |
|---|---|---|---|---|---|
| C001 | Exact wording from manuscript | Literature claim | Introduction, paragraph 3 | Smith and Lee 2023 | External source |
| C002 | Exact wording from manuscript | Internal reproducibility claim | Numerical section, Table 2 note | Code output or table | Internal evidence |

## Pass 1 discipline

Do not judge whether the claim is true.
Do not supply missing citations.
Do not rewrite weak claims.
Do not merge separate claims if they need different evidence.
Do not split a coherent sentence if a single citation supports the whole assertion.

When unsure, extract the claim and flag it as borderline.
