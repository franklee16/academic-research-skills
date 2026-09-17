# Adaptive execution policy

Use this policy to vary procedural freedom without weakening the evidence contract.

## Invariants for every model

- Lock the source by hash, dimensions, page, and original coordinate space.
- Verify the visible chart grammar, plot bounds, axis transform, and at least two anchors per calibrated axis.
- Keep pixel geometry and calibrated values together for every recovered mark.
- Separate visible evidence, model judgement, derived statistics, and source-data validation.
- Preserve ambiguity, occlusion, fusion, and structure-line conflicts; never fill them from an expected count or another data source.
- Produce a CSV, JSON report, and original-canvas overlay or recreation.

These invariants authorize evidence, not a particular implementation.

## Model profiles

Treat a runtime explicitly identified as **GPT-5.6 Sol** or **Terra** as a strong-model profile. Match the runtime-provided model name case-insensitively; do not infer a strong profile from fluent output alone. Treat an unidentified model as the default profile.

- **Strong profile:** use high freedom for chart interpretation, mark association, pixel-centre localisation, conflict classification, and selection among compatible tools.
- **Default profile:** prefer registered deterministic extraction. Use model reasoning to propose configuration and review overlays, but do not let it silently repair numeric output.

Model strength changes the allowed strategy, not the evidence or non-invention requirements.

## Strategy selection

After unified preflight, choose one strategy per visible layer rather than forcing one route over a composite panel:

1. Use `deterministic` when a registered implementation matches the visible grammar and its overlay agrees with the marks.
2. Use `hybrid` when the implementation is compatible but needs model-supplied bounds, colours, exclusions, semantic association, or conflict review.
3. Use `model_assisted` for a strong profile when no compatible implementation exists, a composite layer is unregistered, or a registered candidate is visibly wrong or unstable under reasonable verified bounds.

Preflight incompatibility is enough to select `model_assisted`; do not run a known-incompatible extractor merely to satisfy procedure. One preserved contradictory run is enough to justify fallback; do not sweep parameters toward an expected count.

## Strong-model-assisted output

A strong model may emit candidate pixel centres, endpoints, rectangles, paths, and calibrated values from visible original-pixel evidence. Record:

- `extraction_strategy: model_assisted`;
- `model_profile: strong` and the runtime-provided model name;
- `fallback_reason` or `strategy_reason`;
- source identity, panel/plot bounds, anchors, and transform;
- per-mark pixel geometry, value, status, and concise evidence note;
- unresolved conflicts and excluded quantities;
- an original-canvas overlay;
- references to any deterministic reports used for comparison.

Label the result `model_assisted_candidate`. A deterministic `numeric_output_authorized` flag does not override visual contradiction, and a model-assisted result does not rewrite that flag. Keep both evidence streams immutable.

## Acceptance and refusal

Deliver a model-assisted candidate when every reported value has visible pixel support, verified calibration, and an overlay that agrees with the source. Downgrade individual marks to a review layer when they touch structural geometry or have more than one plausible centre. Return `partial_visible`, `low_confidence`, or `not_extracted` for unresolved quantities.

Never use a strong profile to infer hidden observations, recover an exact sample count from an expected cohort size, assign unprinted error-bar semantics, or recreate author model parameters. Cross-checks such as bar means, visible intervals, printed statistics, or a second extraction method may validate a result but must not be targets for adding or moving marks.
