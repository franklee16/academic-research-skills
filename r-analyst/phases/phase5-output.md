# Phase 5: Output & Interpretation

You are executing Phase 5 of a statistical analysis in R. Your goal is to produce publication-ready outputs and synthesize the analysis into a coherent narrative.

## Why This Phase Matters

Analysis isn't complete until it's communicated. This phase transforms results into tables, figures, and text that can appear in a journal article. Good output is accurate, clear, and tells a story.

## Technique Guides

**Consult these guides** in `r-statistical-techniques/` for output code patterns:

| Topic | Guide |
|-------|-------|
| Tables (modelsummary, etable) | `06_visualization.md` |
| Figures (ggplot2, coefplot) | `06_visualization.md` |
| Project structure, Reproducibility | `07_best_practices.md` |
| Marginal effects visualization | `08_nonlinear_models.md` |

## Your Tasks

### 1. Finalize Tables

**Table 1: Descriptive Statistics**
```r
library(modelsummary)

# Summary statistics
datasummary(
  outcome + treatment + control1 + control2 ~
    N + Mean + SD + Min + Max,
  data = analysis_data,
  output = "output/tables/table1_descriptives.tex",
  title = "Summary Statistics",
  notes = "Sample includes [description]. Data from [source]."
)

# Balance table (if applicable)
datasummary_balance(
  ~ treatment,
  data = analysis_data,
  output = "output/tables/table1_balance.tex",
  title = "Balance Across Treatment Groups"
)
```

**Table 2: Main Results**
```r
modelsummary(
  main_models,
  output = "output/tables/table2_main.tex",
  stars = c('*' = 0.1, '**' = 0.05, '***' = 0.01),
  coef_map = c(
    "treatment" = "Treatment",
    "control1" = "Control 1",
    "control2" = "Control 2"
  ),
  gof_map = c("nobs", "r.squared", "FE: unit", "FE: year"),
  title = "Effect of [Treatment] on [Outcome]",
  notes = list(
    "Standard errors clustered at [level] in parentheses.",
    "* p<0.1, ** p<0.05, *** p<0.01"
  )
)
```

**Table 3: Robustness**
```r
modelsummary(
  robustness_models,
  output = "output/tables/table3_robustness.tex",
  stars = c('*' = 0.1, '**' = 0.05, '***' = 0.01),
  coef_omit = "control",  # Show only treatment
  title = "Robustness Checks",
  notes = "See notes to Table 2."
)
```

### 2. Create Publication Figures

**Figure 1: Trends (for DiD)**
```r
library(ggplot2)

trends_data <- analysis_data %>%
  group_by(year, treatment_group) %>%
  summarise(mean_outcome = mean(outcome, na.rm = TRUE),
            se = sd(outcome, na.rm = TRUE) / sqrt(n()))

p_trends <- ggplot(trends_data, aes(x = year, y = mean_outcome,
                                     color = treatment_group,
                                     linetype = treatment_group)) +
  geom_line(size = 1) +
  geom_point(size = 2) +
  geom_ribbon(aes(ymin = mean_outcome - 1.96*se,
                  ymax = mean_outcome + 1.96*se,
                  fill = treatment_group),
              alpha = 0.2, color = NA) +
  geom_vline(xintercept = treatment_year, linetype = "dashed", color = "gray40") +
  annotate("text", x = treatment_year, y = Inf, label = "Treatment",
           vjust = 2, hjust = 0.5, size = 3) +
  scale_color_manual(values = c("Control" = "#1f77b4", "Treated" = "#ff7f0e")) +
  scale_fill_manual(values = c("Control" = "#1f77b4", "Treated" = "#ff7f0e")) +
  labs(x = "Year", y = "Outcome", color = "", fill = "", linetype = "") +
  theme_minimal() +
  theme(legend.position = "bottom",
        panel.grid.minor = element_blank())

ggsave("output/figures/figure1_trends.pdf", p_trends, width = 8, height = 5)
```

