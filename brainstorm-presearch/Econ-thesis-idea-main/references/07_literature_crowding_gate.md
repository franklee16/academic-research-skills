# Literature Crowding Gate

## Purpose

Use this before narrowing a master's thesis topic when the idea sits in a crowded applied economics literature. The goal is to protect the student from spending weeks on a topic that looks easy but is already saturated, hard to defend, or dependent on weak identification.

This module is called by `references/00_master_router.md`. Return a compact crowding status to the router instead of independently building the rest of the workflow.

The master router's scoring contract still applies. When this gate is reported for an idea or branch, include or preserve that idea's novelty, clarity, feasibility, effectiveness, and impact scores. Do not let a literature summary replace the score table.

## When This Gate Is Mandatory

Run this gate before title polishing, mechanism design, or a full blueprint when most of the following hold:

- the user is a master's student, undergraduate thesis writer, course-paper writer, or otherwise in thesis rescue mode;
- the topic uses broad policy nouns such as digitalization, common prosperity, digital economy, digital finance, green finance, ESG, high-quality development, rural revitalization, new quality productive forces, smart city, low-carbon city, broadband China, or pilot policy;
- the proposed design is a familiar `X affects Y` question with standard panel FE, DID, mediation analysis, threshold regression, or spatial model;
- the likely data are public indices, city/province yearbooks, CSMAR-style firm panels, or CFPS/CHFS without new measurement;
- the student has not named a new dataset, setting, mechanism, identification source, or empirical fact.

## Search Requirements

Before judging novelty or feasibility, search or inspect:

1. English literature: Google Scholar, NBER, RePEc, SSRN, journal pages, and recent working papers when available.
2. Chinese literature: CNKI/Wanfang/VIP if available, Chinese journal websites, university repositories, and credible working-paper or public-account summaries only as leads.
3. The closest 5-10 papers, not just broad survey papers.
4. Each close paper's data, sample, variable definitions, identification strategy, mechanism, and conclusion.

If web or database access is unavailable, state that the crowding verdict is provisional and make the first validation task a literature search.

## Crowding Diagnosis

Classify the field before building the thesis:

| Level | Meaning | Default action |
| --- | --- | --- |
| Low | Few close papers; data and question are not exhausted | Proceed to normal diagnosis |
| Medium | Several close papers; thesis possible only with a narrower setting, cleaner measure, or better mechanism | Pivot before blueprint |
| High | Many close papers use the same X, Y, data, and method | Park original topic or run pivot lab |
| Saturated | The student's exact X-Y-method-data package already appears repeatedly | Kill original topic; optionally branch out |

## Stop Rules

Recommend `park` or `kill` instead of focusing the title when:

- the closest papers already answer the same question with the same unit, period, index, and model;
- the only change is a newer year, a different province, or adding one more routine mechanism variable;
- the topic requires causal claims but the available variation is endogenous or already heavily criticized;
- the defense risk is obvious: committee members can ask "what is new?" and the student has no answer beyond replication;
- the student cannot access data that would create a real distinction from existing work.

Do not rescue a saturated topic by adding decorative mechanisms, arbitrary heterogeneity, a spatial model, a threshold model, or a fashionable index.

## Remaining-Space Search

If the student chooses to enter a crowded area, look for space in this order:

1. New outcome: a less-studied welfare, distributional, or behavioral outcome that still matches the theory.
2. New sample: a defensible population or setting not already covered, not merely a convenient smaller region.
3. New measurement: a transparent and replicable measure that improves on standard indices.
4. New mechanism: a mechanism variable that is conceptually distinct from the outcome and appears in data.
5. Better identification: a variation source with named assumptions and visible diagnostics, not a generic pilot DID.
6. Honest downgrade: a facts or measurement thesis that avoids causal overclaiming.

If the original X-Y package is `high` or `saturated` but the student wants to keep part of the topic, route to `references/08_crowded_topic_pivot_lab.md` before proposing a new thesis title.

## Output For Crowded Topics

When this gate is triggered, lead with:

1. `IRIS review`: five-dimensional scores for the idea or branch, average score, weakest dimensions, and next route.
2. `Literature crowding`: low / medium / high / saturated.
3. `Closest literature pattern`: what existing papers have already done.
4. `Defense risk`: the question an advisor or committee is likely to ask.
5. `Decision`: proceed / pivot / park / kill / downgrade.
6. `Smallest viable next step`: a concrete literature or data check.

Only provide a full thesis blueprint after the idea passes this gate, after a pivot-lab branch passes its filters, or after the user explicitly chooses to proceed despite the risk.

Return to `references/00_master_router.md` with: score state, crowding level, decision, binding defense risk, and recommended next route.
