# Paper Reading Skills

This context defines the vocabulary for paper-reading skills that turn a reading motivation into a concrete research workflow and durable artifacts.

## Language

**Field Map Workflow**:
A complete domain-mapping workflow for entering a research direction, starting from scope boundaries and ending with paper clusters, gap analysis, and a human-readable report.
_Avoid_: Field map as a single markdown file, quick paper list

**Field Boundary**:
The explicit inclusion and exclusion criteria that define which research questions, papers, methods, systems, and benchmarks belong inside the user's current research scope.
_Avoid_: Topic, area, background

**Field Boundary Gate**:
The required clarification step before collecting papers; it is passed only when the research target, in-scope areas, out-of-scope areas, time or venue limits, user goal, and stop condition are explicit.
_Avoid_: Optional preface, rough topic note

**Proposed Field Boundary**:
An AI-drafted Field Boundary offered to the user for critique and revision before the Field Boundary Gate is passed.
_Avoid_: User questionnaire, final scope

**Field Map Workspace**:
A durable artifact set for exactly one research direction explored through a Field Map Workflow.
_Avoid_: Output folder, notes dump

**Seed Paper**:
A representative starting paper selected to anchor the field map, usually from surveys, classic works, high-citation recent papers, benchmark papers, or related systems.
_Avoid_: Random paper, first batch paper

**Seed Set**:
An initial set of roughly 8-12 Seed Papers chosen for coverage across overview, foundational, recent high-impact, benchmark, dataset, evaluation, system, or application perspectives.
_Avoid_: Top ten papers, arbitrary reading list

**Paper Position Record**:
A structured note for one paper that captures the paper's position in the field, including its problem, assumptions, method route, evaluation, contribution type, related works, contrasting works, and gaps left.
_Avoid_: Paper summary, reading notes

**Position-Oriented Reading**:
A paper-reading mode that reads only deeply enough to place a paper in the Field Map Workflow and complete its Paper Position Record.
_Avoid_: Full close reading, exhaustive summary

**Candidate Pool**:
A broad, auditable collection of papers discovered from citations, references, keyword expansion, benchmarks, leaderboards, and related-work trails before selecting which papers to read closely.
_Avoid_: Final paper set, reading list

**Selected Expansion Set**:
The roughly 25-35 non-seed papers chosen from the Candidate Pool for Paper Position Records.
_Avoid_: All discovered papers, search results

**User-Provided Paper**:
A paper directly uploaded or linked by the user, which takes priority over network-discovered papers during Field Map Workflow discovery.
_Avoid_: Local corpus, existing library

**Network Discovery**:
The default paper discovery mode when the user has not provided papers, using web search, citation trails, survey bibliographies, benchmark pages, and other online sources.
_Avoid_: Repository search, offline literature lookup

**Research Cluster**:
A group of papers that share a core problem, method route, assumptions, or evaluation setting within the field map.
_Avoid_: Category, bucket, theme

**Primary Research Cluster**:
The one Research Cluster that best explains a paper's main field position.
_Avoid_: Main category

**Secondary Research Cluster**:
An additional Research Cluster that a paper meaningfully informs without being its main field position.
_Avoid_: Tag, loose theme

**Research Opportunity**:
A possible future research direction derived from gaps across the mapped papers, such as conceptual, method, evaluation, system, or theoretical gaps.
_Avoid_: Idea, future work note

**Research Opportunity Candidate**:
A Research Opportunity backed by paper evidence and phrased so it can become a possible research question, with risks and objections recorded.
_Avoid_: Speculation, loose future work

**Research Question Workflow**:
A downstream paper-reading workflow that turns Research Opportunity Candidates from exactly one Field Map Workspace into evidence-backed Candidate Angles and Research Question Cards.
_Avoid_: Brainstorming, topic generation, generic idea search

**Research Question Card**:
A decision-ready research question artifact derived from one or more Research Opportunity Candidates, recording the question, supporting evidence, fit to the user's writing intent, feasibility, novelty, risks, and whether further paper discovery is needed.
_Avoid_: Idea card, question list item, topic note

**Problem Reality Check**:
A paper-reading workflow routed to exactly one Research Question Card before interrogation begins, stress-testing whether that card's problem is real, externally grounded, and strong enough to motivate research.
_Avoid_: General risk review, method critique, reviewer objection list

**Problem Reality Check Report**:
A durable review artifact attached to one Research Question Card, recording the problem-reality verdict, strongest supporting evidence, weak assumptions, caution points, unsafe motivation claims, and follow-up evidence needs.
_Avoid_: Risk list, paper summary, informal comments

**Problem Reality Verdict**:
The controlled final status of a Problem Reality Check Report: `problem-solid`, `needs-evidence`, `motivation-fragile`, or `reject`.
_Avoid_: Free-form confidence note, numeric score, keep/defer decision

**Unsafe Motivation Claim**:
A motivation statement that a Problem Reality Check Report warns against because it is overstated, undersupported, contradicted by evidence, too broad, or likely to be attacked during paper review.
_Avoid_: Limitation, reviewer objection, writing polish note

**Targeted Evidence Need**:
A focused evidence gap identified by a Problem Reality Check Report, phrased as a recommended next investigation without automatically launching a new paper-search workflow.
_Avoid_: Full literature review, automatic evidence collection, vague next step

**Theoretical Grounding Workflow**:
A downstream paper-reading workflow routed to exactly one Research Question Card and its completed Problem Reality Check Report, extracting Theory-Support Claims and Theory Hooks from the checked problem and turning them into a small set of theoretical traditions and a theory-backed problem framing.
_Avoid_: Theory search, literature background, theoretical justification

**Theoretical Grounding Source Gate**:
The required routing step before a Theoretical Grounding Workflow begins; it is passed only when exactly one source Research Question Card and its completed Problem Reality Check Report are identified, including the Problem Reality Verdict and any motivation fragilities or evidence needs.
_Avoid_: Optional context loading, broad theory scan

**Theory-Support Claim**:
A key judgment in the paper or project that needs theoretical support, recorded as the exact sentence to support and the reason it needs theory rather than decorative citation.
_Avoid_: Core claim, citation topic, related theory

**Problem-Theory Decomposition**:
A durable artifact in a Theoretical Grounding Workflow that decomposes the checked problem into phenomenon, mechanism, failure, Theory-Support Claims, and boundary before candidate theoretical traditions are selected.
_Avoid_: Internal reasoning, outline, theory notes

**Theory Hook**:
A concept relationship extracted from a Problem-Theory Decomposition that could be explained or supported by a theoretical tradition, such as how a source affects trustworthiness or how long-term state influences later action.
_Avoid_: Keyword, theory name, citation label

