# Domain Checklist

Apply only the relevant checklist. Do not force every item into the final answer. If the paper belongs to a field not covered below, create a compact checklist from that field's normal evidence standards, measurement assumptions, data risks, and deployment constraints.

## Psychology and Human-Centered Research

- Construct clarity: distinguish constructs, behaviors, states, traits, affect, style, and proxy signals where relevant.
- Measurement source: self-report scale, observer rating, behavioral annotation, clinical label, or model-inferred label.
- Reliability: internal consistency, inter-rater agreement, test-retest reliability, or missing reliability evidence.
- Validity: construct, convergent, discriminant, criterion, ecological, and cross-cultural validity.
- Dataset population: demographics, language, platform, recruitment, sample size, exclusion criteria.
- Temporal design: whether time-varying constructs are measured longitudinally or inferred from static observations.
- Stability leakage: whether temporary states are treated as stable attributes or stable attributes are inferred from short-term behavior.
- Proxy risk: whether the model predicts linguistic style, topic, platform behavior, or demographic artifacts rather than the intended construct.
- Ethics and privacy: sensitive inference, consent, anonymization, potential harm, and deployment limits.
- Generalization: cross-domain, cross-language, cross-population, and cross-time validation.

## NLP and Large Language Models

- Task formulation: classification, generation, retrieval, ranking, evaluation, or agent workflow.
- Data contamination: overlap with pretraining data, benchmark leakage, prompt leakage.
- Baselines: strong non-LLM baseline, fine-tuned baseline, retrieval baseline, prompting baseline.
- Evaluation: automatic metrics, human evaluation, calibration, robustness, significance testing.
- Prompt sensitivity: prompt variants, decoding settings, seed sensitivity.
- Model access: open weights, API-only, version/date stability, reproducibility limits.
- Cost: token budget, latency, GPU memory, training/inference cost.
- Safety: privacy, bias, harmful inference, high-stakes claims.

## Machine Learning Experiments

- Baseline fairness: same data, budget, preprocessing, and tuning effort.
- Ablation value: each ablation should answer a hypothesis or support a decision.
- Statistical rigor: variance, seeds, confidence intervals, significance tests where appropriate.
- Data splits: leakage, distribution shift, public/private split mismatch.
- Error analysis: per-class, per-domain, hard cases, qualitative examples.
- Compute disclosure: hardware, training time, parameter count, inference cost.
- Negative results: whether failed assumptions are reported or hidden.

## Human-Subjects and Social Computing

- Consent and participant risk.
- Sensitive attribute inference.
- De-identification and data retention.
- Cultural and language representativeness.
- Potential downstream misuse.
- Whether deployment claims exceed the study setting.