**Figure 2: Event Study**
```r
# Using fixest
p_event <- iplot(event_study_model,
                  main = "",
                  xlab = "Time Relative to Treatment",
                  ylab = "Coefficient Estimate")

# Or custom ggplot
event_coefs <- broom::tidy(event_study_model, conf.int = TRUE) %>%
  filter(str_detect(term, "time_to_treat")) %>%
  mutate(time = as.numeric(str_extract(term, "-?\\d+")))

p_event <- ggplot(event_coefs, aes(x = time, y = estimate)) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "gray40") +
  geom_vline(xintercept = -0.5, linetype = "dashed", color = "gray40") +
  geom_pointrange(aes(ymin = conf.low, ymax = conf.high)) +
  labs(x = "Time Relative to Treatment", y = "Coefficient Estimate") +
  theme_minimal()

ggsave("output/figures/figure2_eventstudy.pdf", p_event, width = 8, height = 5)
```

**Figure 3: Coefficient Plot**
```r
p_coef <- modelplot(main_model, coef_omit = "Intercept") +
  geom_vline(xintercept = 0, linetype = "dashed") +
  theme_minimal() +
  labs(title = "")

ggsave("output/figures/figure3_coefplot.pdf", p_coef, width = 6, height = 4)
```

### 3. Write Results Narrative

Draft the key paragraphs for the results section:

**Main effect paragraph:**
> Table 2 presents estimates of the effect of [treatment] on [outcome].
> Column (1) shows the baseline relationship without controls.
> Column (4), our preferred specification, includes [unit] and [time] fixed effects
> and clusters standard errors at the [level] level. We find that [treatment]
> [increases/decreases] [outcome] by [X] [units], significant at the [Y]% level
> (95% CI: [lower, upper]). This represents a [Z]% change relative to the
> pre-treatment mean of [mean].

**Robustness paragraph:**
> Table 3 demonstrates that this finding is robust to alternative specifications.
> The point estimate remains [stable/similar] when we [change 1], [change 2], and
> [change 3]. The effect is [somewhat/not] sensitive to [what]. The sensitivity
> analysis in Figure X shows that an unobserved confounder would need to be
> [X times as strong as the strongest observed predictor] to fully explain
> our findings, suggesting that selection on unobservables is unlikely to
> account for the entire effect.

**Heterogeneity paragraph (if applicable):**
> We examine heterogeneity in treatment effects across [subgroups].
> Table X shows that the effect is [larger/smaller] for [group 1]
> ([estimate]) compared to [group 2] ([estimate]). This difference is
> [statistically significant / not statistically significant] (p = [value]).

### 4. Survey Data Methods Section (If Applicable)

For survey-based analyses, address the five survey methodology deliverables:

**1. Sampling Frame Description:**
```markdown
Data come from the [SURVEY NAME], a [DESIGN TYPE] of [POPULATION].
The sampling frame is [DESCRIPTION]. The target population is [WHO].
[Exclusions]: We exclude [categories] because [reason].
```

**2. Response Rate and Nonresponse:**
```markdown
The response rate was [X]% (calculated as [METHOD: AAPOR RR1/RR3/etc.]).
We compared respondents to [population benchmark / nonrespondents on X variables]
and found [no significant differences / differences on X that we address through Y].
```

**3. Weighting Justification:**
```markdown
We apply [WEIGHT TYPE: post-stratification / raking / none] weights to adjust for
[FACTORS]. Weights are provided by [SOURCE] and calibrated to [BENCHMARKS].
[Alternative: We do not apply weights because {justification}.]
```

**4. Survey Design Acknowledgment:**
```r
library(survey)

# Define survey design
survey_design <- svydesign(
  ids = ~cluster,
  strata = ~stratum,
  weights = ~weight,
  data = analysis_data
)

# All analyses use survey-adjusted estimates
svymean(~outcome, survey_design)
svyglm(outcome ~ treatment + controls, design = survey_design)
```

**5. Population Inference Boundaries:**
```markdown
Our results generalize to [POPULATION] during [TIME PERIOD]. We cannot
speak to [EXCLUDED GROUPS / OTHER TIME PERIODS] because [REASON].
```

### 5. Document Limitations

Identify and articulate limitations honestly:

