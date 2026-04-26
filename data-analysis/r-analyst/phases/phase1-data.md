# Phase 1: Data Familiarization

You are executing Phase 1 of a statistical analysis in R. Your goal is to develop deep familiarity with the data before any modeling.

## Why This Phase Matters

Jumping straight to regression is a common mistake. Understanding your data prevents errors, reveals data quality issues, and often suggests refinements to the research design. This phase creates the foundation for credible analysis.

## Technique Guides

**Consult these guides** in `r-statistical-techniques/` for data handling patterns:

| Topic | Guide |
|-------|-------|
| Visualization (ggplot2) | `06_visualization.md` |
| Best practices, Project setup | `07_best_practices.md` |
| Survey data handling | `02_survey_resampling.md` |

## Your Tasks

### 1. Load and Inspect Data Structure

```r
# Load data
data <- read.csv("data/raw/filename.csv")  # or haven::read_dta() for Stata files

# Basic structure
dim(data)
str(data)
names(data)

# Check for duplicates
n_distinct(data$id)  # Should match nrow if id is unique
```

Document:
- Number of observations and variables
- Unit of observation
- Key variable types
- Any obvious data issues

### 2. Generate Descriptive Statistics (Table 1)

Create a summary statistics table for key variables:

```r
library(modelsummary)

# Define variables for Table 1
vars <- c("outcome", "treatment", "control1", "control2")

# Overall summary
datasummary(All(data[, vars]) ~ Mean + SD + Min + Max + N,
            data = data,
            output = "output/tables/table1_descriptives.tex")

# By treatment group (if applicable)
datasummary_balance(~ treatment,
                    data = data,
                    output = "output/tables/table1_balance.tex")
```

### 3. Check Data Quality

**Missing values:**
```r
# Count missing by variable
colSums(is.na(data))

# Missing patterns
library(naniar)
vis_miss(data)

# Document how missing data will be handled
```

**Outliers:**
```r
# Check key continuous variables
summary(data$outcome)
quantile(data$outcome, c(0.01, 0.05, 0.95, 0.99), na.rm = TRUE)

# Visualize distributions
ggplot(data, aes(x = outcome)) +
  geom_histogram(bins = 50) +
  theme_minimal()
```

**Coding issues:**
```r
# Check categorical variables
table(data$treatment, useNA = "ifany")

# Check for impossible values
data %>% filter(age < 0 | age > 120)
```

### 4. Visualize Key Relationships

Create visualizations relevant to the research design:

**For DiD/Panel:**
```r
# Trends over time by treatment group
data %>%
  group_by(time, treatment_group) %>%
  summarise(mean_outcome = mean(outcome, na.rm = TRUE)) %>%
  ggplot(aes(x = time, y = mean_outcome, color = treatment_group)) +
  geom_line() +
  geom_vline(xintercept = treatment_time, linetype = "dashed") +
  theme_minimal()
```

**For RD:**
```r
# Outcome vs. running variable
ggplot(data, aes(x = running_var, y = outcome)) +
  geom_point(alpha = 0.3) +
  geom_smooth(data = filter(data, running_var < cutoff), method = "lm") +
  geom_smooth(data = filter(data, running_var >= cutoff), method = "lm") +
  geom_vline(xintercept = cutoff, linetype = "dashed") +
  theme_minimal()
```

**For any design:**
```r
# Bivariate relationship
ggplot(data, aes(x = treatment, y = outcome)) +
  geom_boxplot() +
  theme_minimal()

# Correlation matrix for controls
library(corrplot)
corrplot(cor(data[, control_vars], use = "complete.obs"))
```

### 5. Verify Design Requirements

Check that data supports the planned identification strategy:

**For DiD:**
- Do you have pre and post periods?
- Do you have treated and control units?
- Are there enough observations in each cell?

**For Panel FE:**
- Is there within-unit variation in key variables?
- How many time periods per unit?

**For IV:**
- Is the instrument observed?
- What's the first-stage relationship look like?

### 6. Create Analysis Sample

Define and document the final analysis sample:

```r
# Define sample restrictions
analysis_data <- data %>%
  filter(
    !is.na(outcome),
    !is.na(treatment),
    year >= 2000 & year <= 2020
  )

# Document sample construction
cat("Original sample:", nrow(data), "\n")
cat("After dropping missing outcome:", nrow(filter(data, !is.na(outcome))), "\n")
cat("Final analysis sample:", nrow(analysis_data), "\n")

# Save analysis sample
saveRDS(analysis_data, "data/clean/analysis_sample.rds")
```

## Output: Data Report

Create a data report (`memos/phase1-data-report.md`) containing:

```markdown
# Data Familiarization Report

## Data Overview
- **Source**: [where data comes from]
- **Observations**: [N]
- **Variables**: [count and key variables]
- **Time Period**: [if applicable]

## Sample Construction
| Step | N | Notes |
|------|---|-------|
| Original sample | X | |
| After restriction 1 | Y | [reason] |
| Final analysis sample | Z | |

## Descriptive Statistics
[Insert or reference Table 1]

## Data Quality Issues
- **Missing data**: [summary and how handled]
- **Outliers**: [any concerns]
- **Coding issues**: [any found and fixed]

## Key Visualizations
[Reference saved figures]

## Design Verification
- [Confirm data supports the identification strategy]
- [Note any concerns]

## Preliminary Observations
- [Anything notable in the descriptives]
- [Any surprises or concerns]

## Questions for User
- [Any decisions that need user input]
```

## When You're Done

Return a summary to the orchestrator that includes:
1. Final sample size and key restrictions
2. Any data quality issues found
3. Whether data supports the planned design
4. Key observations from descriptives
5. Questions for the user

**Do not proceed to Phase 2 until the user reviews the descriptives and confirms the sample.**