**Candidate Theoretical Tradition**:
A possible theory, conceptual lineage, or research tradition considered because it can explain one or more Theory Hooks or support one or more Theory-Support Claims.
_Avoid_: Famous theory, citation candidate, background area

**Selected Theoretical Tradition**:
A Candidate Theoretical Tradition kept for the final grounding because it directly supports a Theory-Support Claim, explains a Theory Hook, has clear boundaries, and can shape the problem framing.
_Avoid_: Best-known theory, related work cluster, decorative citation

**Targeted Theory Search**:
A narrow paper-search step inside a Theoretical Grounding Workflow that the agent should run by default to verify Candidate Theoretical Traditions and representative sources for specific Theory Hooks or Theory-Support Claims without mapping the whole field.
_Avoid_: Field map, broad literature review, theory brainstorming

**Provisional Theoretical Grounding**:
A theory-backed framing draft whose Candidate Theoretical Traditions have not yet been fully verified with representative sources after Targeted Theory Search is unavailable, explicitly deferred, or insufficient.
_Avoid_: Final theoretical grounding, unsupported theory list

**Theory Evidence Need**:
A remaining source gap recorded only after Targeted Theory Search is unavailable or insufficient, naming the affected Theory-Support Claim, the missing source type, and the search question needed to stabilize the theoretical framing.
_Avoid_: User homework, vague citation gap, general bibliography need

**Theoretical Grounding Workspace**:
A durable artifact set for grounding checked Research Question Cards from exactly one Research Question Workspace, organized around source-problem routing, per-card grounding folders, Theory Hooks, selected theoretical traditions, and final theory-backed framing.
_Avoid_: Problem Reality Check folder, theory notes folder, background reading dump

**Theoretical Pillar**:
A claim-centered theoretical support structure in a Theoretical Grounding Report, linking one Theory-Support Claim to the Selected Theoretical Traditions that support it, the boundaries of that support, and the framing change it enables.
_Avoid_: Theory list, background section, named citation cluster

**Theoretical Grounding Report**:
The final artifact of a Theoretical Grounding Workflow, containing a theory-backed problem framing, Theoretical Pillars organized by Theory-Support Claim, framing changes from the original Research Question Card, and remaining fragilities or evidence needs.
_Avoid_: Theory summary, related work section, citation list

**Theoretical Tradition Selection Gate**:
The required confirmation step before writing a Theoretical Grounding Report; it is passed only when the user confirms, revises, or explicitly delegates the 2-4 Selected Theoretical Traditions and their rationale.
_Avoid_: Automatic theory choice, hidden selection, final theory list

**Method Inspiration Source Gate**:
The required routing step before a Method Inspiration Workflow begins; it is passed only when exactly one Research Question Card or one Source Problem Brief is identified, with the evidence status and reason for method search recorded.
_Avoid_: Source Problem Gate, loose problem note, implicit method-starting context

**Source Problem Brief**:
A user-provided problem record that can provisionally start Method Inspiration when no Research Question Card is available, naming the target problem, failure scenario, intended intervention point, constraints, non-goals, and evidence status.
_Avoid_: Rough idea, topic note, method prompt

**Method Inspiration Workflow**:
A downstream paper-reading workflow that turns one Research Question Card or Source Problem Brief into a Method Candidate Library through method-need decomposition, targeted method search, pattern extraction, transfer mapping, and candidate-method assembly.
_Avoid_: Method brainstorm, architecture design, related-work scan

**Method Inspiration Boundary**:
The boundary that Method Inspiration stops at auditable Candidate Methods and must not ask the user to immediately commit to a paper's actual core method; the human researcher owns the later jump from inspiration to a committed or explicitly blocked method outcome.
_Avoid_: Agent-generated final method, automatic novelty creation, complete method design, quick commitment prompt

**Method Commitment Workflow**:
An independent convergence workflow that turns one confirmed Source Method and the researcher's own judgment into a human-owned committed, provisional, redesign, or rejection outcome. It may follow Method Inspiration, start from a user-authored method, or reconstruct a method from chat, but it must not treat a Candidate Method as already committed.
_Avoid_: Method Inspiration final step, quick synthesis prompt, agent-owned method invention, automatic candidate-method selection

**Source Method**:
The confirmed rough method input to a Method Commitment Workflow, normalized from exactly one selected Candidate Method, user-authored method, hybrid method, or reconstructed chat method and bound to exactly one Method Commitment Source Problem before commitment begins.
_Avoid_: Candidate Method by default, final method, loose method idea

**Method Source Mode**:
The recorded origin type for a Source Method, such as `selected-candidate-method`, `user-authored-method`, `hybrid-method`, or `reconstructed-from-chat`. When multiple Candidate Methods or inspirations are merged, the mode must be `hybrid-method` and must preserve borrowed pieces, discarded pieces, merge rationale, and the new weakest link.
_Avoid_: Hidden merge, selected candidate by default, vague source, automatic synthesis

**Method Commitment Source Problem**:
The exactly one Research Question Card, Source Problem Brief, or confirmed problem statement that a Source Method is being committed against in the current Method Commitment Workflow.
_Avoid_: General application area, multiple target problems, future generalization, transferable use case

**Method Commitment Source Gate**:
The required routing and confirmation step before a Method Commitment Workflow reconstructs or attacks the method; it is passed only when exactly one Source Method and exactly one Method Commitment Source Problem have been recorded and confirmed or explicitly delegated.
_Avoid_: Optional source note, implicit chat context, automatic source reconstruction

**Method Commitment Context Review**:
The required local-artifact review after the Method Commitment Source Gate, preserving relevant source-problem evidence, Problem Reality Check fragilities, unsafe motivation claims, close-work risks, Method Needs, Candidate Methods, Method Patterns, and Method Candidate Library judgments before method attack begins.
_Avoid_: Clean-slate method drafting, default web search, forgetting prior fragilities, broad literature refresh

**Method Design Attack Pass**:
A method-focused interrogation step inside a Method Commitment Workflow that stress-tests the Source Method's structure, mechanism, assumptions, novelty boundary, feasibility, and downstream consequences before commitment. High-risk dimensions require live Challenge Questions; low-risk dimensions may be recorded as cleared from artifacts.
_Avoid_: Problem Reality Check, one-shot method critique, generic reviewer objections, silent agent judgment

**Method Attack Transcript**:
A durable turn-by-turn record of a Method Design Attack Pass, capturing each high-risk Challenge Question, the provisional recommendation, the user's response or explicit delegation, and the resulting design decision.
_Avoid_: Final report, hidden reasoning, informal notes, complete attack report without user responses

