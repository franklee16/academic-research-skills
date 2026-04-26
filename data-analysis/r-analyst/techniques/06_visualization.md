# Visualization & Graphics in R

Publication-quality figures, coefficient plots, event studies, and table output using ggplot2 and the tidyverse ecosystem.

---

## Quick Reference

| Task | Primary Package | Key Function | Example Dataset |
|------|-----------------|--------------|-----------------|
| Scatter plots | `ggplot2` | `geom_point()` | `mtcars`, `diamonds` |
| Line plots | `ggplot2` | `geom_line()` | `economics` |
| Histograms/density | `ggplot2` | `geom_histogram()`, `geom_density()` | `diamonds` |
| Coefficient plots | `fixest`, `broom` | `iplot()`, `coefplot()` | `trade`, `base_did` |
| Event studies | `fixest` | `iplot()` | `base_did` |
| RD plots | `rdrobust` | `rdplot()` | simulated data |
| Multi-panel figures | `patchwork` | `\|`, `/` operators | any |
| Regression tables | `modelsummary` | `modelsummary()` | any model output |
| Descriptive stats | `modelsummary` | `datasummary()` | any data frame |
| Color scales | `viridis`, `scales` | `scale_*_viridis_*()` | any |
| Text labels | `ggrepel` | `geom_text_repel()` | any |
| Export | `ggplot2` | `ggsave()` | any plot |

---

## 1. ggplot2 Fundamentals

### When to Use ggplot2

Use ggplot2 for virtually all static visualizations in R. The grammar of graphics approach provides:
- Consistent, readable syntax across plot types
- Easy layering of multiple geoms
- Excellent defaults with full customization options
- Seamless integration with the tidyverse

### 1.1 Basic Scatter with Regression Line

**When to Use:** Exploring relationships between two continuous variables, checking linearity assumptions.

```r
library(ggplot2)

# Using mtcars: relationship between weight and fuel efficiency
p <- ggplot(mtcars, aes(x = wt, y = mpg)) +
  geom_point(aes(size = hp), alpha = 0.6, color = "steelblue") +
  geom_smooth(method = "lm", se = TRUE, fill = "gray80", color = "navy") +
  labs(
    x = "Weight (1000 lbs)",
    y = "Miles per Gallon",
    title = "Fuel Efficiency vs. Vehicle Weight",
    size = "Horsepower"
  ) +
  theme_minimal() +
  theme(legend.position = "right")

print(p)
```

**Best Practice:** Always include informative axis labels with units. Use `alpha` for overlapping points.

### 1.2 Faceted Plots

**When to Use:** Comparing patterns across subgroups while maintaining consistent scales.

```r
library(ggplot2)

# Using diamonds: price by carat, faceted by cut quality
ggplot(diamonds, aes(x = carat, y = price)) +
  geom_point(alpha = 0.1, size = 0.5) +
  geom_smooth(method = "lm", color = "red") +
  facet_wrap(~ cut, nrow = 1) +
  scale_y_continuous(labels = scales::dollar_format()) +
  labs(
    x = "Carat Weight",
    y = "Price (USD)",
    title = "Diamond Price by Carat Weight Across Cut Quality"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
```

### 1.3 Line Plots for Time Series

**When to Use:** Displaying trends over time, comparing multiple series.

```r
library(ggplot2)
library(scales)

# Using economics: unemployment over time
ggplot(economics, aes(x = date, y = unemploy / 1000)) +
  geom_line(color = "steelblue", linewidth = 0.8) +
  geom_smooth(method = "loess", se = FALSE, color = "red", linetype = "dashed") +
  scale_x_date(date_labels = "%Y", date_breaks = "5 years") +
  labs(
    x = "Year",
    y = "Unemployed (millions)",
    title = "U.S. Unemployment Over Time",
    caption = "Source: Federal Reserve Economic Data"
  ) +
  theme_minimal()
```

### 1.4 Histograms and Density Plots

**When to Use:** Understanding the distribution of a single variable.

```r
library(ggplot2)

# Using diamonds: distribution of price
ggplot(diamonds, aes(x = price)) +
  geom_histogram(aes(y = after_stat(density)),
                 bins = 50, fill = "steelblue", alpha = 0.7) +
  geom_density(color = "red", linewidth = 1) +
  scale_x_continuous(labels = scales::dollar_format()) +
  labs(
    x = "Price (USD)",
    y = "Density",
    title = "Distribution of Diamond Prices"
  ) +
  theme_minimal()

# Grouped density comparison
ggplot(diamonds, aes(x = price, fill = cut)) +
  geom_density(alpha = 0.5) +
  scale_x_continuous(labels = scales::dollar_format(), limits = c(0, 10000)) +
  scale_fill_viridis_d() +
  labs(
    x = "Price (USD)",
    y = "Density",
    title = "Price Distribution by Cut Quality",
    fill = "Cut"
  ) +
  theme_minimal()
```

### 1.5 Box Plots and Violin Plots

**When to Use:** Comparing distributions across categories, identifying outliers.

```r
library(ggplot2)

# Using mpg: highway mileage by vehicle class
ggplot(mpg, aes(x = reorder(class, hwy, FUN = median), y = hwy, fill = class)) +
  geom_boxplot(alpha = 0.7, show.legend = FALSE) +
  geom_jitter(width = 0.2, alpha = 0.3, size = 0.8) +
  coord_flip() +
  scale_fill_viridis_d() +
  labs(
    x = "Vehicle Class",
    y = "Highway MPG",
    title = "Highway Fuel Efficiency by Vehicle Class"
  ) +
  theme_minimal()

# Violin plot alternative
ggplot(mpg, aes(x = reorder(class, hwy, FUN = median), y = hwy, fill = class)) +
  geom_violin(alpha = 0.7, show.legend = FALSE) +
  geom_boxplot(width = 0.1, fill = "white", alpha = 0.8) +
  coord_flip() +
  scale_fill_viridis_d() +
  labs(
    x = "Vehicle Class",
    y = "Highway MPG",
    title = "Highway Fuel Efficiency by Vehicle Class"
  ) +
  theme_minimal()
```

---

## 2. Publication-Ready Themes

