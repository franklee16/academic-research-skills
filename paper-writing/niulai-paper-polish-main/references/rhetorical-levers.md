# Evidence-preserving rhetorical levers

Use these levers to increase reviewer legibility, not to inflate merit.

## Co-primary lever: evidence framing

Move the strongest existing evidence close to the claim it supports. State the comparison axis, value or direction, uncertainty, and practical meaning when those facts already exist in the manuscript.

Weak:

> The method performs well on several benchmarks.

Stronger when the cited table actually supports it:

> Across the three evaluated benchmarks, the method improves the prespecified primary metric over the strongest reported baseline (Table 2); the gain is smallest on Dataset C, which defines the current boundary of the result.

Do not add a number, significance claim, baseline status, or “consistent” pattern unless verified across every relevant result.

## Co-primary lever: novelty stance

Position novelty as a precise difference from the closest work:

- what prior systems assume or cannot do;
- which mechanism, representation, evaluation, or empirical finding changes that boundary;
- why the delta matters to the target community.

Prefer “introduces X that enables Y under Z” to “is the first groundbreaking framework.” If priority cannot be exhaustively verified, avoid “first.” Cite and fairly describe the strongest adjacent work, including inconvenient overlap.

## 3. Scope framing

Define the supported scope positively and explicitly. Broaden only by logical implication already justified by the method and evaluation. Keep domain, dataset, population, model-family, compute, and distribution-shift limits visible.

Avoid shrinking the contribution through vague disclaimers, but do not replace a narrow evaluation with universal language. A useful pattern is: “Within [tested conditions], the evidence supports [claim]; whether it extends to [untested condition] remains open.”

## 4. Contribution structure

Use a small contribution set with one-to-one evidence anchors. The title, abstract, introduction list, results headings, limitations, and conclusion should use compatible terminology and scope. Remove contribution bullets that merely describe routine implementation.

## 5. Technical precision and readability

Define overloaded terms, state assumptions before their use, and favor direct syntax. Formalism is valuable when it removes ambiguity; unnecessary notation or lexical complexity increases reviewer effort without strengthening the work.

## Failure patterns

- Moving limitations out of sight instead of addressing them.
- Turning correlations into mechanisms or causal effects.
- Replacing “associated with” by “changes,” “produces,” “shapes,” or “isolates” when the design or semantic-preservation audit does not support that escalation.
- Calling an average improvement universal when subgroups are mixed.
- Describing a hand-selected baseline as the strongest available baseline.
- Treating a prettier figure as new evidence.
- Adding citations for prestige rather than factual support.
- Repeating a positive rewrite until calibration and nuance disappear.