**Method Decision Log**:
A durable decision record inside a Method Commitment Workflow that captures only structure-changing method decisions, such as source mode, hybrid merge rationale, method boundary, Mechanistic Claim revision, weakest link, blockers, and final status.
_Avoid_: Chat transcript, meeting notes, full attack transcript, implementation changelog

**Method Commitment Gate**:
The final confirmation step in a Method Commitment Workflow, requiring the researcher to confirm the method thesis, Mechanistic Claim, method boundary, weakest link, and any intentionally unfrozen open decisions before a Method Commitment Status is assigned.
_Avoid_: Silent finalization, unchecked weak link, hidden open decision, automatic downstream routing

**Explicit Method Commitment Confirmation**:
A direct researcher confirmation that a method should receive `committed` Method Commitment Status and become downstream-ready. Agent recommendation, broad delegation, or "you decide" is not enough; without explicit confirmation, an otherwise stable method remains provisionally committed with a blocker.
_Avoid_: Implicit approval, generic delegation, agent-owned commitment, silent downstream routing

**Method Inspiration Workspace**:
A durable artifact set for method inspiration from exactly one field context, organized around source-problem routing, per-problem inspiration folders, Method Needs, Method Patterns, Transfer Mappings, Candidate Methods, and Method Candidate Libraries.
_Avoid_: Method notes folder, architecture folder, paper dump

**Method Need**:
A problem-derived functional requirement for a method, naming the target failure, intervention point, required capability, expected inputs and outputs, constraints, success signal, and evidence status.
_Avoid_: Model module, feature idea, implementation component

**Method Need Decomposition**:
A durable artifact in a Method Inspiration Workflow that turns the source Research Question Card or Source Problem Brief into Method Needs before method papers are searched.
_Avoid_: Architecture plan, module list, generic requirements document

**Method Needs Confirmation Gate**:
The required confirmation step after Method Need Decomposition; it is passed only when the user confirms, revises, or explicitly delegates the Method Needs before Targeted Method Search proceeds.
_Avoid_: Hidden requirement inference, automatic method search, informal needs check

**Targeted Method Search**:
A narrow paper-search step inside a Method Inspiration Workflow that looks for method ideas for specific Method Needs across Same-Problem Papers, Adjacent-Problem Papers, and Far-Analogy Papers.
_Avoid_: Method Paper Search, broad related work search, baseline selection

**Method Search Sufficiency Check**:
A coverage-based check in a Method Inspiration Workflow that decides whether each core Method Need has enough Same-Problem, Adjacent-Problem, and Far-Analogy evidence to extract Method Patterns and move toward assembly, or should remain marked as `needs-search`.
_Avoid_: Fixed paper-count target, exhaustive search, arbitrary stopping point

**Same-Problem Paper**:
A method-search candidate that directly addresses the same or highly similar problem as the source Research Question Card or Source Problem Brief.
_Avoid_: Baseline by default, any paper from the same field

**Adjacent-Problem Paper**:
A method-search candidate whose problem differs from the source problem but whose mechanism, failure mode, or required capability matches one or more Method Needs.
_Avoid_: Same-topic paper, loosely related paper

**Far-Analogy Paper**:
A method-search candidate from a more distant field whose method structure can transfer to one or more Method Needs despite substantial domain or task differences.
_Avoid_: Inspirational citation, random analogy, metaphor

**Method Pattern**:
A reusable method design pattern extracted from a paper, tied to a source URL, source paper type, matched Method Need, original setting, core mechanism, Transferable Unit, assumptions, inputs and outputs, integration cost, transfer risk, and evidence strength.
_Avoid_: Paper summary, full method copy, implementation recipe

**Transferable Unit**:
The smallest reusable design element inside a Method Pattern, such as a module, objective, training flow, inference flow, data construction step, filter, router, memory update, critic, or controller.
_Avoid_: Whole architecture, inspiration, vague lesson

**Transfer Mapping**:
A durable artifact in a Method Inspiration Workflow that decides how Method Patterns transfer into the source problem by recording Need-Pattern Fit before assigning any Assembly Role.
_Avoid_: Direct architecture design, analogy note, method mashup

**Need-Pattern Fit**:
The fit judgment between one Method Pattern and one Method Need, naming the matched capability, mismatch, required adaptation, transfer boundary, and whether the pattern is eligible for candidate-method assembly.
_Avoid_: Similarity score, relevance note, citation match

**Assembly Role**:
The role a Method Pattern may play inside a candidate method after Need-Pattern Fit is established, such as input processor, retriever, planner, memory manager, critic, training objective, data generator, evaluation proxy, or controller.
_Avoid_: Model component by default, paper label, arbitrary module name

**Candidate Method Assembly**:
A workflow step that combines eligible Method Patterns into 3-5 comparable Candidate Methods, making coverage, roles, flows, novelty hypotheses, weak links, feasibility, and experiment implications explicit.
_Avoid_: Single best method, architecture drafting, method brainstorming

**Candidate Method**:
A possible method design assembled from Method Patterns, recording its method thesis, covered and uncovered Method Needs, Assembly Roles, inputs, modules, outputs, training or inference flow, source papers, novelty hypothesis, weakest link, feasibility, experiment implications, and status.
_Avoid_: Final method, implementation plan, idea sketch

**Committed Method Design**:
A human-owned method design with `committed` Method Commitment Status, stable enough to serve as the source method for experiment design or research-framing workflows. Baseline and metric selection now belong inside the Experiment Design Workflow.
_Avoid_: Candidate Method, provisionally committed method, agent-generated method, real method

**Method Thesis**:
The paper-level method claim in a Candidate Method or Committed Method Design, stating what mechanism is introduced at what intervention point to improve what target outcome under what scope.
_Avoid_: Method name, contribution slogan, implementation summary

**Mechanistic Claim**:
The attackable causal hypothesis inside a Committed Method Design that explains why the proposed mechanism should improve the target outcome. It is the claim that ablations, baselines, metrics, and reviewer objections should pressure-test.
_Avoid_: Method Thesis, intuition, expected result, novelty claim

**Method Commitment Downstream Pressure Point**:
A routing hint recorded in a Committed Method Design that names the ablations, baseline pressures, and metric signals implied by the method's Mechanistic Claim without designing the full experiment protocol.
_Avoid_: Complete experiment design, final baseline set, metric formula, evaluation protocol

**Method Commitment Status**:
The controlled final status of a Method Commitment Workflow: `committed`, `provisionally-committed`, `needs-redesign`, or `reject-current-method`. Only `committed` is downstream-ready; `provisionally-committed` records a nearly stable design with named Method Commitment Blockers, not a normal source for downstream workflows.
_Avoid_: Confidence score, proof of novelty, experiment result, paper acceptance prediction