### When to Use Custom Themes

Create custom themes for:
- Consistent styling across all paper figures
- Meeting journal-specific requirements
- Ensuring readability in print and online formats

### 2.1 Publication Theme Template

```r
library(ggplot2)

# Clean theme for journal submission
theme_publication <- function(base_size = 11, base_family = "") {
  theme_minimal(base_size = base_size, base_family = base_family) +
    theme(
      # Remove background and grid
      panel.border = element_blank(),
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),

      # Add axis lines
      axis.line = element_line(colour = "black", linewidth = 0.5),

      # Axis text and titles
      axis.text = element_text(color = "black", size = base_size),
      axis.title.x = element_text(margin = margin(t = 10), size = base_size + 1),
      axis.title.y = element_text(margin = margin(r = 10), size = base_size + 1),

      # Legend
      legend.position = "bottom",
      legend.key = element_blank(),
      legend.background = element_blank(),

      # Title
      plot.title = element_text(face = "bold", size = base_size + 2, hjust = 0),
      plot.subtitle = element_text(size = base_size, hjust = 0, color = "gray40"),
      plot.caption = element_text(size = base_size - 2, hjust = 1, color = "gray50"),

      # Margins
      plot.margin = margin(10, 10, 10, 10)
    )
}

# Apply to a plot
ggplot(mtcars, aes(x = wt, y = mpg)) +
  geom_point(size = 2, color = "steelblue") +
  geom_smooth(method = "lm", se = TRUE, color = "navy", fill = "gray80") +
  labs(
    x = "Weight (1000 lbs)",
    y = "Miles per Gallon",
    title = "Vehicle Weight vs. Fuel Efficiency",
    subtitle = "Linear relationship with 95% confidence band",
    caption = "Data: Motor Trend Car Road Tests (1974)"
  ) +
  theme_publication()
```

### 2.2 AER/QJE Style Theme

```r
# American Economic Review style
theme_aer <- function(base_size = 10) {
  theme_classic(base_size = base_size) +
    theme(
      # Minimal, clean look
      panel.grid = element_blank(),
      axis.line = element_line(linewidth = 0.3),
      axis.ticks = element_line(linewidth = 0.3),

      # No legend title
      legend.title = element_blank(),
      legend.position = "bottom",
      legend.direction = "horizontal",

      # Subtle colors
      strip.background = element_rect(fill = "gray95", color = NA),
      strip.text = element_text(face = "bold", size = base_size)
    )
}

# Example usage
ggplot(economics, aes(x = date, y = unemploy / 1000)) +
  geom_line(linewidth = 0.5) +
  labs(x = "", y = "Unemployed (millions)") +
  theme_aer()
```

---

## 3. Multi-Panel Figures with patchwork

### When to Use Multi-Panel Figures

Use multi-panel figures when:
- Comparing related analyses side-by-side
- Creating figure panels (A, B, C) for publication
- Showing the same relationship across subgroups
- Combining different plot types that share context

### 3.1 Basic Panel Composition

```r
library(ggplot2)
library(patchwork)

# Create individual panels using mtcars
p1 <- ggplot(mtcars, aes(x = wt, y = mpg)) +
  geom_point(color = "steelblue") +
  geom_smooth(method = "lm", se = FALSE, color = "red") +
  labs(title = "A. Weight vs. MPG", x = "Weight", y = "MPG") +
  theme_minimal()

p2 <- ggplot(mtcars, aes(x = hp, y = mpg)) +
  geom_point(color = "forestgreen") +
  geom_smooth(method = "lm", se = FALSE, color = "red") +
  labs(title = "B. Horsepower vs. MPG", x = "Horsepower", y = "MPG") +
  theme_minimal()

p3 <- ggplot(mtcars, aes(x = factor(cyl), y = mpg, fill = factor(cyl))) +
  geom_boxplot(show.legend = FALSE) +
  scale_fill_viridis_d() +
  labs(title = "C. MPG by Cylinders", x = "Cylinders", y = "MPG") +
  theme_minimal()

# Combine horizontally
(p1 | p2 | p3)

# Combine in a grid (2 on top, 1 on bottom)
(p1 | p2) / p3

# With shared theme applied to all
(p1 | p2) / p3 & theme_minimal()
```

### 3.2 Complex Layouts with Annotations

```r
library(ggplot2)
library(patchwork)

# Create panels
scatter <- ggplot(diamonds[sample(nrow(diamonds), 1000), ], aes(x = carat, y = price)) +
  geom_point(alpha = 0.3, color = "steelblue") +
  geom_smooth(method = "lm", color = "red") +
  labs(x = "Carat", y = "Price ($)") +
  theme_minimal()

histogram <- ggplot(diamonds, aes(x = price)) +
  geom_histogram(bins = 40, fill = "steelblue", alpha = 0.7) +
  labs(x = "Price ($)", y = "Count") +
  theme_minimal()

boxplot <- ggplot(diamonds, aes(x = cut, y = price, fill = cut)) +
  geom_boxplot(show.legend = FALSE) +
  scale_fill_viridis_d() +
  labs(x = "Cut Quality", y = "Price ($)") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Complex layout with widths and heights
layout <- (scatter | histogram) / boxplot +
  plot_layout(heights = c(2, 1)) +
  plot_annotation(
    title = "Diamond Prices Analysis",
    subtitle = "Exploring the relationship between physical properties and price",
    caption = "Data: ggplot2::diamonds",
    tag_levels = "A",
    theme = theme(
      plot.title = element_text(size = 14, face = "bold"),
      plot.subtitle = element_text(size = 10, color = "gray40")
    )
  )

print(layout)
```

### 3.3 Inset Plots

```r
library(ggplot2)
library(patchwork)

# Main plot
main_plot <- ggplot(economics, aes(x = date, y = unemploy / 1000)) +
  geom_line(color = "steelblue") +
  labs(x = "Year", y = "Unemployed (millions)",
       title = "U.S. Unemployment Over Time") +
  theme_minimal()

# Inset: recent years only
inset_plot <- ggplot(subset(economics, date >= as.Date("2000-01-01")),
                     aes(x = date, y = unemploy / 1000)) +
  geom_line(color = "red", linewidth = 0.5) +
  labs(x = "", y = "") +
  theme_minimal() +
  theme(
    plot.background = element_rect(fill = "white", color = "gray50"),
    axis.text = element_text(size = 6)
  )

# Combine with inset
main_plot + inset_element(inset_plot, left = 0.6, bottom = 0.6, right = 0.98, top = 0.98)
```

