# Symbol Conventions

Use these conventions as defaults, then adapt to the field and manuscript.

## General Principles

- The paper symbol is not a direct translation of the code variable name.
- Preserve traceability through the table, not through long symbols.
- Keep the main symbol short and physically meaningful.
- Use one subscript layer at most.
- Use `\mathrm{...}` for textual parameter subscripts.
- Do not assign symbols to implementation-only variables.

## Common Physical Quantities

| Meaning | Preferred symbol examples |
|---|---|
| Time | `t`, `t_k`, `T` |
| Sample index | `n`, `k` |
| Velocity | `v`, `v^\ast`, `\hat{v}` |
| Displacement | `x`, `u`, `d` |
| Phase | `\varphi`, `\Delta\varphi` |
| Amplitude/envelope | `A`, `a`, `E` |
| Frequency | `f`, `\omega` |
| Signal | `x(n)`, `y(n)` |
| Noise | `\eta`, `\epsilon` |

## Parameters And Thresholds

Use compact bases:

- `T`: time duration, window, delay, period.
- `N`: count, window length, number of samples.
- `\theta`: generic threshold.
- `\lambda`: regularization or weighting parameter.
- `\alpha`, `\beta`, `\gamma`: tunable coefficients.

Examples:

- `CFG.T_hard_limit` -> `T_{\mathrm{hard}}`
- `CFG.xfade_ms` -> `T_{\mathrm{xfade}}`
- `CFG.iSNR_amp_rel_min` -> `\theta_{\mathrm{weak}}`
- `N_win` -> `N_{\mathrm{win}}`

## States And Flags

Prefer a single state variable:

- `s(n) \in \{S_0,S_1,S_2,S_3\}`
- `s_k = S_1`

Boolean flags such as `is_weak`, `is_burst`, and `is_locked` should usually be listed as code variables folded into `s(n)` rather than receiving independent symbols.

## Intermediate Quantities

Default rule: do not expose intermediate variables in the notation table unless they appear in the method equations or represent a named contribution.

If included, mark them as processed versions of a physical quantity:

- `A^{(r)}` for a recovered or refined amplitude version.
- `\Delta\varphi^{(c)}` for a corrected phase difference.
- `\tilde{x}` for a filtered or smoothed signal.

Avoid long forms such as `A_{\mathrm{env},\mathrm{corr}}`.

## Audit Checklist

- No paper symbol is assigned to two unrelated meanings.
- No code variable receives two different paper symbols.
- No symbol uses nested or multiword descriptive subscripts.
- Textual subscripts are upright with `\mathrm{...}`.
- Flags are folded into state notation when possible.
- Omitted intermediate variables are intentionally omitted, not forgotten.