**Method Commitment Blocker**:
A named unresolved issue that prevents a provisionally committed method from entering downstream workflows, such as an unstable Mechanistic Claim, unresolved weakest link, close-work saturation risk, missing feasibility evidence, missing explicit human commitment, or intentionally unfrozen design decision.
_Avoid_: Minor TODO, hidden caveat, generic limitation, downstream routing hint

**Method Commitment Output Artifact**:
The status-aligned final artifact of a Method Commitment Workflow, chosen from Committed Method Design, Provisional Method Design, Method Redesign Brief, or Method Rejection Note according to the Method Commitment Status.
_Avoid_: Status-neutral final method file, misleading committed artifact, hidden blocked outcome

**Method Commitment Summary**:
The always-present routing summary for a Method Commitment Workflow, recording the Source Method, Method Commitment Source Problem, Method Commitment Status, output artifact, blockers, next recommended workflow, and do-not-route warnings.
_Avoid_: Final method design, duplicate output artifact, unstructured index note

**Experiment Design Workflow**:
A downstream paper-reading workflow that turns one source method or research question into a claim-to-evidence experiment plan, including tasks, datasets, protocols, baseline pressures, metric signals, ablations, controls, result interpretation, and human evaluation or user studies when needed. It starts from what must be proven or refuted, not from benchmark, baseline, or metric lists.
_Avoid_: Separate baseline workflow, separate metric workflow, benchmark list, metric bank, loose experiment brainstorm

**Experiment Design Source Gate**:
The required routing step before an Experiment Design Workflow begins; it is passed only when the source artifact, source status, key claims, target outcome, target failure, intervention point, scope boundaries, and inherited do-not-route warnings are explicit. A Committed Method Design is the normal source; rough methods or Research Question Cards produce provisional experiment designs.
_Avoid_: Implicit source, hidden provisional status, using blocked method designs as normal sources

**Experiment Source Decision Packet**:
A bounded Source Gate confirmation unit that identifies exactly one candidate experiment source, its source status, Method Thesis or research question, Mechanistic Claim when available, target failure, intervention point, inherited warnings, and recommended routing. It does not preview benchmarks, baselines, metrics, or protocol choices.
_Avoid_: Source-free experiment start, rough method prompt, early benchmark discussion

**Minimal Experiment Brief**:
A provisional source-context record used when Experiment Design starts from a Research Question Card, Source Problem Brief, rough method, or non-committed source, naming the Method Thesis or question, Mechanistic Claim if available, target failure, intervention point, scope, non-goals, weakest link, main reviewer objection, and provisional status.
_Avoid_: Method commitment substitute, final experiment context, hidden rough source

**Provisional Experiment Sketch**:
An automatically generated or under-confirmed experiment design draft that may organize likely claims, routes, baselines, metrics, and ablations, but has not passed the required Experiment Design gates and must not be treated as a final experiment plan.
_Avoid_: Final experiment design, confirmed protocol, validation plan

**Claim-Evidence Map**:
A durable artifact in an Experiment Design Workflow that decomposes the Method Thesis, Mechanistic Claim, assumptions, and target outcomes into the observable evidence needed to support or reject each claim, including evidence routes, evidence strength, reviewer objections, and failure interpretations.
_Avoid_: Dataset-first experiment plan, ungrounded metric list, vague validation idea

**Claim-Evidence Decision Packet**:
A bounded confirmation unit for one core claim in a Claim-Evidence Review Gate, showing the claim, source, proposed evidence route, what the route can and cannot prove, proxy risk, and the agent's recommended decision.
_Avoid_: Full-map approval, hidden route choice, oversized confirmation prompt

**High-Risk Claim Challenge**:
A live challenge inside the Claim-Evidence Review Gate that tests one risky claim-to-evidence decision before the claim's evidence route can be accepted, especially when the route relies on a weak proxy, misses the target failure, or avoids needed human evidence.
_Avoid_: Generic concern, optional reviewer note, post-hoc limitation

**Claim-Evidence Review Gate**:
The required confirmation step before benchmark, baseline, metric, or protocol selection begins; it proceeds through Claim-Evidence Decision Packets and required High-Risk Claim Challenges, and is passed only after the key claim decomposition and evidence routes are reviewable and the user's decision is recorded.
_Avoid_: Silent claim decomposition, dataset-first routing, hidden proxy choice

**Stepwise Gate Confirmation**:
A workflow confirmation pattern where the agent presents one bounded decision packet, gives a recommended answer, and waits for the user to confirm, revise, or explicitly delegate before moving to dependent decisions.
_Avoid_: Batch approval, implied delegation, one-shot workflow run

**Gate-Scoped Delegation**:
An explicit user delegation that applies only to the named gate or decision packet currently under review, after the agent has shown the relevant decisions and recommendation. It cannot carry across workflow gates or silently waive High-Risk Claim Challenges.
_Avoid_: Blanket delegation, inherited approval, silent challenge waiver

**Gate-Bound Artifact Drafting**:
A workflow writing pattern where artifacts may be drafted before a gate passes, but dependent downstream artifacts cannot be finalized or treated as accepted until the relevant gate status and user decision are recorded.
_Avoid_: Final-looking drafts, downstream artifact leapfrogging, delayed gate record

**Evidence Route**:
The kind of study or analysis chosen to support or refute a claim, such as standard benchmark, targeted workload, synthetic controlled task, real-world case study, ablation, stress test, human evaluation, user study, or error analysis.
_Avoid_: Dataset choice, metric choice, generic experiment idea

**Experiment Stack**:
The claim-aligned set of experiment layers selected for an Experiment Design Workflow, such as main effect, mechanism or ablation, robustness, generalization, human evaluation or user study, efficiency, and failure analysis.
_Avoid_: Single benchmark run, experiment checklist, fixed required template

**Evidence Strength Label**:
A controlled label for how directly an experiment result supports a claim, such as direct evidence, strong proxy, weak proxy, anecdotal evidence, or speculative design assumption.
_Avoid_: Confidence score, statistical significance, proof

**Baseline Pressure Matrix**:
A durable artifact in an Experiment Design Workflow that selects baselines by the claim or reviewer objection they pressure-test, including close work, strong recent methods, classic expected baselines, lower bounds, component-equivalent baselines, ablated variants, and upper bounds when meaningful.
_Avoid_: Baseline list, popularity-based inclusion, hiding difficult close work

**Claim-Metric Map**:
A durable artifact in an Experiment Design Workflow that links each key claim to an observable construct, primary and diagnostic metrics, measurement protocol, improvement direction, success criterion when known, and validity risks.
_Avoid_: Metric bank, proxy metric without claim mapping, metric formula detached from protocol