---

## 4. Coefficient Plots

### When to Use Coefficient Plots

Coefficient plots are essential for:
- Visualizing regression results (easier to interpret than tables)
- Comparing effects across multiple models
- Showing confidence intervals clearly
- Presenting many coefficients simultaneously

### 4.1 Using fixest::iplot and coefplot

```r
library(fixest)

# Load the trade dataset from fixest
data(trade, package = "fixest")

# Estimate models with different specifications
model1 <- feols(log(Euros) ~ log(dist_km) | Origin, data = trade)
model2 <- feols(log(Euros) ~ log(dist_km) + log(Year) | Origin, data = trade)
model3 <- feols(log(Euros) ~ log(dist_km) + log(Year) | Origin + Destination, data = trade)

# Basic coefficient plot
coefplot(model1)

# Multiple models comparison
coefplot(list("Base" = model1, "Year Control" = model2, "Two-way FE" = model3),
         keep = "dist_km",
         main = "Effect of Distance on Trade")

# Customize appearance
coefplot(model3,
         keep = c("dist_km", "Year"),
         ci_level = 0.95,
         pt.pch = 19,
         pt.col = "navy",
         ci.col = "navy",
         ref.line = 0,
         grid = FALSE,
         main = "Trade Determinants")
```

### 4.2 Manual Coefficient Plot with ggplot2

```r
library(ggplot2)
library(broom)
library(dplyr)

# Fit multiple models on mtcars
model1 <- lm(mpg ~ wt + hp + am, data = mtcars)
model2 <- lm(mpg ~ wt + hp + am + cyl, data = mtcars)
model3 <- lm(mpg ~ wt + hp + am + cyl + disp, data = mtcars)

# Extract and combine coefficients
extract_coefs <- function(model, model_name) {
  tidy(model, conf.int = TRUE) %>%
    filter(term != "(Intercept)") %>%
    mutate(model = model_name)
}

coef_df <- bind_rows(
  extract_coefs(model1, "Model 1"),
  extract_coefs(model2, "Model 2"),
  extract_coefs(model3, "Model 3")
)

# Create coefficient plot
ggplot(coef_df, aes(x = estimate, y = term, color = model)) +
  geom_vline(xintercept = 0, linetype = "dashed", color = "gray50") +
  geom_pointrange(aes(xmin = conf.low, xmax = conf.high),
                  position = position_dodge(width = 0.5),
                  size = 0.5) +
  scale_color_viridis_d(begin = 0.2, end = 0.8) +
  labs(
    x = "Coefficient Estimate",
    y = "",
    title = "Coefficient Comparison Across Models",
    color = "Model"
  ) +
  theme_minimal() +
  theme(
    legend.position = "bottom",
    panel.grid.minor = element_blank()
  )
```

### 4.3 Horizontal Coefficient Plot with Labels

```r
library(ggplot2)
library(broom)
library(dplyr)
library(ggrepel)

# Model with multiple predictors
model <- lm(mpg ~ wt + hp + drat + qsec + am + gear + carb, data = mtcars)

# Extract coefficients
coef_df <- tidy(model, conf.int = TRUE) %>%
  filter(term != "(Intercept)") %>%
  mutate(
    significant = p.value < 0.05,
    term_label = case_when(
      term == "wt" ~ "Weight (1000 lbs)",
      term == "hp" ~ "Horsepower",
      term == "drat" ~ "Rear Axle Ratio",
      term == "qsec" ~ "1/4 Mile Time",
      term == "am" ~ "Manual Transmission",
      term == "gear" ~ "Number of Gears",
      term == "carb" ~ "Number of Carburetors",
      TRUE ~ term
    )
  ) %>%
  arrange(estimate)

# Ordered coefficient plot
ggplot(coef_df, aes(x = reorder(term_label, estimate), y = estimate)) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "gray60", linewidth = 0.5) +
  geom_pointrange(aes(ymin = conf.low, ymax = conf.high, color = significant),
                  size = 0.6) +
  geom_text(aes(label = sprintf("%.2f", estimate)),
            hjust = -0.3, size = 3) +
  coord_flip() +
  scale_color_manual(values = c("FALSE" = "gray50", "TRUE" = "steelblue"),
                     labels = c("FALSE" = "p >= 0.05", "TRUE" = "p < 0.05"),
                     name = "Statistical\nSignificance") +
  labs(
    x = "",
    y = "Coefficient Estimate (95% CI)",
    title = "Determinants of Fuel Efficiency",
    subtitle = "Linear regression coefficients with 95% confidence intervals"
  ) +
  theme_minimal() +
  theme(
    legend.position = "bottom",
    panel.grid.major.y = element_blank()
  )
```

---

## 5. Event Study Visualization

### When to Use Event Studies

Event study plots are crucial for:
- Difference-in-differences designs with staggered treatment
- Testing parallel trends assumptions
- Showing dynamic treatment effects over time
- Identifying pre-trends that might violate identifying assumptions

### 5.1 Event Study with fixest

```r
library(fixest)

# Load base_did dataset from fixest (simulated DID data)
data(base_did, package = "fixest")

# Estimate event study model
# The data has: y (outcome), x1 (covariate), id (unit), period (time),
# treat (binary treatment indicator), post (post-treatment indicator)
event_model <- feols(
  y ~ i(period, treat, ref = 5) | id + period,
  cluster = ~id,
  data = base_did
)

# Built-in event study plot
iplot(event_model,
      xlab = "Period (Relative to Reference = 5)",
      ylab = "Effect Estimate",
      main = "Event Study: Treatment Effects Over Time")

# Customized appearance
iplot(event_model,
      ci_level = 0.95,
      pt.pch = 19,
      pt.col = "navy",
      ci.col = "navy",
      ref.line = 0,
      grid = TRUE,
      main = "Dynamic Treatment Effects")
```

