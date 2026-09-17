# Crowded Topic Pivot Lab

## Purpose

Use this after the literature crowding gate when the student's original topic is crowded but their underlying interest is still valuable. The goal is to generate disciplined nearby thesis directions from the original topic, not to brainstorm arbitrary fashionable titles.

This module is called by `references/00_master_router.md`. It should return screened candidate branches and backup options to the router; it should not refine every branch into a full thesis blueprint.

Every generated branch must receive novelty, clarity, feasibility, effectiveness, and impact scores before it can be recommended, rejected, or stored as a backup.

## When To Use

Use this module when:

- `references/07_literature_crowding_gate.md` classifies the original idea as `high` or `saturated`;
- the student still wants to keep part of the original interest, such as digitalization, common prosperity, digital finance, ESG, smart cities, rural e-commerce, or policy experimentation;
- the user asks for alternative topics, nearby directions, rescue paths, or a way to branch out from the current idea.

Do not use this module to rescue a saturated exact topic. First state that the original X-Y package should not proceed, then generate adjacent options.

## Inputs To Extract

Start by decomposing the original idea:

| Element | Question |
| --- | --- |
| X | What is the key explanatory object, shock, technology, policy, institution, or behavior? |
| Y | What is the outcome, welfare object, distributional fact, firm behavior, or policy target? |
| Mechanisms | What channels do existing papers already claim? |
| Unit | Region, firm, household, worker, school, platform, village, industry, or other unit? |
| Data precedent | What data have close papers used? |
| Defense risk | What "what is new?" challenge made the original topic unsafe? |

## Three Search Dimensions

### 1. Horizontal Dimension

Split the original X-Y pair and search outward from each side.

- **X-side search**: keep X, drop the original Y. Ask what newer outcomes, settings, or behaviors related to X appear in Chinese top journals, English top/field journals, and recent working papers.
- **Y-side search**: keep Y, drop the original X. Ask what newer determinants, measurements, populations, or mechanisms related to Y appear in the literature.

Example pattern:

```text
Original: digitalization -> common prosperity
X-side: digitalization -> firm organization / labor matching / market integration / household risk sharing
Y-side: common prosperity -> opportunity equality / income mobility / public service access / asset accumulation
```

### 2. Vertical Dimension

Treat an existing result as one link in a mechanism chain, then move one step deeper.

Forward vertical search:

```text
X -> known mechanism M -> what downstream behavior or outcome should change?
```

Upstream vertical search:

```text
What raises or blocks M -> M -> Y?
```

Example patterns:

```text
Digitalization -> stronger communication -> firm coordination / management span / remote collaboration / information transparency
Rural e-commerce -> common prosperity; then ask what promotes rural e-commerce adoption or effectiveness
```

The mechanism must be conceptually distinct from the final outcome and measurable with realistic data. Do not simply relabel the outcome as a channel.

### 3. Reverse Dimension

Reverse the common causal direction in the literature, then re-run horizontal and vertical searches.

If close papers mostly study:

```text
X -> outcomes
```

ask:

```text
What causes X, adoption of X, diffusion of X, or local capacity to use X?
```

If close papers mostly study:

```text
determinants -> Y
```

ask whether Y itself changes later behavior, policy response, migration, investment, or institutional demand. Use this only when the reverse outcome has an economics meaning and a measurable data path.

## Literature Search Requirements

For each promising branch, inspect enough literature to avoid reinventing the same topic:

1. Search Chinese top journals and closely related Chinese economics/management journals.
2. Search English top journals, top field journals, NBER/RePEc/SSRN working papers, and recent relevant papers.
3. Record the nearest 3-5 papers per branch: question, data, method, mechanism, and remaining space.
4. If database access is unavailable, mark the branch as `literature unverified` and make literature verification the first task.

## Filtering Rules

Each branch must pass four filters before becoming a candidate thesis:

1. **Crowding**: not already the same X-Y-data-method package.
2. **Feasibility**: a credible data path, measurement path, theory model path, or structural/quantitative model-data path.
3. **Design**: an empirical, descriptive, measurement, theory, structural/quantitative, or policy-report strategy that can be explained without method decoration.
4. **Defense**: a plausible answer to "what is new compared with the closest papers?"

Reject branches that survive only by adding decorative mechanisms, arbitrary heterogeneity, a new buzzword, or an unsupported causal method.

## Readable Candidate Questions

Three-dimensional branching is an exploration stage. Do not force every branch into a maximally compressed one-sentence question. A compressed question that packs several network positions, mechanisms, and outcomes into one clause can become unreadable and make the branch look less coherent than it is.

For each branch, separate:

- **Candidate idea**: a short label, such as `知识共创-技术转让错配`.
- **Readable candidate question**: one clear question, or at most two short sentences, that a graduate student and advisor can understand without decoding hidden assumptions.
- **Key objects**: unit, X/object, Y/outcome or fact, mechanism/comparison, claim type, and likely data object.

Readable branch questions should usually name:

1. the unit or setting;
2. the economic object being compared or varied;
3. the outcome, fact, model object, or theoretical mechanism;
4. why the contrast matters economically;
5. whether the branch is causal, descriptive/measurement, theory, structural/quantitative, policy, or mixed.

Avoid questions like:

```text
城市有强知识合作网络但弱技术转让网络时，是否更难把创新转化为增长？
```

Prefer a more explicit version:

```text
在城市创新网络中，知识共创中心性和技术转让中心性是否存在系统性错配？如果一个城市能参与知识共创、但缺少技术交易和转化网络位置，这种错配是否对应更低的专利转化、企业成长或产业升级表现？
```

Only after the user selects a branch should the router compress it into a formal one-sentence research question.

## Output Template

Use this compact table before any full thesis blueprint:

| Branch | Source from original topic | Dimension | Candidate idea | Readable candidate question | Key objects | Paper type | N/C/F/E/I | Average | Closest literature pattern | Data/model path | Main design | Defense risk | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | X-side / Y-side / mechanism / reverse-X / reverse-Y | horizontal / vertical / reverse | | | unit; X/object; Y/fact; mechanism/comparison; claim type | | | | | | | | proceed / verify / pivot / park / kill |

Then give:

- **Recommended branch**: one primary direction and one backup.
- **Why not the others**: the binding risk for rejected branches.
- **First verification task**: usually a literature search plus data metadata check.
- **Do not claim yet**: causal, novelty, or mechanism claims not yet supported.
- **Selected-branch one-sentence rewrite**: only if the user has selected or accepted one branch.
- **是否继续打磨**: use natural language to say whether the branch search needs more iteration, is ready to freeze into one selected branch, can optionally continue, or should stop/change route.

Only after a branch receives `proceed` or `verify` should the normal thesis blueprint begin.

Return to `references/00_master_router.md` with: primary branch, backup branches, rejected branches, first verification task, and whether user selection is needed.

## Mini Example

For `digitalization -> common prosperity`, possible disciplined branches include:

- Horizontal X-side: digitalization and firm organization, labor matching, household risk sharing, or public service access.
- Horizontal Y-side: opportunity equality, income mobility, public service equalization, or asset accumulation as narrower common-prosperity objects.
- Vertical: digitalization improves communication, which may affect coordination, management span, remote collaboration, or information transparency.
- Reverse: what drives digitalization adoption by firms, villages, households, or local governments?

These are only seeds. Do not treat them as viable until the branch-specific literature and data checks pass.