**Ablation And Control Plan**:
A durable artifact in an Experiment Design Workflow that tests the Mechanistic Claim through component removals, intervention-point ablations, data-source ablations, stress tests, negative controls, sanity checks, and confound checks.
_Avoid_: Decorative ablation list, one-off component removal, unchecked leakage or unfair comparison

**Result Interpretation Contract**:
A pre-results agreement in an Experiment Design Workflow that states what major success, failure, proxy mismatch, ablation, baseline, or human-evaluation result patterns would imply for the claim, method, or paper story.
_Avoid_: Post-hoc explanation, success-only expectation, result summary

**Experiment Design Review Packet**:
A bounded confirmation unit inside the Experiment Design Review Gate for one dependent design decision, such as the Experiment Stack, task or dataset protocol, baseline pressure, metric validity, ablations and controls, or Result Interpretation Contract.
_Avoid_: Final-bundle approval, all-artifact approval, hidden design dependency

**Experiment Design Review Gate**:
The final confirmation step before an Experiment Design Workflow treats its artifacts as a final experiment plan; it proceeds through Experiment Design Review Packets in dependency order and is passed only when the claim decomposition, evidence routes, experiment stack, baselines, metrics, ablations, controls, and result interpretations are accepted and the user's decision is recorded.
_Avoid_: Silent final plan, agent-owned experiment design, human evaluation study

**Research Framing Workflow**:
A downstream paper-reading workflow that turns one stable Research Framing Source Chain into paper-facing expression by comparing closest related works, checking claim-level citation support, clarifying positioning, identifying contribution highlights, and extracting reusable writing moves.
_Avoid_: Citation support as a separate workflow, positioning-only check, writing-style collection, broad related-work scan

**Research Framing Source Chain**:
The exactly one upstream research lineage selected for a Research Framing Workflow, usually ending at a reviewed Experiment Design and tracing back through its source method and source question when present. The chain may be entered through its leaf artifact, but framing must not bundle multiple alternative questions, methods, or experiments as coequal sources.
_Avoid_: Source collage, experiment-only pointer, all upstream artifacts as separate sources

**Research Framing Leaf Source**:
The deepest stable artifact currently available in a Research Framing Source Chain, preferred in order from reviewed Experiment Design to Committed Method Design to Research Question Card. A leaf source determines how final or provisional the framing may be.
_Avoid_: Arbitrary source choice, shallow source when a deeper stable source exists, multiple leaf sources

**Source Chain Trace**:
The provenance summary inside a Research Framing Package that names the Research Framing Leaf Source, the upstream artifacts it traces through, and the source statuses or gates that make the chain stable or provisional.
_Avoid_: Current experiment summary, bibliography provenance, hidden workspace lookup

**Research Framing Context Review**:
The required local-artifact review after the Research Framing Source Gate, preserving the leaf source's claims, evidence routes, baseline pressures, metric validity risks, ablations, unsafe claims, and upstream warnings before building the Close Work Set. When the leaf source is an Experiment Design, the Baseline Pressure Matrix is the primary local source for initial close-work candidates.
_Avoid_: Clean-slate paper search, ignoring experiment baselines, broad related-work reset

**Research Framing Source Gate**:
The required routing step before a Research Framing Workflow begins; it is passed only when exactly one Research Framing Source Chain, its stable and provisional claims, known close works, writing goal, and scope boundaries are explicit.
_Avoid_: Draft polishing without source status, broad paper-writing help, hidden unstable claims

**Close Work Selection Gate**:
The required Research Framing confirmation step that fixes the 3-8 Close Works and their Close Work Threat Roles before final positioning, story, or claim-safety decisions are made.
_Avoid_: Hidden close-work choice, convenient citation set, story-first related work

**Story And Claim Safety Gate**:
The required Research Framing confirmation step before writing the final package, checking the One-Sentence Paper Pitch, novelty boundary, safe claims, claims to avoid, and any claim downgrades required by the Claim Support Bank or Result Claim Boundary.
_Avoid_: Overclaimed introduction, unchecked novelty boundary, planned evidence as result

**Close Work Set**:
The 3-8 papers, systems, benchmarks, or methods that most strongly define how the user's current research must be compared, positioned, and cited in a paper.
_Avoid_: General bibliography, field map cluster, all related work, convenient citations

**Close Work Threat Role**:
The reason a Close Work belongs in the Close Work Set, such as same-problem work, same-method-family work, same-setting or system work, same-evaluation work, baseline-threat work, or novelty-threat work. One Close Work may fill multiple threat roles, and the set should not be padded just to fill every role.
_Avoid_: Related-work category, citation theme, one-paper-per-bucket quota

**Claim Support Bank**:
A durable artifact in a Research Framing Workflow that maps each paper-facing claim to sources that directly support, weakly support, narrow, contradict, or merely background the claim, with safer wording recorded when support is too thin. Claim types are motivation, gap, novelty, mechanism, method, evaluation, practical relevance, and limitation.
_Avoid_: Citation list, bibliography dump, decorative references, unsupported motivation prose

**Result Claim Boundary**:
The rule that Research Framing must not state outcome-achieved empirical claims before the relevant experiment results exist; planned evidence must be phrased as evaluation intent, expected evidence, or a claim to test.
_Avoid_: Planned evidence as result, our method improves without results, validation language before validation

**Positioning Matrix**:
A durable artifact in a Research Framing Workflow that compares the user's work with the Close Work Set across problem, method, setting, assumptions, evidence, contribution type, and novelty boundary.
_Avoid_: Similarity table, related-work summary, uniqueness proof, baseline selection

**Paper Story Spine**:
The compact narrative route for the current research, connecting known situation, unresolved tension, close-work limitation, proposed intervention, evidence plan, and contribution highlights. It is finalized after the Close Work Set, Positioning Matrix, and Claim Support Bank have constrained what the paper can safely say.
_Avoid_: Abstract draft, marketing slogan, source-only story, generic motivation outline

**One-Sentence Paper Pitch**:
The single paper-level sentence that states the central problem or tension, the setting, the proposed method or intervention, and the expected evidence or contribution. It controls the framing emphasis but is not necessarily final abstract prose, and should be constrained by close-work comparison and claim support.
_Avoid_: Slogan, title, source-only pitch, full abstract, contribution list

**Contribution Highlight**:
A paper-facing point worth foregrounding because it is both true of the user's current research and differentiating against the Close Work Set.
_Avoid_: Feature list, overclaim, novelty claim without comparison

**Writing Move Library**:
A durable intermediate artifact in a Research Framing Workflow that extracts reusable rhetorical structures from close papers, such as gap packaging, related-work transitions, contribution lists, limitation handling, and figure or table patterns, without copying prose. Its usable insights are absorbed into the Paper Writing Blueprint rather than presented as a standalone final-package section.
_Avoid_: Phrase bank, final package section, paraphrase source, style mimicry, quote collection