### 5.2 Manual Event Study Plot with ggplot2

```r
library(fixest)
library(ggplot2)
library(broom)
library(dplyr)
library(stringr)

# Use fixest's base_did data
data(base_did, package = "fixest")

# Estimate event study
model <- feols(
  y ~ i(period, treat, ref = 5) | id + period,
  cluster = ~id,
  data = base_did
)

# Extract event study coefficients
event_coefs <- broom::tidy(model, conf.int = TRUE) %>%
  filter(str_detect(term, "period::")) %>%
  mutate(
    period = as.numeric(str_extract(term, "[0-9]+")),
    significant = conf.low > 0 | conf.high < 0
  )

# Add reference period (period = 5)
event_coefs <- bind_rows(
  event_coefs,
  tibble(period = 5, estimate = 0, conf.low = 0, conf.high = 0, significant = FALSE)
) %>%
  arrange(period)

# Create publication-quality event study plot
ggplot(event_coefs, aes(x = period, y = estimate)) +
  # Reference lines
  geom_hline(yintercept = 0, linetype = "dashed", color = "gray50") +
  geom_vline(xintercept = 5.5, linetype = "dotted", color = "red", linewidth = 0.8) +

  # Confidence ribbon
  geom_ribbon(aes(ymin = conf.low, ymax = conf.high), alpha = 0.2, fill = "steelblue") +

  # Line connecting estimates
  geom_line(color = "navy", linewidth = 0.8) +

  # Points with significance coloring
  geom_point(aes(color = significant), size = 3) +

  # Styling
  scale_color_manual(
    values = c("FALSE" = "gray50", "TRUE" = "navy"),
    guide = "none"
  ) +
  scale_x_continuous(breaks = 1:10) +

  # Labels
  labs(
    x = "Period",
    y = "Coefficient Estimate",
    title = "Event Study: Dynamic Treatment Effects",
    subtitle = "Vertical line indicates treatment onset; shaded region shows 95% CI",
    caption = "Reference period: 5. Robust standard errors clustered at unit level."
  ) +

  theme_minimal() +
  theme(
    panel.grid.minor = element_blank(),
    plot.subtitle = element_text(color = "gray40")
  )
```

### 5.3 Event Study with Multiple Groups

```r
library(fixest)
library(ggplot2)
library(dplyr)

# Create simulated multi-group event study data
set.seed(42)
n <- 1000
event_data <- tibble(
  id = rep(1:100, each = 10),
  time = rep(1:10, 100),
  group = rep(sample(c("Treatment A", "Treatment B", "Control"), 100, replace = TRUE), each = 10),
  rel_time = time - 5,
  treated = as.numeric(group != "Control" & time >= 5),
  y = 2 + 0.5 * (group == "Treatment A") * (time >= 5) * (time - 4) +
      0.3 * (group == "Treatment B") * (time >= 5) * (time - 4) +
      rnorm(n, 0, 0.5)
)

# Summarize by group and time
event_summary <- event_data %>%
  group_by(group, rel_time) %>%
  summarise(
    mean_y = mean(y),
    se = sd(y) / sqrt(n()),
    conf.low = mean_y - 1.96 * se,
    conf.high = mean_y + 1.96 * se,
    .groups = "drop"
  )

# Multi-group event study plot
ggplot(event_summary, aes(x = rel_time, y = mean_y, color = group, fill = group)) +
  geom_hline(yintercept = 2, linetype = "dashed", color = "gray50") +
  geom_vline(xintercept = -0.5, linetype = "dotted", color = "gray30") +
  geom_ribbon(aes(ymin = conf.low, ymax = conf.high), alpha = 0.2, color = NA) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  scale_color_viridis_d(end = 0.8) +
  scale_fill_viridis_d(end = 0.8) +
  labs(
    x = "Time Relative to Treatment",
    y = "Outcome",
    title = "Event Study by Treatment Group",
    color = "Group",
    fill = "Group"
  ) +
  theme_minimal() +
  theme(legend.position = "bottom")
```

---

## 6. Regression Discontinuity Visualization

### When to Use RD Plots

RD plots are essential for:
- Visualizing discontinuities at the threshold
- Checking for manipulation of the running variable
- Presenting RD results to non-technical audiences
- Validating the RD design before formal estimation

### 6.1 Manual RD Plot with ggplot2

```r
library(ggplot2)
library(dplyr)

# Create simulated RD data
set.seed(123)
n <- 500
rd_data <- tibble(
  running_var = runif(n, -1, 1),
  treatment = as.numeric(running_var >= 0),
  outcome = 2 + 0.5 * running_var + 0.8 * treatment + rnorm(n, 0, 0.3)
)

# Basic RD plot with local linear fits
ggplot(rd_data, aes(x = running_var, y = outcome)) +
  geom_point(aes(color = factor(treatment)), alpha = 0.5, size = 1.5) +
  geom_vline(xintercept = 0, linetype = "dashed", color = "gray40") +
  geom_smooth(data = filter(rd_data, running_var < 0),
              method = "lm", se = TRUE, color = "steelblue", fill = "steelblue", alpha = 0.2) +
  geom_smooth(data = filter(rd_data, running_var >= 0),
              method = "lm", se = TRUE, color = "coral", fill = "coral", alpha = 0.2) +
  scale_color_manual(values = c("0" = "steelblue", "1" = "coral"),
                     labels = c("0" = "Below Cutoff", "1" = "Above Cutoff")) +
  labs(
    x = "Running Variable (centered at cutoff)",
    y = "Outcome",
    title = "Regression Discontinuity Design",
    subtitle = "Local linear regression on each side of the cutoff",
    color = "Treatment Status"
  ) +
  theme_minimal() +
  theme(legend.position = "bottom")
```

### 6.2 RD Plot with Binned Means

