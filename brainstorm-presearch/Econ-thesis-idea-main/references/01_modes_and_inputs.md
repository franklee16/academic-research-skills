# Modes And Inputs

## Purpose

Use this file at the beginning of a `thesis-idea` task. Classify the user, the paper type, and the ambition level before judging the idea.

For multi-step work, use this file under the control of `references/00_master_router.md`.

## Raw Interest Intake

Users may start with a personal interest, advisor direction, policy, variable, phenomenon, or a very colloquial intuition. Do not require a polished academic topic before beginning.

Before the first full diagnosis, preserve the user's raw wording and create a provisional idea card:

```text
raw_wording:
possible_economic_object:
possible_X:
possible_Y:
possible_mechanism:
possible_setting:
claim_type:
main_missing_piece:
```

Use the card to help the mandatory ideation review. Do not over-academicize the idea so early that the user's original curiosity, constraint, or advisor requirement disappears.

## Default Modes

### Thesis Rescue Mode

Use by default for undergraduate and master's students, course papers, opening reports, and urgent thesis deadlines.

Priority order:

1. literature crowding and whether the topic should be stopped before focusing;
2. obtainable data;
3. clear question;
4. basic identification or credible descriptive strategy;
5. interpretable results;
6. literature positioning.

Required output:

- literature crowding level for crowded thesis topics;
- whether the original topic is too broad;
- one-sentence research question;
- feasibility color and decision;
- minimum viable thesis version;
- data and variable map;
- usable baseline model;
- what not to claim;
- first-week validation plan and advisor memo, but only after `是否继续打磨` says the idea is ready to freeze or proceed.

### Research-Design Strengthening Mode

Use for advanced master's students, PhD students, working papers, or users who already have data/method capacity.

Add:

- literature positioning;
- comparison of identification options;
- main threats and responses;
- mechanism and heterogeneity design;
- table and figure list;
- robustness priority.

### Top-Field Or Top-Journal Mode

Use only when the user asks for top-field/top-journal potential or clearly wants a high-ambition research idea.

Ask whether the idea has at least one of:

- new data;
- new measurement;
- new mechanism;
- new identification;
- a sharp economics puzzle with generalizable insight.

If not, recommend an appropriate downgrade path.

## Paper Type First

Classify before diagnosing:

| Type | Core gate | Common risk |
| --- | --- | --- |
| Thesis empirical paper | data, variables, runnable model | broad topic, vague variables, correlation only |
| Policy evaluation | treated/control groups, timing, pre-trend | endogenous policy, contamination, unclear window |
| Measurement/facts paper | new measure or stable fact | no economics meaning, only charts |
| Theory paper | new mechanism, formal setup, propositions | intuition without model, no literature distinction |
| Structural/quantitative paper | model-data mapping, moments, fit, counterfactuals | black-box model, unidentified parameters |
| Policy report | facts, policy relevance, feasible options | weak evidence, promotional cases |
| High-ambition idea | puzzle, new data/mechanism/identification | blunt contribution, old question with new sample |

## Input Fields

Infer what you can. Do not stop because fields are missing.

```yaml
user_stage: undergraduate / master / phd / researcher / unknown
paper_goal: course_paper / thesis / working_paper / journal_submission / policy_report
field: labor / development / urban / finance / io / political_economy / innovation / trade / macro / other
time_limit: weeks_or_months_until_deadline
data_access: public_data / school_database / firm_data / survey_data / no_data_yet / unknown
method_level: descriptive / measurement / panel_fe / did / iv / rdd / structural / calibration / simulation / theory / unknown
advisor_preference: causal_identification / policy_relevance / simple_feasible / theory / unknown
initial_idea: user_raw_idea
must_use_data: optional
must_avoid: optional
ambition_level: thesis / excellent_thesis / working_paper / top_field / top5
```

## Missing Information Rule

When information is missing:

- give an initial diagnosis from available information;
- state assumptions briefly;
- ask at most one high-impact follow-up question at the end;
- if there is a deadline, design backward from the deadline.

## Big-Noun Compression

Convert broad topics into:

```text
In [sample/setting], does [shock/treatment/constraint] affect [outcome] through [mechanism], using [variation/comparison]?
```

If the idea is descriptive:

```text
How does [outcome/fact] vary across [groups/space/time], and what economic mechanism might explain it?
```

Use big-noun compression after the raw interest card and mandatory ideation review, not as a premature final title. If several translations are plausible, show 2-3 options and ask the user to choose or correct the intended object.