**Paper Writing Blueprint**:
The final writing-facing outline in a Research Framing Package, usually covering the introduction route, related-work route, and contribution bullets derived from the story, positioning, claim support, and writing moves.
_Avoid_: Full paper draft, generic template, raw writing-move notes

**Research Framing Package**:
The final artifact of a Research Framing Workflow, bound to one Research Framing Source Chain and containing the source research summary, One-Sentence Paper Pitch, Paper Story Spine, Close Work Set, Positioning Matrix, Claim Support Bank, safe claims, claims to avoid, and Paper Writing Blueprint.
_Avoid_: Separate citation bank, separate positioning matrix, separate writing template, polished paper section

**Provisional Framing Sketch**:
An under-stabilized Research Framing output used when the leaf source is only a Committed Method Design, Research Question Card, proposal draft, user brief, or otherwise lacks a reviewed Experiment Design or equivalent stable experiment plan. It may preview pitch, story, close work, positioning, and safe claims, but must mark missing experiment-backed evidence and must not be treated as a Research Framing Package.
_Avoid_: Final package, paper-ready framing, hidden provisional status

**Provisional Method Design**:
The final artifact of a Method Commitment Workflow when the Method Commitment Status is `provisionally-committed`, recording the nearly stable method design together with the Method Commitment Blockers that prevent downstream routing.
_Avoid_: Committed Method Design, downstream source method, vague draft

**Method Redesign Brief**:
The final artifact of a Method Commitment Workflow when the Method Commitment Status is `needs-redesign`, recording why the Source Method is not structurally stable, which parts remain salvageable, and what redesign decisions are required next.
_Avoid_: Committed Method Design, failed final method, vague TODO note

**Method Rejection Note**:
The final artifact of a Method Commitment Workflow when the Method Commitment Status is `reject-current-method`, recording why the current Source Method should not proceed and which assumptions, fit claims, or feasibility constraints failed.
_Avoid_: Committed Method Design, soft redesign, hidden rejection

**Method Candidate Library**:
The final artifact of a Method Inspiration Workflow, containing several Candidate Methods plus the selected, deferred, and rejected Method Patterns, transfer judgments, source URLs, risks, disposition reasons, and evidence statuses needed to compare and later revise them.
_Avoid_: Method summary, chosen architecture, paper list

**Method Pattern Disposition**:
The recorded outcome for a Method Pattern after Transfer Mapping, such as selected for assembly, deferred, or rejected, with reasons such as mismatch, too-strong assumptions, high integration cost, weak evidence, or excessive similarity to a baseline.
_Avoid_: Hidden discard, gut-feel filtering, unexplained exclusion

**Candidate Method Selection Gate**:
The required confirmation step before finalizing the Method Candidate Library; it is passed only when the user confirms, revises, replaces, or explicitly delegates the 3-5 Candidate Methods and their assembly rationales.
_Avoid_: Automatic final method choice, unconfirmed architecture, single winner, choosing a Committed Method Design

**Problem Reality Check Workspace**:
A durable artifact set for single-card Problem Reality Checks from exactly one Research Question Workspace, organized around source-card routing, per-card check reports, cross-report comparison, and evidence needs.
_Avoid_: Research Question Workspace subfolder, comments folder, review notes dump

**Source Card Gate**:
The required routing step before a Problem Reality Check begins; it is passed only when exactly one source Research Question Card is identified and its key metadata is recorded.
_Avoid_: Optional card selection, broad question-area review

**Reality Check Dimension**:
A required interrogation lens inside a Problem Reality Check, covering one aspect of whether the Research Question Card's problem is real, grounded, supported, unsolved, safely motivated, and well-scoped.
_Avoid_: Loose checklist item, score category, reviewer comment type

**Challenge Question**:
An attack-style but answerable question inside a Problem Reality Check, pairing a skeptical claim with the hidden assumption being tested, the evidence that would satisfy the challenge, and the recommended answer or likely verdict.
_Avoid_: Generic checklist prompt, yes/no question, vague concern

**Interrogation Transcript**:
A durable turn-by-turn record of a Problem Reality Check, capturing each Challenge Question, the agent's provisional recommendation, the user's response or correction, and the resulting dimension verdict before the final report is written.
_Avoid_: One-shot report, hidden reasoning, informal chat log

**Research Question Workspace**:
A durable artifact set for research-question selection derived from exactly one Field Map Workspace and organized around candidate angles, writing intent, and Research Question Cards.
_Avoid_: Field map subfolder, brainstorming folder, topic shortlist

**Writing Intent**:
The user's explicit priority order for choosing research questions, including the main paper-writing goal, secondary goals, and practical constraints that shape how Research Opportunity Candidates are turned into Research Question Cards.
_Avoid_: Preference, taste, vague goal

**Guided Choice**:
A narrowing interaction in which the agent offers multiple viable options or a binary tradeoff before asking the user to choose, so research-question selection converges through comparison instead of single-option confirmation.
_Avoid_: Single recommendation, yes/no confirmation, open-ended preference question

**Candidate Angle**:
A narrower research cut derived from a Research Opportunity Candidate and shaped by a possible contribution type, such as benchmark, method, system, study, theory, or evaluation protocol.
_Avoid_: Subtopic, idea variant, direction

**Contribution Type**:
The primary kind of research contribution a Candidate Angle is expected to make, such as benchmark, evaluation protocol, defense method, system, human study, conceptual model, or empirical measurement.
_Avoid_: Paper type, format, flavor

**Evidence Sufficiency Check**:
A gate in the Research Question workflow that decides whether a Candidate Angle has enough paper-backed support to become a Research Question Card, needs targeted evidence collection, or should be deferred.
_Avoid_: Gut check, confidence score, quick validation

**Supporting Evidence**:
Additional paper-backed evidence collected during the Research Question workflow to support a Candidate Angle or Research Question Card when the source Field Map Workspace is not sufficient.
_Avoid_: Proof, justification text, invented support

**Field Map Report**:
A zero-build static HTML report inside a Field Map Workspace that organizes the boundary, seed set, search strategy, clusters, paper table, opportunities, and next actions for human reading.
_Avoid_: Web app, dashboard

**Workspace Presentation**:
A curated, interactive presentation artifact generated from exactly one source workspace or one source chain for review, handoff, rereading, or continuing the research. It treats source artifacts as the facts of record, uses a Derived Presentation Layer to decide which files and sections deserve user-facing display, foregrounds the current research state, key judgments, evidence, risks, and next actions, and preserves links or previews for the complete source files rather than becoming a second editable copy.
_Avoid_: Full workspace dump, multi-workspace collage, replacement for source artifacts, workspace editor, slide deck