```r
library(ggplot2)
library(dplyr)

# Create simulated data
set.seed(456)
n <- 1000
rd_data <- tibble(
  x = runif(n, -1, 1),
  treatment = as.numeric(x >= 0),
  y = 1 + 0.3 * x + 0.5 * treatment + 0.2 * x * treatment + rnorm(n, 0, 0.2)
)

# Create bins
n_bins <- 20
rd_data <- rd_data %>%
  mutate(
    bin = cut(x, breaks = n_bins, labels = FALSE),
    bin_center = (cut(x, breaks = n_bins, labels = FALSE) - 0.5) / n_bins * 2 - 1
  )

# Calculate bin means
bin_means <- rd_data %>%
  group_by(bin) %>%
  summarise(
    bin_center = mean(x),
    mean_y = mean(y),
    se = sd(y) / sqrt(n()),
    n = n(),
    .groups = "drop"
  ) %>%
  mutate(treatment = as.numeric(bin_center >= 0))

# RD plot with binned means
ggplot() +
  # Binned means with error bars
  geom_errorbar(data = bin_means,
                aes(x = bin_center, ymin = mean_y - 1.96 * se, ymax = mean_y + 1.96 * se),
                width = 0.02, color = "gray50") +
  geom_point(data = bin_means,
             aes(x = bin_center, y = mean_y, color = factor(treatment)),
             size = 3) +

  # Polynomial fits
  geom_smooth(data = filter(rd_data, x < 0),
              aes(x = x, y = y), method = "lm", formula = y ~ poly(x, 2),
              se = TRUE, color = "steelblue", fill = "steelblue", alpha = 0.15) +
  geom_smooth(data = filter(rd_data, x >= 0),
              aes(x = x, y = y), method = "lm", formula = y ~ poly(x, 2),
              se = TRUE, color = "coral", fill = "coral", alpha = 0.15) +

  # Cutoff line
  geom_vline(xintercept = 0, linetype = "dashed", linewidth = 0.8) +

  scale_color_manual(values = c("0" = "steelblue", "1" = "coral"), guide = "none") +
  labs(
    x = "Running Variable",
    y = "Outcome",
    title = "RD Plot with Binned Means",
    subtitle = "Dots show bin means with 95% CI; curves show quadratic fit"
  ) +
  theme_minimal()
```

### 6.3 Density Test Plot (McCrary Test)

```r
library(ggplot2)
library(dplyr)

# Using the same rd_data
# Density plot to check for manipulation
ggplot(rd_data, aes(x = x)) +
  geom_histogram(aes(y = after_stat(density)), bins = 40,
                 fill = "gray70", color = "white") +
  geom_density(color = "steelblue", linewidth = 1) +
  geom_vline(xintercept = 0, linetype = "dashed", color = "red", linewidth = 1) +
  labs(
    x = "Running Variable",
    y = "Density",
    title = "Density of Running Variable",
    subtitle = "Check for bunching at the cutoff (McCrary test visualization)"
  ) +
  theme_minimal()
```

---

## 7. Regression Tables

### When to Use Different Table Formats

- **modelsummary**: Best for most applications, highly customizable, exports to Word/LaTeX/HTML
- **fixest::etable**: Best when using fixest models, native LaTeX support
- **gtsummary**: Best for descriptive statistics and clinical/survey data

### 7.1 Basic Tables with modelsummary

```r
library(modelsummary)

# Fit multiple models on mtcars
model1 <- lm(mpg ~ wt, data = mtcars)
model2 <- lm(mpg ~ wt + hp, data = mtcars)
model3 <- lm(mpg ~ wt + hp + am, data = mtcars)

# Basic table
modelsummary(
  list("(1)" = model1, "(2)" = model2, "(3)" = model3),
  stars = c('*' = 0.1, '**' = 0.05, '***' = 0.01),
  gof_omit = "AIC|BIC|Log|F|RMSE"
)

# With custom coefficient names
modelsummary(
  list("(1)" = model1, "(2)" = model2, "(3)" = model3),
  stars = TRUE,
  coef_rename = c(
    "wt" = "Weight (1000 lbs)",
    "hp" = "Horsepower",
    "am" = "Manual Transmission"
  ),
  gof_map = c("nobs", "r.squared", "adj.r.squared")
)
```

### 7.2 Publication-Quality Tables

```r
library(modelsummary)

# Models
models <- list(
  "OLS" = lm(mpg ~ wt + hp, data = mtcars),
  "With Controls" = lm(mpg ~ wt + hp + am + cyl, data = mtcars),
  "Full" = lm(mpg ~ wt + hp + am + cyl + disp + drat, data = mtcars)
)

# Export to Word
modelsummary(
  models,
  output = "regression_table.docx",
  stars = c('*' = 0.1, '**' = 0.05, '***' = 0.01),
  coef_rename = c(
    "wt" = "Weight",
    "hp" = "Horsepower",
    "am" = "Manual",
    "cyl" = "Cylinders",
    "disp" = "Displacement",
    "drat" = "Rear Axle Ratio"
  ),
  gof_map = c("nobs", "r.squared", "adj.r.squared"),
  notes = c("Standard errors in parentheses.",
            "* p < 0.1, ** p < 0.05, *** p < 0.01"),
  title = "Table 1: Determinants of Fuel Efficiency"
)

# Export to LaTeX
modelsummary(
  models,
  output = "regression_table.tex",
  stars = c('*' = 0.1, '**' = 0.05, '***' = 0.01),
  gof_omit = "AIC|BIC|Log|F|RMSE"
)
```

### 7.3 fixest etable

```r
library(fixest)

# Load trade data
data(trade, package = "fixest")

# Multiple models with fixed effects
models <- list(
  feols(log(Euros) ~ log(dist_km), data = trade),
  feols(log(Euros) ~ log(dist_km) | Origin, data = trade),
  feols(log(Euros) ~ log(dist_km) | Origin + Destination, data = trade),
  feols(log(Euros) ~ log(dist_km) | Origin + Destination + Year, data = trade)
)

# Screen display
etable(models,
       headers = c("OLS", "Origin FE", "Two-way FE", "Three-way FE"),
       keep = "dist_km",
       se.below = TRUE,
       fitstat = c("n", "r2", "ar2"))

# LaTeX output
etable(models,
       file = "trade_results.tex",
       title = "Effect of Distance on Trade",
       label = "tab:trade",
       keep = "dist_km",
       dict = c("log(dist_km)" = "Log Distance"),
       fixef.group = list("Origin FE" = "Origin",
                         "Destination FE" = "Destination",
                         "Year FE" = "Year"),
       style.tex = style.tex("aer"))
```