```markdown
## Limitations

1. **[Identification limitation]**: Our identification strategy relies on
   [assumption]. While we provide evidence supporting this assumption through
   [tests], we cannot definitively rule out [threat].

2. **[External validity]**: Our sample consists of [description]. Results may
   not generalize to [other contexts] because [reason].

3. **[Measurement]**: [Variable] is measured using [method], which may
   [limitation]. We address this by [mitigation] but acknowledge [remaining concern].

4. **[Data limitation]**: We lack data on [variable], which could [potential issue].
   Our robustness checks in Table X suggest this is [unlikely to/may] affect our
   conclusions.
```

### 5. Create Replication Package

Prepare materials for reproducibility:

```r
# Master script header
cat('
# ============================================================
# Replication Code for "[Paper Title]"
# Authors: [Names]
# Date: [Date]
#
# This script reproduces all tables and figures in the paper.
# Runtime: approximately [X] minutes on [hardware]
# ============================================================

# Requirements
# R version: ', R.version.string, '
# Key packages: fixest, modelsummary, ggplot2, dplyr

# Set seed for reproducibility
set.seed(12345)

# Run analysis
source("code/01_clean_data.R")
source("code/02_descriptives.R")
source("code/03_main_analysis.R")
source("code/04_robustness.R")
source("code/05_figures.R")

# Session info
sessionInfo()
', sep = "")
```

## Output: Final Report

Create the final synthesis (`memos/phase5-final-report.md`):

```markdown
# Analysis Summary

## Key Finding
[One sentence summary of the main result]

## Main Result
- **Effect size**: [estimate with CI]
- **Significance**: [p-value or significance level]
- **Interpretation**: [what this means substantively]

## Robustness Assessment
- The finding [is/is not] robust to [list of checks]
- Main concerns: [if any]

## Output Files Created

### Tables
- `table1_descriptives.tex`: Summary statistics
- `table2_main.tex`: Main results
- `table3_robustness.tex`: Robustness checks

### Figures
- `figure1_trends.pdf`: Pre/post trends
- `figure2_eventstudy.pdf`: Event study
- `figure3_coefplot.pdf`: Coefficient plot

### Replication Materials
- `00_master.R`: Master script
- `code/`: All analysis code
- `data/clean/`: Analysis datasets

## Results Narrative
[Draft paragraphs for the paper]

## Limitations
[Honest assessment of limitations]

## Conclusion
[What can and cannot be concluded from this analysis]
```

### 6. Pre-Submission Checklist

Before finalizing, verify the analysis meets publication standards:

**Minimum Standard (Required):**
- [ ] All variables clearly defined with units and coding
- [ ] Sample size and any exclusions documented
- [ ] Main coefficient table includes SEs and significance levels
- [ ] Standard error type specified (robust, clustered at X level, etc.)
- [ ] At least one robustness check reported
- [ ] Limitations section acknowledges main threats to validity

**Strong Standard (Competitive for top journals):**
- [ ] Descriptive statistics table with means, SDs, and sample sizes
- [ ] Multiple robustness specifications in appendix
- [ ] Effect sizes interpreted substantively (not just "significant")
- [ ] For nonlinear models: AMEs or predicted probabilities reported
- [ ] Sensitivity analysis for selection on unobservables (e.g., sensemakr)
- [ ] Missing data approach documented and defended
- [ ] Visualization of key results (event study, coefficient plot, etc.)
- [ ] Replication code and data availability statement

**Exemplary Standard (Model for the field):**
- [ ] Pre-registration referenced (if applicable)
- [ ] Multiple identification strategies compared
- [ ] Heterogeneity analysis with theoretical motivation
- [ ] Mechanism analysis or mediation tests
- [ ] Power analysis or minimum detectable effects
- [ ] Bound analysis for worst-case scenarios
- [ ] Complete replication package with README

**Language Checklist:**
- [ ] Causal language only used with appropriate identification strategy
- [ ] Effect sizes interpreted relative to meaningful benchmarks
- [ ] Confidence intervals reported, not just p-values
- [ ] Scope conditions clearly stated
- [ ] "Significant" refers to statistical significance (or avoid the term)

## When You're Done

Return a summary to the orchestrator that includes:
1. List of all tables and figures created
2. The main finding in one sentence
3. Key limitations
4. Any remaining questions or concerns
5. Confirmation that replication materials are ready
6. Checklist tier achieved (minimum/strong/exemplary)

**The analysis is now complete.** All materials should be ready for paper writing.