**Derived Presentation Layer**:
An agent-generated, source-linked display layer inside a Workspace Presentation that selects, condenses, or reorganizes source artifacts so users can quickly understand the research state without reading every process file. It may summarize cumbersome artifacts, but it must keep source links visible and must not become the editable facts of record.
_Avoid_: New source artifact, hidden rewrite, unsourced summary, direct workspace edit

**Primary Display Artifact**:
A source artifact that should be shown directly in a Workspace Presentation because it contains final or near-final user-facing research state rather than internal process detail.
_Avoid_: Every markdown file, hidden process note

**Summarize-Then-Link Artifact**:
A source artifact that contains important decisions, evidence, or risks but is too process-heavy or cumbersome for default direct display, so the Derived Presentation Layer summarizes it and links to the source file.
_Avoid_: Hidden decision record, copied full transcript, unsourced condensation

**Link-Only Artifact**:
A source artifact that is template-like, mechanical, repetitive, provisional, or mainly useful for audit, so it is linked or tucked into a source-file drawer without becoming a main reading module.
_Avoid_: Deleted artifact, ignored source, primary reading section

**Presentation Display Map**:
The workflow-specific rule set that classifies source artifacts as Primary Display, Summarize-Then-Link, or Link-Only and orders them into the Workspace Presentation sections a user should read.
_Avoid_: Ad hoc page layout, full file listing, hidden display judgment

**Presentation Module Summary**:
A source-linked, agent-generated summary for one presentation module, combining short prose with lightweight extracted fields so a Workspace Presentation can show decisions, evidence, risks, and next actions in scannable form.
_Avoid_: Source artifact rewrite, free-floating summary, strict parser output

**Presentation Source Gate**:
A lightweight confirmation step before generating a Workspace Presentation, fixing exactly one source workspace or source chain, the presentation slug, detected workflow coverage, output path, update mode, and major display modules.
_Avoid_: Research workflow gate, broad workspace scan, accidental presentation source

## Example Dialogue

Dev: "Should `field map` just output `research_clusters.md`?"

Domain expert: "No. Use **Field Map Workflow** for the full process. It creates one **Field Map Workspace**, starts with the **Field Boundary**, uses **Seed Papers** to expand the literature set, groups papers into **Research Clusters**, and ends by naming **Research Opportunities**."

Dev: "Should we run a broad reviewer-objection pass on all three question cards?"

Domain expert: "Not for problem motivation. Use a **Problem Reality Check** after the **Source Card Gate** selects exactly one **Research Question Card**. The check asks one **Challenge Question** at a time, records an **Interrogation Transcript**, then writes one **Problem Reality Check Report**, assigns a **Problem Reality Verdict**, flags **Unsafe Motivation Claims**, and records **Targeted Evidence Needs** without launching a new paper search."

Dev: "Can the theoretical grounding skill just list provenance theory, trust theory, and governance theory?"

Domain expert: "No. Use a **Theoretical Grounding Workflow** only after the **Theoretical Grounding Source Gate** finds one checked card and its completed **Problem Reality Check Report**. First write a **Problem-Theory Decomposition**, confirm the **Theory-Support Claims**, extract **Theory Hooks**, run **Targeted Theory Search**, then keep only **Selected Theoretical Traditions** that support claim-centered **Theoretical Pillars** in the final **Theoretical Grounding Report**. If sources are still thin after search, record a **Theory Evidence Need** instead of pretending the theory support is final."

Dev: "Can method inspiration start from a rough problem?"

Domain expert: "Yes, but call the routing step the **Method Inspiration Source Gate**. Prefer one **Research Question Card** as the source; if the user only has a rough problem, write a **Source Problem Brief** and mark downstream method candidates as provisional until the problem has been checked."

Dev: "Should method inspiration end by asking the user to choose the final method?"

Domain expert: "No. Respect the **Method Inspiration Boundary**: 05 ends with a **Method Candidate Library**, not a **Committed Method Design**. A later **Method Commitment Workflow** starts only after one **Source Method** is confirmed, and that Source Method may come from a selected Candidate Method, a user-authored method, a hybrid method, or a reconstructed chat method."

Dev: "If the method idea is already in chat, can Method Commitment just proceed?"

Domain expert: "No. Even chat-derived ideas must pass the **Method Commitment Source Gate** by being normalized into one confirmed **Source Method** before reconstruction, attack, or commitment begins."

Dev: "Can one Source Method be committed for several related problems at once?"

Domain expert: "No. A **Source Method** must be bound to exactly one **Method Commitment Source Problem** in the current run. Transferability can be recorded, but the commitment target cannot be a bundle of future use cases."

Dev: "If we choose CM-1 but borrow CM-3's lifecycle state machine, is that still a selected candidate method?"

Domain expert: "No. The **Method Source Mode** is `hybrid-method` whenever multiple Candidate Methods or inspirations are merged. Record what was borrowed, what was discarded, why the merge is coherent, and what new weakest link it creates."

Dev: "Can Method Commitment just read the Source Method and ignore earlier artifacts?"

Domain expert: "No. Run a **Method Commitment Context Review** so prior Problem Reality Check fragilities, unsafe motivation claims, close-work risks, Method Needs, Candidate Methods, Method Patterns, and library judgments are inherited. Do not default to a new web search."

Dev: "Can Method Commitment generate a full attack report in one shot?"

Domain expert: "No. Run a **Method Design Attack Pass** and record a **Method Attack Transcript**. High-risk method dimensions need live Challenge Questions with user responses or explicit delegation; low-risk dimensions can be marked as cleared from artifacts."

Dev: "Should the Method Decision Log record every turn of the conversation?"

Domain expert: "No. The **Method Decision Log** records only structure-changing decisions: source mode, hybrid merge rationale, method boundary, Mechanistic Claim changes, weakest link, blockers, and status."

Dev: "If the Method Thesis sounds plausible, is the method ready to commit?"

Domain expert: "No. A **Method Thesis** says what the method claims; the **Mechanistic Claim** says why that mechanism should work. Method Commitment must make both explicit before the method can become a **Committed Method Design**."

Dev: "Should Method Commitment write the full experiment plan?"

Domain expert: "No. A **Committed Method Design** should record **Method Commitment Downstream Pressure Points**: required ablations, implied baseline pressures, and metric signals. Full protocols, baseline sets, and metric definitions belong to the later **Experiment Design Workflow**."

Dev: "Can Experiment Design start by finding common benchmarks, baselines, and metrics?"