---

## 8. Descriptive Statistics Tables

### When to Create Descriptive Tables

Create summary statistics tables for:
- First table in any empirical paper (Table 1)
- Describing sample characteristics
- Balance tables for RCTs or matching designs
- Comparing subgroups

### 8.1 Summary Statistics with modelsummary

```r
library(modelsummary)

# Basic summary statistics using mtcars
datasummary_skim(mtcars)

# Customized summary table
datasummary(
  mpg + wt + hp + disp + qsec ~
    N + Mean + SD + Min + Median + Max,
  data = mtcars,
  title = "Table 1: Summary Statistics"
)

# With better formatting
datasummary(
  (`Miles per Gallon` = mpg) +
  (`Weight (1000 lbs)` = wt) +
  (`Horsepower` = hp) +
  (`Displacement` = disp) ~
    N + Mean + SD + Min + Max,
  data = mtcars,
  fmt = 2,
  title = "Table 1: Vehicle Characteristics",
  notes = "Source: Motor Trend Car Road Tests (1974)"
)
```

### 8.2 Balance Tables

```r
library(modelsummary)
library(dplyr)

# Create treatment indicator in mtcars (e.g., based on transmission)
mtcars_bal <- mtcars %>%
  mutate(treatment = factor(am, labels = c("Automatic", "Manual")))

# Balance table comparing treatment groups
datasummary_balance(
  ~ treatment,
  data = mtcars_bal %>% select(mpg, wt, hp, disp, qsec, treatment),
  dinm = TRUE,                    # Show difference-in-means
  dinm_statistic = "p.value",    # Show p-values
  title = "Table 1: Balance Check by Transmission Type"
)
```

### 8.3 Grouped Summary Statistics

```r
library(modelsummary)
library(dplyr)

# Using diamonds dataset grouped by cut
diamonds_subset <- diamonds %>%
  select(price, carat, depth, table, cut) %>%
  filter(cut %in% c("Fair", "Good", "Very Good", "Premium", "Ideal"))

# Summary by cut quality
datasummary(
  price + carat + depth + table ~ cut * (Mean + SD),
  data = diamonds_subset,
  fmt = 2,
  title = "Diamond Characteristics by Cut Quality"
)

# Alternative: cross-tabulation
datasummary_crosstab(
  cut ~ color,
  data = diamonds,
  statistic = ~ N + Percent("col")
)
```

### 8.4 Publication-Ready Summary Table with gt

```r
library(dplyr)
library(tidyr)
library(gt)

# Create formatted summary statistics
summary_table <- mtcars %>%
  summarise(
    across(c(mpg, wt, hp, disp, qsec),
           list(
             Mean = ~mean(.),
             SD = ~sd(.),
             Min = ~min(.),
             Max = ~max(.)
           ))
  ) %>%
  pivot_longer(everything(),
               names_to = c("Variable", "Statistic"),
               names_sep = "_") %>%
  pivot_wider(names_from = Statistic, values_from = value) %>%
  mutate(
    Variable = case_when(
      Variable == "mpg" ~ "Miles per Gallon",
      Variable == "wt" ~ "Weight (1000 lbs)",
      Variable == "hp" ~ "Horsepower",
      Variable == "disp" ~ "Displacement (cu.in.)",
      Variable == "qsec" ~ "1/4 Mile Time (sec)"
    )
  )

# Create gt table
summary_table %>%
  gt() %>%
  tab_header(
    title = "Table 1: Summary Statistics",
    subtitle = "Motor Trend Car Road Tests (1974)"
  ) %>%
  fmt_number(columns = c(Mean, SD, Min, Max), decimals = 2) %>%
  cols_label(
    Variable = "",
    Mean = "Mean",
    SD = "Std. Dev.",
    Min = "Minimum",
    Max = "Maximum"
  ) %>%
  tab_source_note("N = 32 automobiles")
```

---

## 9. Color and Accessibility

### When to Consider Color Carefully

- Publications may be printed in grayscale
- Colorblind readers (8% of men)
- Projector/screen presentations
- Journal-specific requirements

### 9.1 Viridis Color Scales (Colorblind-Safe)

```r
library(ggplot2)
library(viridis)

# Continuous scale
ggplot(diamonds[sample(nrow(diamonds), 1000), ],
       aes(x = carat, y = price, color = depth)) +
  geom_point(alpha = 0.7) +
  scale_color_viridis_c(option = "plasma") +  # Options: viridis, magma, plasma, inferno, cividis
  labs(title = "Using viridis continuous scale") +
  theme_minimal()

# Discrete scale
ggplot(mpg, aes(x = class, y = hwy, fill = class)) +
  geom_boxplot(show.legend = FALSE) +
  scale_fill_viridis_d(option = "viridis") +
  labs(title = "Using viridis discrete scale") +
  theme_minimal() +
  coord_flip()
```

### 9.2 Custom Color Palettes

```r
library(ggplot2)

# Define a publication-safe palette
pub_colors <- c(
  "#0072B2",  # Blue

  "#D55E00",  # Vermillion (red-orange)
  "#009E73",  # Bluish green
  "#CC79A7",  # Reddish purple
  "#F0E442",  # Yellow
  "#56B4E9"   # Sky blue
)

# Apply to discrete scale
ggplot(mpg, aes(x = class, fill = class)) +
  geom_bar() +
  scale_fill_manual(values = pub_colors) +
  labs(title = "Custom Colorblind-Safe Palette") +
  theme_minimal() +
  theme(legend.position = "none")
```

### 9.3 Grayscale-Safe Plots

```r
library(ggplot2)

# Using shapes and linetypes instead of just color
ggplot(mtcars, aes(x = wt, y = mpg, shape = factor(cyl), linetype = factor(cyl))) +
  geom_point(size = 3) +
  geom_smooth(method = "lm", se = FALSE, color = "black") +
  scale_shape_manual(values = c(16, 17, 15)) +  # Circle, triangle, square
  labs(
    x = "Weight (1000 lbs)",
    y = "Miles per Gallon",
    shape = "Cylinders",
    linetype = "Cylinders",
    title = "Grayscale-Safe Plot with Shape Encoding"
  ) +
  theme_minimal()
```

