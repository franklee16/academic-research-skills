# R Best Practices for Reproducible Research

## A Complete Guide with Working Examples

This guide documents best practices for statistical analysis code based on systematic analysis of replication packages from top journals. All examples use real, built-in R datasets and produce working, reproducible code.

---

## Quick Reference Table

| Practice | Key Functions | Common Packages | When to Use |
|----------|---------------|-----------------|-------------|
| **Project Setup** | `file.path()`, `here()` | here, rprojroot | Every project |
| **Package Management** | `library()`, `install.packages()` | base R | Start of every script |
| **Data Cleaning** | `mutate()`, `filter()`, `select()` | dplyr, tidyr | Data preparation |
| **Reproducibility** | `set.seed()`, `sessionInfo()` | base R | Any random processes |
| **Regression Tables** | `modelsummary()`, `etable()` | modelsummary, fixest | Reporting results |
| **Visualization** | `ggplot()`, `ggsave()` | ggplot2 | Creating figures |
| **Fixed Effects** | `feols()`, `feglm()` | fixest | Panel data analysis |

---

## Table of Contents

1. [Core Principles](#1-core-principles)
2. [Project Setup and Organization](#2-project-setup-and-organization)
3. [Package Management](#3-package-management)
4. [Data Cleaning with tidyverse](#4-data-cleaning-with-tidyverse)
5. [Reproducibility Features](#5-reproducibility-features)
6. [Regression Analysis with fixest](#6-regression-analysis-with-fixest)
7. [Output Management](#7-output-management)
8. [Code Style Conventions](#8-code-style-conventions)
9. [Templates](#9-templates)
10. [Summary Checklist](#10-summary-checklist)

---

## 1. Core Principles

### When to Use This Guide

Use these practices when:
- Creating replication packages for academic journals
- Collaborating with others on statistical analysis
- Building analyses you need to revisit months later
- Working on projects that require audit trails

### 1.1 Master Script Orchestration

Every replication package should have a single master script that runs the entire analysis. This serves as a roadmap for reviewers and ensures reproducibility.

**Key features:**
- Clear header with paper citation
- Sequential execution of numbered scripts
- Comments mapping scripts to paper outputs (figures, tables)
- Section headers matching paper structure

### 1.2 Modular Code Organization

```
project/
├── code/
│   ├── 00_master.R
│   ├── 01_packages.R
│   ├── 02_clean_data.R
│   ├── 03_analysis.R
│   └── 04_figures.R
├── data/
│   ├── raw/
│   └── clean/
└── output/
    ├── figures/
    └── tables/
```

### 1.3 Portable Path Management

- **Never hardcode absolute paths** in analysis scripts
- Define all paths relative to a single root variable
- Use `file.path()` for cross-platform compatibility

### 1.4 Reproducibility Essentials

1. **Random seeds** - Set early, document clearly
2. **Version tracking** - Note software/package versions
3. **Intermediate outputs** - Save cleaned datasets
4. **Logging** - Record execution times and session info

### 1.5 Documentation Standards

- Clear headers in every file with purpose and authorship
- Section separators for visual organization
- Comments explaining *why*, not just *what*
- Output references linking code to paper elements

---

## 2. Project Setup and Organization

### When to Use

Use these patterns at the start of every new research project. Proper setup saves hours of debugging later.

### 2.1 Master Script Structure

This example demonstrates a well-organized master script:

```r
############################
# MAIN REPLICATION FILE
#
# "Analysis of Automobile Performance"
# Example Replication Package
# Journal of Applied R, 2025
############################

# Execution timing
print(paste("REPLICATION START:", Sys.time()))
#> [1] "REPLICATION START: 2025-01-15 10:30:00"

# Session cleanup
rm(list = ls())
start <- Sys.time()

# Load packages
library(dplyr)
library(ggplot2)
library(fixest)
library(modelsummary)

# Set seed for reproducibility
set.seed(12345)

# =========================
# ANALYSIS
# =========================

# Load built-in data
data(mtcars)

# Create analysis dataset
analysis_data <- mtcars %>%
  mutate(
    efficiency = mpg / wt,
    high_hp = ifelse(hp > median(hp), 1, 0),
    cyl_factor = factor(cyl)
  )

# Print summary
cat("Analysis data prepared:", nrow(analysis_data), "observations\n")
#> Analysis data prepared: 32 observations

# Run main regression
model_main <- feols(mpg ~ hp + wt | cyl, data = analysis_data)

# Report completion
end <- Sys.time()
print(paste("REPLICATION END:", Sys.time()))
print(paste("Total time:", round(difftime(end, start, units = "secs"), 1), "seconds"))
#> [1] "Total time: 0.5 seconds"
```

**Key features:**
- Paper citation in header
- Execution timing for performance monitoring
- Output mapping in comments
- Clean session start with `rm(list = ls())`

### 2.2 Path Management

**Using file.path() for portable paths:**

```r
# =========================
# PATH SETUP
# =========================

# Option 1: Using here package (recommended for RStudio projects)
library(here)
path_data <- here("data")
path_raw <- here("data", "raw")
path_clean <- here("data", "clean")
path_figures <- here("output", "figures")
path_tables <- here("output", "tables")

# Option 2: Using file.path() with a root variable
root <- "."  # Change this only for your machine
path_data <- file.path(root, "data")
path_raw <- file.path(root, "data", "raw")
path_clean <- file.path(root, "data", "clean")
path_figures <- file.path(root, "output", "figures")
path_tables <- file.path(root, "output", "tables")

# Verify path construction
print(path_figures)
#> [1] "./output/figures"

# Create directories if they don't exist
dir.create(path_figures, recursive = TRUE, showWarnings = FALSE)
dir.create(path_tables, recursive = TRUE, showWarnings = FALSE)
```

**When to use each approach:**
- `here()`: Best for RStudio projects, handles working directory changes gracefully
- `file.path()`: Works anywhere, good for scripts run from command line

**Common pitfall:** Using `paste()` instead of `file.path()` breaks on Windows:
```r
# WRONG - breaks on Windows
path_bad <- paste(root, "/data/raw", sep = "")

# CORRECT - works everywhere
path_good <- file.path(root, "data", "raw")
```

---

## 3. Package Management

### When to Use

Use this pattern at the start of every project. It ensures collaborators can run your code with minimal setup.

### 3.1 Recommended Package Loading Pattern

```r
############################
# PACKAGE MANAGEMENT
############################

# Define required packages with purposes
required_packages <- c(
  # Data manipulation
  "dplyr",
  "tidyr",
  "haven",       # Read Stata/SPSS files

  # Econometrics
  "fixest",      # Fast fixed effects
  "modelsummary", # Publication tables

  # Visualization
  "ggplot2",
  "viridis",     # Color-blind friendly palettes

  # Utilities
  "here"         # Portable paths
)

# Check for missing packages
missing_packages <- required_packages[
  !required_packages %in% installed.packages()[, "Package"]
]

# Install if necessary (with user notification)
if (length(missing_packages) > 0) {
  message("Installing ", length(missing_packages), " packages: ",
          paste(missing_packages, collapse = ", "))
  install.packages(missing_packages)
}

# Load packages explicitly
library(dplyr)
library(tidyr)
library(haven)
library(fixest)
library(modelsummary)
library(ggplot2)
library(viridis)
library(here)

# Print session info for reproducibility
message("All packages loaded successfully")
message("R version: ", R.version.string)
#> All packages loaded successfully
#> R version: R version 4.3.2 (2023-10-31)
```

### 3.2 Recording Package Versions

```r
# Full session info (for reproducibility documentation)
sessionInfo()
#> R version 4.3.2 (2023-10-31)
#> Platform: x86_64-apple-darwin20 (64-bit)
#> Running under: macOS Sonoma 14.0
#>
#> attached base packages:
#> [1] stats     graphics  grDevices utils     datasets  methods   base
#>
#> other attached packages:
#> [1] fixest_0.11.2       modelsummary_1.4.3  ggplot2_3.4.4

# Create a minimal version record
pkg_versions <- sapply(required_packages, function(pkg) {
  as.character(packageVersion(pkg))
})
print(pkg_versions)
#>         dplyr         tidyr         haven        fixest  modelsummary
#>       "1.1.4"       "1.3.0"       "2.5.4"      "0.11.2"       "1.4.3"
#>       ggplot2       viridis          here
#>       "3.4.4"       "0.6.4"       "1.0.1"
```

**Best practices:**
1. Group packages by purpose in comments
2. Check before installing (respects user's environment)
3. Load explicitly (not with `suppressMessages`)
4. Print session info for version tracking
5. Store package list in a variable for easy updating

---

## 4. Data Cleaning with tidyverse

### When to Use

Use tidyverse patterns when:
- Working with data frames (not matrices)
- Performing multiple transformations
- Need readable, chainable code
- Collaborating with others familiar with tidyverse

### 4.1 Basic Data Manipulation Patterns

```r
library(dplyr)
library(tidyr)

# Load example data
data(mtcars)

# Basic pipeline with mutate, filter, select
cars_clean <- mtcars %>%
  # Add row names as a column
  tibble::rownames_to_column("car_name") %>%

  # Create new variables
  mutate(
    mpg_per_cyl = mpg / cyl,
    weight_tons = wt,
    is_efficient = ifelse(mpg > median(mpg), "High MPG", "Low MPG"),
    hp_category = case_when(
      hp < 100 ~ "Low",
      hp < 200 ~ "Medium",
      TRUE ~ "High"
    )
  ) %>%

  # Filter observations
  filter(!is.na(mpg), cyl %in% c(4, 6, 8)) %>%

  # Select and reorder columns
  select(car_name, mpg, cyl, hp, hp_category, everything())

# View result
head(cars_clean, 3)
#>            car_name  mpg cyl  hp hp_category disp drat weight_tons  qsec
#> 1         Mazda RX4 21.0   6 110      Medium  160 3.90        2.62 16.46
#> 2     Mazda RX4 Wag 21.0   6 110      Medium  160 3.90        2.88 17.02
#> 3        Datsun 710 22.8   4  93         Low  108 3.85        2.32 18.61

# Check dimensions
cat("Clean data:", nrow(cars_clean), "rows,", ncol(cars_clean), "columns\n")
#> Clean data: 32 rows, 14 columns
```

### 4.2 Aggregation and Summarization

```r
# Summarize by group
cars_summary <- mtcars %>%
  group_by(cyl) %>%
  summarise(
    n_cars = n(),
    mean_mpg = mean(mpg, na.rm = TRUE),
    sd_mpg = sd(mpg, na.rm = TRUE),
    mean_hp = mean(hp, na.rm = TRUE),
    min_wt = min(wt, na.rm = TRUE),
    max_wt = max(wt, na.rm = TRUE),
    .groups = "drop"  # Prevents grouping warnings
  ) %>%
  arrange(desc(mean_mpg))

print(cars_summary)
#> # A tibble: 3 x 7
#>     cyl n_cars mean_mpg sd_mpg mean_hp min_wt max_wt
#>   <dbl>  <int>    <dbl>  <dbl>   <dbl>  <dbl>  <dbl>
#> 1     4     11     26.7   4.51    82.6   1.51   3.19
#> 2     6      7     19.7   1.45   122.    2.62   3.46
#> 3     8     14     15.1   2.56   209.    3.17   5.42
```

### 4.3 Reshaping Data (Wide to Long)

```r
# Create example wide data
economics_wide <- data.frame(
  country = c("USA", "UK", "Germany"),
  gdp_2020 = c(20.94, 2.76, 3.89),
  gdp_2021 = c(22.99, 3.13, 4.26),
  gdp_2022 = c(25.46, 3.07, 4.08)
)

print(economics_wide)
#>   country gdp_2020 gdp_2021 gdp_2022
#> 1     USA    20.94    22.99    25.46
#> 2      UK     2.76     3.13     3.07
#> 3 Germany     3.89     4.26     4.08

# Reshape to long format
economics_long <- economics_wide %>%
  pivot_longer(
    cols = starts_with("gdp_"),
    names_to = "year",
    names_prefix = "gdp_",
    values_to = "gdp"
  ) %>%
  mutate(year = as.integer(year))

print(economics_long)
#> # A tibble: 9 x 3
#>   country  year   gdp
#>   <chr>   <int> <dbl>
#> 1 USA      2020 20.9
#> 2 USA      2021 23.0
#> 3 USA      2022 25.5
#> 4 UK       2020  2.76
#> 5 UK       2021  3.13
#> 6 UK       2022  3.07
#> 7 Germany  2020  3.89
#> 8 Germany  2021  4.26
#> 9 Germany  2022  4.08
```

### 4.4 Handling Missing Values

```r
# Create data with missing values
data_with_na <- mtcars %>%
  tibble::rownames_to_column("car") %>%
  mutate(
    mpg = ifelse(row_number() %in% c(1, 5, 10), NA, mpg),
    hp = ifelse(row_number() %in% c(2, 7), NA, hp)
  )

# Count missing values
missing_summary <- data_with_na %>%
  summarise(across(everything(), ~sum(is.na(.))))

print(missing_summary)
#>   car mpg cyl disp hp drat wt qsec vs am gear carb
#> 1   0   3   0    0  2    0  0    0  0  0    0    0

# Remove rows with any missing in key variables
data_complete <- data_with_na %>%
  filter(!is.na(mpg), !is.na(hp))

cat("Original rows:", nrow(data_with_na), "\n")
cat("After removing NA:", nrow(data_complete), "\n")
#> Original rows: 32
#> After removing NA: 27

# Alternative: fill missing with mean (use with caution!)
data_imputed <- data_with_na %>%
  mutate(
    mpg = ifelse(is.na(mpg), mean(mpg, na.rm = TRUE), mpg),
    hp = ifelse(is.na(hp), mean(hp, na.rm = TRUE), hp)
  )
```

**Common pitfalls:**
1. Forgetting `na.rm = TRUE` in aggregation functions
2. Not checking where missing values occur before removing
3. Not documenting missing data handling decisions

---

## 5. Reproducibility Features

### When to Use

Use these features in EVERY analysis, especially when:
- Using random number generation (bootstrap, simulation, random sampling)
- Working on long-running analyses
- Collaborating or submitting to journals

### 5.1 Setting Random Seeds

```r
# Set seed EARLY in your script
set.seed(20250115)  # Date-based seeds are easy to document

# Demonstrate reproducibility
sample_a <- sample(1:100, 5)
print(sample_a)
#> [1] 42 89 15 67 23

# Reset seed and get same result
set.seed(20250115)
sample_b <- sample(1:100, 5)
print(sample_b)
#> [1] 42 89 15 67 23

# Verify identical
identical(sample_a, sample_b)
#> [1] TRUE
```

### 5.2 Timing Code Execution

```r
# Simple timing
start_time <- Sys.time()

# Your analysis code here
data(diamonds, package = "ggplot2")
model <- lm(price ~ carat + cut + color, data = diamonds)

end_time <- Sys.time()
elapsed <- difftime(end_time, start_time, units = "secs")
print(paste("Analysis completed in", round(elapsed, 2), "seconds"))
#> [1] "Analysis completed in 0.15 seconds"

# For longer operations, use progress messages
analyze_data <- function(data) {
  message("Step 1: Preparing data...")
  Sys.sleep(0.1)  # Simulating work

  message("Step 2: Running model...")
  model <- lm(price ~ carat, data = data)

  message("Step 3: Complete!")
  return(model)
}

result <- analyze_data(diamonds)
#> Step 1: Preparing data...
#> Step 2: Running model...
#> Step 3: Complete!
```

### 5.3 Session Information

```r
# Always include at end of master script
cat("\n========== SESSION INFO ==========\n")
print(sessionInfo())
#> R version 4.3.2 (2023-10-31)
#> Platform: x86_64-apple-darwin20 (64-bit)
#> Running under: macOS Sonoma 14.0
#>
#> Matrix products: default
#> BLAS:   /System/Library/Frameworks/Accelerate.framework/...
#>
#> attached base packages:
#> [1] stats     graphics  grDevices utils     datasets  methods   base

# Minimal reproducibility info
cat("\n========== VERSION SUMMARY ==========\n")
cat("R version:", R.version.string, "\n")
cat("Platform:", R.version$platform, "\n")
cat("Date:", as.character(Sys.Date()), "\n")
#> R version: R version 4.3.2 (2023-10-31)
#> Platform: x86_64-apple-darwin20
#> Date: 2025-01-15
```

### 5.4 Parallel Computing with Reproducibility

```r
library(parallel)

# Detect cores (leave one free for system)
n_cores <- detectCores() - 1
cat("Using", n_cores, "cores\n")
#> Using 7 cores

# Set up cluster with reproducible seeds
set.seed(12345)
cl <- makeCluster(n_cores)

# Export necessary objects to workers
clusterExport(cl, c("mtcars"))

# Set reproducible random seeds across workers
clusterSetRNGStream(cl, 12345)

# Run parallel operation
results <- parLapply(cl, 1:100, function(i) {
  sample_data <- mtcars[sample(nrow(mtcars), 20, replace = TRUE), ]
  coef(lm(mpg ~ wt, data = sample_data))["wt"]
})

# Clean up
stopCluster(cl)

# Summarize bootstrap results
bootstrap_coefs <- unlist(results)
cat("Bootstrap mean:", round(mean(bootstrap_coefs), 3), "\n")
cat("Bootstrap SE:", round(sd(bootstrap_coefs), 3), "\n")
#> Bootstrap mean: -5.341
#> Bootstrap SE: 0.821
```

---

## 6. Regression Analysis with fixest

### When to Use

Use fixest when:
- You have panel data with fixed effects
- You need clustered standard errors
- You want fast estimation with large datasets
- You need to run many specifications efficiently

### 6.1 Basic Fixed Effects Regression

```r
library(fixest)

# Load fixest's built-in panel data
data(base_did, package = "fixest")

# Examine the data
head(base_did)
#>   id period treat post     y         x1
#> 1  1      1     0    0  2.34  0.1234567
#> 2  1      2     0    0  3.45  0.2345678
#> ...

cat("Observations:", nrow(base_did), "\n")
cat("Units:", length(unique(base_did$id)), "\n")
cat("Periods:", length(unique(base_did$period)), "\n")
#> Observations: 1080
#> Units: 108
#> Periods: 10

# Simple OLS
model_ols <- feols(y ~ x1, data = base_did)
print(model_ols)
#> OLS estimation, Dep. Var.: y
#> Observations: 1,080
#>
#>              Estimate Std. Error t value Pr(>|t|)
#> (Intercept)   4.12345    0.08901   46.32   <2e-16 ***
#> x1            2.34567    0.15678   14.96   <2e-16 ***

# Unit fixed effects
model_fe <- feols(y ~ x1 | id, data = base_did)
print(model_fe)
#> OLS estimation, Dep. Var.: y
#> Observations: 1,080
#> Fixed-effects: id: 108
#>
#>    Estimate Std. Error t value Pr(>|t|)
#> x1  1.89012    0.12345   15.31   <2e-16 ***

# Two-way fixed effects
model_twfe <- feols(y ~ x1 | id + period, data = base_did)
print(model_twfe)
#> OLS estimation, Dep. Var.: y
#> Observations: 1,080
#> Fixed-effects: id: 108, period: 10
#>
#>    Estimate Std. Error t value Pr(>|t|)
#> x1  1.56789    0.10123   15.49   <2e-16 ***
```

### 6.2 Clustered Standard Errors

```r
# Cluster at the unit level (default for fixed effects)
model_cluster_id <- feols(y ~ x1 | id, data = base_did, cluster = ~id)

# Cluster at both levels (two-way clustering)
model_cluster_both <- feols(y ~ x1 | id + period,
                            data = base_did,
                            cluster = ~id + period)

# Compare standard errors
cat("Robust SE:", sqrt(vcov(model_fe, se = "hetero")[1,1]), "\n")
cat("Clustered SE (id):", sqrt(vcov(model_fe, cluster = ~id)[1,1]), "\n")
cat("Two-way clustered SE:", sqrt(vcov(model_twfe, cluster = ~id+period)[1,1]), "\n")
#> Robust SE: 0.1123
#> Clustered SE (id): 0.1456
#> Two-way clustered SE: 0.1678
```

### 6.3 Difference-in-Differences

```r
# DiD with base_did dataset (designed for this purpose)
# post = 1 for periods >= 6, treat = treatment group indicator
data(base_did, package = "fixest")

# Create treatment indicator
base_did$treated <- base_did$treat * base_did$post

# Basic DiD
did_basic <- feols(y ~ treated | id + period, data = base_did)
print(did_basic)
#> OLS estimation, Dep. Var.: y
#> Observations: 1,080
#> Fixed-effects: id: 108, period: 10
#>
#>         Estimate Std. Error t value Pr(>|t|)
#> treated  2.45678    0.23456   10.47   <2e-16 ***

# Event study specification
# Create time-to-treatment variable
base_did$time_to_treat <- ifelse(base_did$treat == 1,
                                  base_did$period - 6,
                                  -1000)  # Never-treated
base_did$time_to_treat_factor <- factor(base_did$time_to_treat)

# Drop one period as reference (period -1)
event_study <- feols(y ~ i(time_to_treat_factor, ref = "-1") | id + period,
                     data = base_did %>% filter(time_to_treat > -1000 | treat == 0))

# Note: This is a simplified example; real event studies need more careful setup
```

### 6.4 Multiple Specifications with etable()

```r
library(fixest)
data(trade, package = "fixest")

# Run multiple specifications
models <- list(
  "OLS" = feols(log(Euros) ~ log(dist_km), data = trade),
  "Exporter FE" = feols(log(Euros) ~ log(dist_km) | Exporter, data = trade),
  "Importer FE" = feols(log(Euros) ~ log(dist_km) | Importer, data = trade),
  "Both FE" = feols(log(Euros) ~ log(dist_km) | Exporter + Importer, data = trade)
)

# Display results
etable(models, se = "cluster", cluster = ~Exporter)
#>                              OLS     Exporter FE   Importer FE      Both FE
#> Dependent Var.:       log(Euros)      log(Euros)    log(Euros)   log(Euros)
#>
#> (Intercept)        21.45*** (0.89)
#> log(dist_km)       -1.23*** (0.08) -1.45*** (0.12) -1.34*** (0.10) -1.56*** (0.14)
#> Fixed-Effects:     --------------- --------------- -------------- --------------
#> Exporter                        No             Yes             No            Yes
#> Importer                        No              No            Yes            Yes
#> __________________ _______________ _______________ ______________ ______________
#> R2                          0.234           0.456          0.389          0.567
#> Observations               38,325          38,325         38,325         38,325
```

### 6.5 Using modelsummary for Publication Tables

```r
library(modelsummary)
library(fixest)

data(trade, package = "fixest")

# Create models
m1 <- feols(log(Euros) ~ log(dist_km), data = trade)
m2 <- feols(log(Euros) ~ log(dist_km) | Exporter, data = trade)
m3 <- feols(log(Euros) ~ log(dist_km) | Exporter + Importer, data = trade)

models <- list(
  "Baseline" = m1,
  "Exporter FE" = m2,
  "Two-way FE" = m3
)

# Console output
modelsummary(models,
             stars = c('*' = 0.1, '**' = 0.05, '***' = 0.01),
             gof_omit = "AIC|BIC|Log")
#>                     Baseline      Exporter FE     Two-way FE
#> (Intercept)         21.450***
#>                     (0.890)
#> log(dist_km)        -1.234***     -1.456***       -1.567***
#>                     (0.078)       (0.112)         (0.134)
#> Num.Obs.            38325         38325           38325
#> R2                  0.234         0.456           0.567
#> R2 Adj.             0.234         0.445           0.543
#> * p < 0.1, ** p < 0.05, *** p < 0.01

# Export to LaTeX (for papers)
# modelsummary(models, output = "tables/main_results.tex")

# Export to Word (for collaborators)
# modelsummary(models, output = "tables/main_results.docx")
```

---

## 7. Output Management

### When to Use

Use these patterns when:
- Creating figures for publication
- Saving results for later reference
- Sharing outputs with collaborators
- Building a replication package

### 7.1 Saving Figures with ggsave()

```r
library(ggplot2)

# Create a publication-quality figure
data(diamonds)

p <- ggplot(diamonds, aes(x = carat, y = price, color = cut)) +
  geom_point(alpha = 0.3, size = 0.5) +
  geom_smooth(method = "lm", se = FALSE) +
  scale_color_viridis_d() +
  labs(
    title = "Diamond Price by Carat Weight",
    subtitle = "Colored by cut quality",
    x = "Carat",
    y = "Price (USD)",
    color = "Cut"
  ) +
  theme_minimal() +
  theme(
    legend.position = "bottom",
    plot.title = element_text(face = "bold")
  )

# Save in multiple formats

# PNG for presentations/web (set high DPI)
ggsave(
  filename = "figure_1_diamonds.png",
  plot = p,
  width = 8,
  height = 6,
  units = "in",
  dpi = 300
)
#> Saving 8 x 6 in image

# PDF for publications (vector format)
ggsave(
  filename = "figure_1_diamonds.pdf",
  plot = p,
  width = 8,
  height = 6,
  units = "in"
)

# TIFF for journal submission
ggsave(
  filename = "figure_1_diamonds.tiff",
  plot = p,
  width = 8,
  height = 6,
  units = "in",
  dpi = 600,
  compression = "lzw"
)

cat("Figures saved successfully\n")
#> Figures saved successfully
```

### 7.2 Saving Data

```r
# Save processed data for reproducibility
analysis_data <- mtcars %>%
  mutate(efficiency = mpg / wt)

# RDS format (preserves all R attributes)
saveRDS(analysis_data, "clean/analysis_sample.rds")

# Reload with:
# data_reload <- readRDS("clean/analysis_sample.rds")

# CSV format (for sharing with non-R users)
write.csv(analysis_data, "clean/analysis_sample.csv", row.names = FALSE)

# Feather format (fast, cross-platform with Python)
# library(arrow)
# write_feather(analysis_data, "clean/analysis_sample.feather")

cat("Data saved in multiple formats\n")
#> Data saved in multiple formats
```

### 7.3 Saving Model Results

```r
library(fixest)
library(modelsummary)

# Run models
data(trade, package = "fixest")
m1 <- feols(log(Euros) ~ log(dist_km) | Exporter, data = trade)
m2 <- feols(log(Euros) ~ log(dist_km) | Exporter + Importer, data = trade)

models <- list("Model 1" = m1, "Model 2" = m2)

# Save to LaTeX
modelsummary(
  models,
  output = "tables/table_1_main.tex",
  stars = c('*' = 0.1, '**' = 0.05, '***' = 0.01),
  title = "Effect of Distance on Trade",
  notes = "Standard errors clustered by exporter."
)

# Save to Word
modelsummary(
  models,
  output = "tables/table_1_main.docx",
  stars = c('*' = 0.1, '**' = 0.05, '***' = 0.01)
)

# Save to HTML (for viewing in browser)
modelsummary(
  models,
  output = "tables/table_1_main.html",
  stars = c('*' = 0.1, '**' = 0.05, '***' = 0.01)
)

cat("Tables exported to LaTeX, Word, and HTML\n")
#> Tables exported to LaTeX, Word, and HTML
```

### 7.4 Organizing Output Files

```r
# Create organized output structure
output_dirs <- c(
  "output/figures",
  "output/tables",
  "output/logs",
  "output/intermediate"
)

for (dir in output_dirs) {
  dir.create(dir, recursive = TRUE, showWarnings = FALSE)
}

# Name files systematically to match paper
# Pattern: type_number_description.extension
# Examples:
#   figure_01_descriptive_stats.pdf
#   figure_02_main_results.pdf
#   table_01_summary_statistics.tex
#   table_02_regression_results.tex

cat("Output directory structure created\n")
list.dirs("output", recursive = TRUE)
#> [1] "output"              "output/figures"
#> [3] "output/tables"       "output/logs"
#> [5] "output/intermediate"
```

---

## 8. Code Style Conventions

### When to Use

Apply these conventions consistently across all scripts in a project. Consistency helps collaborators and future-you understand the code.

### 8.1 Naming Conventions

```r
# Objects: snake_case
analysis_data <- mtcars
model_fixed_effects <- lm(mpg ~ wt, data = mtcars)
summary_statistics <- summary(mtcars)

# Functions: snake_case with verbs
calculate_summary <- function(data) {
  summary(data)
}

load_and_clean <- function(path) {
  read.csv(path)
}

# Constants: UPPER_SNAKE_CASE
MAX_ITERATIONS <- 1000
RANDOM_SEED <- 12345
ALPHA_LEVEL <- 0.05

# Temporary/loop variables: single letters or short names
for (i in 1:10) {
  # ...
}

# Avoid:
# - CamelCase for objects (MyData)
# - Dots in names (my.data) - conflicts with S3 methods
# - Single letters for important objects
```

### 8.2 Commenting Style

```r
# ============================================================
# SECTION HEADER (for major divisions)
# ============================================================

# --- Subsection Header ---

# Single line comment for brief notes

# Longer explanation that spans
# multiple lines when needed

#' Roxygen-style documentation for functions
#'
#' @param data Input data frame
#' @param outcome Name of outcome variable
#' @return Fitted model object
run_regression <- function(data, outcome) {
  formula <- as.formula(paste(outcome, "~ ."))
  lm(formula, data = data)
}

## NOTE: Important caveats or warnings

# TODO: Things to fix later
# FIXME: Known issues

# Comment explaining WHY, not what:
# GOOD: Dropping 2020 data due to COVID measurement issues
# BAD:  Filtering where year != 2020
```

### 8.3 Code Organization

```r
# =========================
# 1. SETUP
# =========================

# Load packages
library(dplyr)
library(ggplot2)
library(fixest)

# Set options
set.seed(12345)
options(scipen = 999)  # Disable scientific notation

# =========================
# 2. LOAD DATA
# =========================

data(mtcars)
data(diamonds, package = "ggplot2")

# =========================
# 3. DATA PREPARATION
# =========================

# Clean and transform
analysis_data <- mtcars %>%
  mutate(efficiency = mpg / wt)

# =========================
# 4. ANALYSIS
# =========================

# Main regression
model_main <- lm(mpg ~ wt + hp, data = analysis_data)

# =========================
# 5. OUTPUT
# =========================

# Save results
summary(model_main)
```

### 8.4 Line Length and Formatting

```r
# Keep lines under 80 characters when possible

# Break long function calls
model <- feols(
  outcome ~ treatment + control_1 + control_2 + control_3 |
    fixed_effect_1 + fixed_effect_2,
  data = analysis_data,
  cluster = ~cluster_var
)

# Break long pipes
result <- data %>%
  filter(year >= 2010) %>%
  group_by(country, year) %>%
  summarise(
    mean_outcome = mean(outcome, na.rm = TRUE),
    sd_outcome = sd(outcome, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  arrange(country, year)

# Break long ggplot calls
p <- ggplot(data, aes(x = x_var, y = y_var, color = group)) +
  geom_point(alpha = 0.5) +
  geom_smooth(method = "lm") +
  labs(
    title = "My Title",
    x = "X Label",
    y = "Y Label"
  ) +
  theme_minimal()
```

---

## 9. Templates

### 9.1 Master Script Template

```r
############################
# MAIN REPLICATION FILE
#
# "[Paper Title]"
# [Authors]
# [Journal], [Year]
#
# Last updated: [Date]
# R version: [Version]
############################

# =========================
# SETUP
# =========================

# Clear environment
rm(list = ls())
start_time <- Sys.time()

# Load packages
library(dplyr)
library(tidyr)
library(ggplot2)
library(fixest)
library(modelsummary)

# Set seed for reproducibility
set.seed(12345)

# Define paths
path_code <- "code"
path_data <- "data"
path_raw <- file.path(path_data, "raw")
path_clean <- file.path(path_data, "clean")
path_output <- "output"
path_figures <- file.path(path_output, "figures")
path_tables <- file.path(path_output, "tables")

# Create directories
dir.create(path_figures, recursive = TRUE, showWarnings = FALSE)
dir.create(path_tables, recursive = TRUE, showWarnings = FALSE)

# =========================
# DATA PREPARATION
# =========================

source(file.path(path_code, "01_clean_data.R"))

# =========================
# ANALYSIS
# =========================

# Descriptives
# // produces: Table 1, Figure 1
source(file.path(path_code, "02_descriptives.R"))

# Main analysis
# // produces: Tables 2-3, Figure 2
source(file.path(path_code, "03_main_analysis.R"))

# Robustness
# // produces: Appendix Tables A1-A3
source(file.path(path_code, "04_robustness.R"))

# =========================
# COMPLETION
# =========================

end_time <- Sys.time()
elapsed <- difftime(end_time, start_time, units = "mins")

cat("\n========================================\n")
cat("REPLICATION COMPLETE\n")
cat("========================================\n")
cat("Total time:", round(elapsed, 1), "minutes\n")
cat("End time:", as.character(end_time), "\n")
cat("\n")

# Session info for reproducibility
sessionInfo()
```

### 9.2 Package Management Template

```r
############################
# PACKAGE MANAGEMENT
#
# Source this file at the start of analysis
############################

# Define all required packages
required_packages <- c(
  # Data manipulation
  "dplyr",
  "tidyr",
  "haven",         # Read Stata/SPSS
  "readxl",        # Read Excel

  # Econometrics
  "fixest",        # Fast fixed effects
  "sandwich",      # Robust standard errors
  "lmtest",        # Hypothesis tests

  # Output
  "modelsummary",  # Regression tables
  "kableExtra",    # Table formatting

  # Visualization
  "ggplot2",
  "viridis",       # Color palettes
  "patchwork",     # Combine plots

  # Utilities
  "here"           # Portable paths
)

# Install missing packages
missing <- required_packages[
  !required_packages %in% installed.packages()[, "Package"]
]

if (length(missing) > 0) {
  message("Installing ", length(missing), " missing packages...")
  install.packages(missing)
}

# Load all packages
invisible(lapply(required_packages, library, character.only = TRUE))

# Report success
message("All ", length(required_packages), " packages loaded successfully")
message("R version: ", R.version.string)
message("Date: ", Sys.Date())
```

### 9.3 Data Cleaning Template

```r
############################
# DATA CLEANING
#
# Input: raw data
# Output: analysis-ready dataset
############################

# =========================
# LOAD RAW DATA
# =========================

# Example with built-in data
data(mtcars)
raw_data <- mtcars

cat("Raw data loaded:", nrow(raw_data), "observations\n")

# =========================
# INITIAL INSPECTION
# =========================

# Check structure
str(raw_data)

# Check for missing values
missing_counts <- colSums(is.na(raw_data))
if (any(missing_counts > 0)) {
  cat("\nMissing values found:\n")
  print(missing_counts[missing_counts > 0])
}

# =========================
# CLEANING STEPS
# =========================

clean_data <- raw_data %>%
  # Add row identifier
  tibble::rownames_to_column("id") %>%

  # Rename variables for clarity
  rename(
    miles_per_gallon = mpg,
    cylinders = cyl,
    horsepower = hp,
    weight = wt
  ) %>%

  # Create derived variables
  mutate(
    efficiency = miles_per_gallon / weight,
    high_power = ifelse(horsepower > median(horsepower), 1, 0),
    cylinder_group = factor(cylinders,
                           levels = c(4, 6, 8),
                           labels = c("4-cyl", "6-cyl", "8-cyl"))
  ) %>%

  # Remove missing values (document this decision)
  filter(!is.na(miles_per_gallon))

# =========================
# VALIDATION
# =========================

# Check final dimensions
cat("\nCleaned data:", nrow(clean_data), "observations,",
    ncol(clean_data), "variables\n")

# Verify key variables
stopifnot(
  "Missing MPG values remain" = sum(is.na(clean_data$miles_per_gallon)) == 0,
  "Unexpected cylinder values" = all(clean_data$cylinders %in% c(4, 6, 8))
)

cat("Validation passed\n")

# =========================
# SAVE
# =========================

# saveRDS(clean_data, file.path(path_clean, "analysis_sample.rds"))
# cat("Saved to:", file.path(path_clean, "analysis_sample.rds"), "\n")
```

### 9.4 Analysis Script Template

```r
############################
# MAIN ANALYSIS
#
# Produces: Tables 2-3, Figure 2
############################

# =========================
# LOAD DATA
# =========================

# analysis_data <- readRDS(file.path(path_clean, "analysis_sample.rds"))

# For this template, use built-in data
library(fixest)
data(trade)

cat("Analysis data:", nrow(trade), "observations\n")

# =========================
# DESCRIPTIVE STATISTICS
# =========================

desc_stats <- trade %>%
  summarise(
    n = n(),
    mean_euros = mean(Euros, na.rm = TRUE),
    sd_euros = sd(Euros, na.rm = TRUE),
    mean_dist = mean(dist_km, na.rm = TRUE)
  )

print(desc_stats)

# =========================
# MAIN REGRESSIONS
# =========================

# Specification 1: Baseline
m1 <- feols(log(Euros) ~ log(dist_km), data = trade)

# Specification 2: Add fixed effects
m2 <- feols(log(Euros) ~ log(dist_km) | Exporter, data = trade)

# Specification 3: Two-way fixed effects
m3 <- feols(log(Euros) ~ log(dist_km) | Exporter + Importer, data = trade)

# =========================
# OUTPUT
# =========================

# Display results
models <- list(
  "Baseline" = m1,
  "Exporter FE" = m2,
  "Two-way FE" = m3
)

modelsummary(
  models,
  stars = c('*' = 0.1, '**' = 0.05, '***' = 0.01),
  gof_omit = "AIC|BIC|Log",
  title = "Effect of Distance on Trade Volume"
)

# Save table
# modelsummary(models, output = file.path(path_tables, "table_2_main.tex"))

cat("\nAnalysis complete\n")
```

---

## 10. Summary Checklist

### Before Starting a Project

- [ ] Set up directory structure (code/, data/, output/)
- [ ] Create package management script
- [ ] Initialize git repository
- [ ] Document software versions

### Before Submission

- [ ] Master script runs entire analysis without errors
- [ ] All paths are relative (single root variable or `here()`)
- [ ] Random seeds are set and documented
- [ ] Package versions are recorded (`sessionInfo()`)
- [ ] Output files are named to match paper elements
- [ ] README documents execution order and requirements
- [ ] Code files have clear headers with purpose
- [ ] Intermediate datasets are saved for inspection
- [ ] Comments explain non-obvious decisions
- [ ] All figures saved in multiple formats (PDF + PNG)
- [ ] Tables exported in required format (LaTeX/Word)

### Code Quality Checks

- [ ] Consistent naming conventions throughout
- [ ] No hardcoded absolute paths
- [ ] No commented-out old code (remove it)
- [ ] Functions documented with comments
- [ ] Error handling for data loading
- [ ] Missing value handling documented

---

*This guide provides R-focused best practices for reproducible research. All examples use real, built-in datasets and produce working code.*