Domain expert: "No. Use the **Experiment Design Source Gate**, then write a **Claim-Evidence Map** and pass the **Claim-Evidence Review Gate** first. Choose **Evidence Routes**, an **Experiment Stack**, a **Baseline Pressure Matrix**, and a **Claim-Metric Map** only after the claims and reviewer objections are explicit."

Dev: "Can Experiment Design proceed from a rough natural-language method description?"

Domain expert: "Only provisionally. Prefer a **Committed Method Design** and confirm it through an **Experiment Source Decision Packet**. If the Method Thesis, **Mechanistic Claim**, target failure, or intervention point is not stable, route back to **Method Commitment Workflow**."

Dev: "Can the Claim-Evidence Review Gate show the whole map and ask for one approval?"

Domain expert: "No. Use **Claim-Evidence Decision Packets** so each core claim's evidence route, proxy risk, and reviewer objection can be confirmed or revised before dependent benchmark, baseline, metric, and protocol choices begin."

Dev: "If a core claim's evidence route is risky, can the packet still just ask for approval?"

Domain expert: "No. Ask a **High-Risk Claim Challenge** first. The researcher must answer or explicitly delegate the risky claim-to-evidence decision before that route can anchor later protocol, baseline, or metric choices."

Dev: "Can the agent silently finalize the experiment plan after filling the artifacts?"

Domain expert: "No. The **Experiment Design Review Gate** requires the researcher to confirm, revise, or explicitly delegate the claim decomposition, evidence routes, baselines, metrics, ablations, controls, and **Result Interpretation Contract**. This gate is about workflow ownership; it is not the same as a human evaluation or user study."

Dev: "Can the Experiment Design Review Gate wait until all artifacts are drafted and then ask for one approval?"

Domain expert: "No. Use **Experiment Design Review Packets** in dependency order: first the **Experiment Stack**, then task and protocol choices, baseline pressures, metric validity, ablations and controls, and finally the **Result Interpretation Contract**."

Dev: "Can Experiment Design ask for one big approval after drafting everything?"

Domain expert: "No. Use **Stepwise Gate Confirmation**: present one bounded decision packet with a recommended answer, wait for confirmation, revision, or explicit delegation, then continue to dependent choices."

Dev: "If the researcher says 'you decide' at the start, can that approve every later gate?"

Domain expert: "No. Treat delegation as **Gate-Scoped Delegation**. It applies only to the named gate or packet after the researcher has seen the recommendation, and it cannot silently waive a **High-Risk Claim Challenge**."

Dev: "If the researcher asks the agent to run Experiment Design fully automatically, can the result be final?"

Domain expert: "No. A fully automatic run can produce only a **Provisional Experiment Sketch**. The sketch may organize likely choices, but unreviewed choices must not be silently treated as confirmed."

Dev: "Can the workflow draft all experiment files first and fill in gate records afterward?"

Domain expert: "No. Use **Gate-Bound Artifact Drafting**. Drafts can capture proposed decisions, but downstream files cannot look final or drive later choices until the relevant gate status and user decision are recorded."

Dev: "Does `committed` mean the method is already correct?"

Domain expert: "No. **Method Commitment Status** describes structural readiness, not proven correctness. `committed` means downstream-ready; `provisionally-committed` means the design is nearly stable but blocked by named **Method Commitment Blockers** and should not enter downstream workflows yet."

Dev: "Can Method Commitment leave weak points implicit if the final status is provisional?"

Domain expert: "No. The **Method Commitment Gate** requires the weakest link and intentionally unfrozen open decisions to be explicit before any status is assigned. If they block downstream use, record them as **Method Commitment Blockers**."

Dev: "Can the agent mark `committed` if it recommends commitment and the user delegated judgment?"

Domain expert: "No. `committed` requires **Explicit Method Commitment Confirmation** from the researcher. Without it, even a strong method should remain `provisionally-committed` with missing explicit human commitment recorded as a blocker."

Dev: "Should a rejected method still produce `committed_method_design.md` for completeness?"

Domain expert: "No. Write a **Committed Method Design** only for `committed` outcomes. Use a **Provisional Method Design** for `provisionally-committed`, a **Method Redesign Brief** for `needs-redesign`, and a **Method Rejection Note** for `reject-current-method`."

Dev: "Can the final artifact have a generic name regardless of status?"

Domain expert: "No. The **Method Commitment Output Artifact** must match the **Method Commitment Status** so blocked, redesign, and rejection outcomes cannot be mistaken for downstream-ready committed methods."

Dev: "If the status-specific output artifact exists, do we still need a summary?"

Domain expert: "Yes. The **Method Commitment Summary** is always present as the routing index: it names the Source Method, status, output artifact, blockers, next workflow, and do-not-route warnings without replacing the status-specific artifact."

Dev: "Can Research Framing bind the Research Question Card, Committed Method Design, and Experiment Design as three separate sources?"

Domain expert: "No. Select exactly one **Research Framing Source Chain** and use its deepest stable **Research Framing Leaf Source**. If a reviewed Experiment Design exists, enter through that leaf and record a **Source Chain Trace** back to the method and question instead of treating upstream artifacts as coequal sources."

Dev: "Can Research Framing start from a committed method and still produce the final package?"

Domain expert: "Only provisionally. A final **Research Framing Package** normally requires a reviewed Experiment Design or equivalent stable experiment plan. If the leaf source is only a Committed Method Design, Research Question Card, draft, or brief, write a **Provisional Framing Sketch** and mark missing experiment-backed evidence."

Dev: "Should Research Framing write the pitch before checking close work?"

Domain expert: "No. Build and confirm the **Close Work Set** through the **Close Work Selection Gate** first, using **Close Work Threat Roles** rather than a general bibliography. The **One-Sentence Paper Pitch**, **Paper Story Spine**, novelty boundary, and safe claims are finalized later through the **Story And Claim Safety Gate**."

Dev: "Can the framing package say the method improves safety if the experiments are only planned?"

Domain expert: "No. Respect the **Result Claim Boundary**. Without actual results, planned evidence belongs in evaluation-intent wording such as 'we evaluate whether...' rather than outcome-achieved empirical claims."

Dev: "Can a presentation bundle every folder under `workspace/` so the user sees everything in one place?"

Domain expert: "No. A **Workspace Presentation** starts from exactly one source workspace or one coherent source chain. Use the **Presentation Source Gate** to fix the source, slug, output path, update mode, and major modules before generating the presentation."

Dev: "Can the presentation rewrite long process files into a cleaner final artifact?"

Domain expert: "No. Use a **Derived Presentation Layer** with **Presentation Module Summaries** for cumbersome process files, but keep source artifacts as the facts of record. Classify files with the **Presentation Display Map** as **Primary Display Artifacts**, **Summarize-Then-Link Artifacts**, or **Link-Only Artifacts**, and keep source links visible."