---

## 10. Text Labels and Annotations

### When to Add Labels

- Highlighting specific data points
- Adding statistical results to plots
- Annotating important features
- Creating self-explanatory figures

### 10.1 Smart Labels with ggrepel

```r
library(ggplot2)
library(ggrepel)
library(dplyr)

# Label extreme points in mtcars
mtcars_labeled <- mtcars %>%
  tibble::rownames_to_column("car") %>%
  mutate(label = ifelse(mpg > 30 | mpg < 15 | wt > 5, car, ""))

ggplot(mtcars_labeled, aes(x = wt, y = mpg)) +
  geom_point(color = "steelblue", size = 2) +
  geom_text_repel(
    aes(label = label),
    size = 3,
    max.overlaps = 20,
    box.padding = 0.5,
    point.padding = 0.3,
    segment.color = "gray50",
    segment.size = 0.3
  ) +
  labs(
    x = "Weight (1000 lbs)",
    y = "Miles per Gallon",
    title = "Fuel Efficiency vs Weight",
    subtitle = "Extreme values labeled"
  ) +
  theme_minimal()
```

### 10.2 Statistical Annotations

```r
library(ggplot2)
library(dplyr)

# Calculate correlation for annotation
cor_value <- cor(mtcars$wt, mtcars$mpg)
model <- lm(mpg ~ wt, data = mtcars)
r_squared <- summary(model)$r.squared

ggplot(mtcars, aes(x = wt, y = mpg)) +
  geom_point(color = "steelblue", size = 2) +
  geom_smooth(method = "lm", se = TRUE, color = "navy", fill = "gray80") +
  annotate(
    "text",
    x = 5, y = 32,
    label = sprintf("r = %.2f\nR^2 = %.2f", cor_value, r_squared),
    hjust = 0,
    size = 4,
    fontface = "italic"
  ) +
  annotate(
    "segment",
    x = 4.5, xend = 4.8,
    y = 33, yend = 33,
    color = "navy",
    linewidth = 1
  ) +
  annotate(
    "text",
    x = 4.8, y = 33,
    label = " OLS fit",
    hjust = 0,
    size = 3
  ) +
  labs(
    x = "Weight (1000 lbs)",
    y = "Miles per Gallon",
    title = "Linear Relationship Between Weight and Fuel Efficiency"
  ) +
  theme_minimal()
```

### 10.3 Highlighting Regions

```r
library(ggplot2)

# Add highlighted regions
ggplot(economics, aes(x = date, y = unemploy / 1000)) +
  # Recession shading (approximate dates)
  annotate("rect",
           xmin = as.Date("2007-12-01"), xmax = as.Date("2009-06-01"),
           ymin = -Inf, ymax = Inf,
           fill = "red", alpha = 0.2) +
  annotate("rect",
           xmin = as.Date("2001-03-01"), xmax = as.Date("2001-11-01"),
           ymin = -Inf, ymax = Inf,
           fill = "red", alpha = 0.2) +
  # Main line
  geom_line(color = "steelblue", linewidth = 0.7) +
  # Labels
  annotate("text",
           x = as.Date("2008-06-01"), y = 14,
           label = "Great Recession",
           size = 3, fontface = "bold") +
  labs(
    x = "Year",
    y = "Unemployed (millions)",
    title = "U.S. Unemployment with Recession Periods Highlighted"
  ) +
  theme_minimal()
```

---

## 11. Export and File Formats

### When to Use Each Format

| Format | Use Case | Pros | Cons |
|--------|----------|------|------|
| PDF | Publication, archival | Vector, universal, print-ready | Some journals require specific formats |
| PNG | Web, presentations, drafts | Universal compatibility | Raster, can get blurry when scaled |
| TIFF | Some journals require it | High quality, uncompressed | Large file sizes |
| EPS | LaTeX documents | Vector, widely supported | Older format |
| SVG | Web, editing later | Vector, editable | Not always supported by journals |

### 11.1 High-Quality Export

```r
library(ggplot2)

# Create a plot
p <- ggplot(mtcars, aes(x = wt, y = mpg)) +
  geom_point(color = "steelblue", size = 2) +
  geom_smooth(method = "lm", color = "navy") +
  labs(x = "Weight", y = "MPG") +
  theme_minimal()

# Vector formats for publication
ggsave("figure1.pdf", plot = p, device = cairo_pdf,
       width = 6, height = 4, dpi = 300)

ggsave("figure1.eps", plot = p, device = cairo_ps,
       width = 6, height = 4)

# High-resolution raster
ggsave("figure1.png", plot = p,
       width = 6, height = 4, dpi = 600)

ggsave("figure1.tiff", plot = p,
       width = 6, height = 4, dpi = 600, compression = "lzw")

# Web-optimized PNG
ggsave("figure1_web.png", plot = p,
       width = 8, height = 5, dpi = 150)
```

### 11.2 Multi-Panel Export

```r
library(ggplot2)
library(patchwork)

# Create panels
p1 <- ggplot(mtcars, aes(wt, mpg)) + geom_point() + ggtitle("A")
p2 <- ggplot(mtcars, aes(hp, mpg)) + geom_point() + ggtitle("B")
p3 <- ggplot(mtcars, aes(factor(cyl), mpg)) + geom_boxplot() + ggtitle("C")
p4 <- ggplot(mtcars, aes(mpg)) + geom_histogram(bins = 10) + ggtitle("D")

# Combine
combined <- (p1 | p2) / (p3 | p4) & theme_minimal()

# Export combined figure
ggsave("figure_combined.pdf", plot = combined,
       width = 10, height = 8, device = cairo_pdf)
```

### 11.3 Batch Export

```r
library(ggplot2)
library(purrr)

# Create multiple plots programmatically
variables <- c("wt", "hp", "disp", "drat")

plots <- map(variables, function(var) {
  ggplot(mtcars, aes(x = .data[[var]], y = mpg)) +
    geom_point(color = "steelblue") +
    geom_smooth(method = "lm", color = "red") +
    labs(x = var, y = "MPG", title = paste("MPG vs", var)) +
    theme_minimal()
})

# Save all plots
walk2(plots, variables, function(p, var) {
  ggsave(paste0("figure_", var, ".png"), plot = p,
         width = 5, height = 4, dpi = 300)
})
```

---

## 12. Maps and Spatial Visualization

### When to Use Maps

- Geographic distribution of treatment effects
- Spatial variation in outcomes
- Regional comparisons
- Any data with geographic coordinates or boundaries

### 12.1 Basic Choropleth Map

```r
library(ggplot2)
library(maps)
library(dplyr)

# Get US state map data
states_map <- map_data("state")

# Create simulated state-level data
set.seed(42)
state_data <- tibble(
  region = unique(states_map$region),
  value = rnorm(length(unique(states_map$region)), mean = 50, sd = 15)
)

# Merge map with data
map_with_data <- left_join(states_map, state_data, by = "region")

# Create choropleth
ggplot(map_with_data, aes(x = long, y = lat, group = group, fill = value)) +
  geom_polygon(color = "white", linewidth = 0.2) +
  scale_fill_viridis_c(option = "plasma", name = "Value") +
  coord_map("albers", lat0 = 39, lat1 = 45) +
  labs(title = "Simulated State-Level Data") +
  theme_void() +
  theme(legend.position = "bottom")
```

### 12.2 Point Maps

```r
library(ggplot2)
library(maps)

# US map base
us_map <- map_data("state")

# Sample city data
cities <- data.frame(
  city = c("New York", "Los Angeles", "Chicago", "Houston", "Phoenix"),
  long = c(-74.0060, -118.2437, -87.6298, -95.3698, -112.0740),
  lat = c(40.7128, 34.0522, 41.8781, 29.7604, 33.4484),
  population = c(8.3, 3.9, 2.7, 2.3, 1.6)
)

# Map with points
ggplot() +
  geom_polygon(data = us_map, aes(x = long, y = lat, group = group),
               fill = "gray95", color = "gray70") +
  geom_point(data = cities, aes(x = long, y = lat, size = population),
             color = "red", alpha = 0.7) +
  scale_size_continuous(range = c(2, 10), name = "Population\n(millions)") +
  coord_map("albers", lat0 = 39, lat1 = 45) +
  labs(title = "Major U.S. Cities by Population") +
  theme_void()
```

---

## 13. Best Practices Checklist

### Figure Preparation

- [ ] Use vector formats (PDF, EPS) for line plots and charts
- [ ] Use 600+ DPI for raster images with many data points
- [ ] Match journal font requirements (often 8-10pt minimum)
- [ ] Include informative axis labels with units
- [ ] Add reference lines (zero line, treatment timing)
- [ ] Use colorblind-safe palettes (viridis or custom)
- [ ] Test figures in grayscale
- [ ] Ensure text is readable when printed at intended size

### Coefficient Plots

- [ ] Include confidence intervals (95% standard, note if different)
- [ ] Order coefficients meaningfully (by effect size, not alphabetically)
- [ ] Mark reference category clearly
- [ ] Use consistent scales across panels
- [ ] Add zero reference line
- [ ] Consider horizontal orientation for many coefficients

### Event Studies

- [ ] Include pre-treatment periods to show parallel trends
- [ ] Mark treatment onset clearly (vertical line)
- [ ] Omit one pre-period as reference (typically t = -1)
- [ ] Show confidence intervals
- [ ] Note clustering level in caption

### Tables

- [ ] Report standard errors or confidence intervals (not both)
- [ ] Include sample size (N) and R-squared
- [ ] Note clustering level and fixed effects
- [ ] Use consistent decimal places (typically 2-3)
- [ ] Add clear notes explaining significance levels
- [ ] Label variables with human-readable names

### Color Usage

- [ ] Use viridis or other colorblind-safe palettes
- [ ] Ensure figure works in grayscale
- [ ] Use shapes/linetypes in addition to color when possible
- [ ] Limit to 5-7 distinct colors maximum
- [ ] Maintain color consistency across related figures

---

## 14. Troubleshooting Common Issues

### Text and Label Problems

```r
# Text too small: increase base_size
theme_minimal(base_size = 14)

# Labels overlapping: use ggrepel
library(ggrepel)
geom_text_repel(aes(label = label), max.overlaps = 20)

# Axis labels cut off: adjust margins
theme(plot.margin = margin(10, 20, 10, 10))
```

### Color Issues

```r
# Colors look different in PDF: use cairo_pdf
ggsave("plot.pdf", device = cairo_pdf)

# Need more distinct colors: use viridis
scale_color_viridis_d(option = "turbo")
```

### Export Problems

```r
# Fonts not embedding: specify font family
theme(text = element_text(family = "Arial"))

# File too large: use compression
ggsave("plot.tiff", compression = "lzw")

# Plot looks different size: specify dimensions explicitly
ggsave("plot.pdf", width = 6.5, height = 4.5, units = "in")
```

### Performance with Large Datasets

```r
# Too many points: sample or use alpha
geom_point(alpha = 0.1, size = 0.5)

# Or use 2D binning
geom_bin2d(bins = 50) +
  scale_fill_viridis_c()

# Or hexbin
geom_hex(bins = 30) +
  scale_fill_viridis_c()
```

---

## Package Reference

| Package | Purpose | Installation |
|---------|---------|--------------|
| `ggplot2` | Core plotting | `install.packages("ggplot2")` |
| `patchwork` | Multi-panel figures | `install.packages("patchwork")` |
| `scales` | Axis formatting | `install.packages("scales")` |
| `viridis` | Colorblind-safe palettes | `install.packages("viridis")` |
| `ggrepel` | Smart text labels | `install.packages("ggrepel")` |
| `fixest` | Coefficient/event study plots | `install.packages("fixest")` |
| `modelsummary` | Regression tables | `install.packages("modelsummary")` |
| `broom` | Tidy model output | `install.packages("broom")` |
| `gt` | Publication tables | `install.packages("gt")` |
| `maps` | Base map data | `install.packages("maps")` |
| `sf` | Spatial data handling | `install.packages("sf")` |
