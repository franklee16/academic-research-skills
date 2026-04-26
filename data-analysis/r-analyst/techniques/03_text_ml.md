# Text Analysis & Machine Learning in R

Comprehensive guide to text analysis and ML methods with reproducible examples using package vignette data.

---

## Quick Reference

| Task | R Package | Key Function | Example Dataset |
|------|-----------|--------------|-----------------|
| LDA Topic Modeling | topicmodels | `LDA()` | AssociatedPress |
| Structural Topic Model | stm | `stm()` | gadarian |
| Sentiment Analysis | tidytext | `get_sentiments()` | janeaustenr books |
| TF-IDF | tidytext | `bind_tf_idf()` | janeaustenr books |
| Causal Forests | grf | `causal_forest()` | Simulated |
| Random Forests | ranger | `ranger()` | iris, mtcars |
| SVM | caret, e1071 | `train()`, `svm()` | iris |
| Cross-Validation | caret | `trainControl()` | PimaIndiansDiabetes2 |
| GAMs | mgcv | `gam()` | gamSim() |
| EFA | psych | `fa()` | bfi |
| CFA | lavaan | `cfa()` | HolzingerSwineford1939 |
| IRT | mirt | `mirt()` | LSAT6, simdata() |
| Reliability | psych | `alpha()`, `ICC()` | bfi |

### Installation

```r
# Install all required packages
packages <- c(
  "topicmodels", "tm", "LDAvis", "slam",   # Topic modeling
  "stm",                                    # STM
  "tidytext", "janeaustenr", "textdata",   # Sentiment (textdata for lexicons)
  "dplyr", "tidyr", "ggplot2", "stringr",  # Data manipulation
  "grf",                                    # Causal forests
  "ranger",                                 # Random forests
  "caret", "e1071", "kernlab",             # SVM
  "mlbench", "pROC",                        # Classification/CV
  "mgcv",                                   # GAMs
  "psych", "lme4",                          # Factor analysis & ICC
  "lavaan", "semTools",                     # CFA
  "mirt"                                    # IRT
)

# Install if not present
install.packages(setdiff(packages, rownames(installed.packages())))

# Note: First use of sentiment lexicons requires one-time download:
# tidytext::get_sentiments("afinn")  # Will prompt to download
```

---

## 1. Topic Modeling

Topic models discover latent themes in document collections. They are unsupervised methods that identify groups of co-occurring words.

### 1.1 Latent Dirichlet Allocation (LDA)

**When to use LDA:**
- Exploratory analysis of large document collections
- No metadata/covariates needed to explain topic variation
- Goal is to discover themes without prior hypotheses
- Documents are reasonably long (paragraphs to pages)

**Assumptions:**
- Documents are mixtures of topics
- Topics are distributions over words
- Word order doesn't matter (bag-of-words)
- Number of topics K is fixed and known

**Common pitfalls:**
- Choosing K arbitrarily (use diagnostics)
- Over-interpreting topics with low coherence
- Not preprocessing adequately (stopwords, rare terms)
- Ignoring multi-word expressions

```r
library(topicmodels)
library(tm)

# Load built-in Associated Press dataset
# 2,246 news articles with 10,473 unique terms
data("AssociatedPress")

# Inspect the document-term matrix
AssociatedPress
#> <<DocumentTermMatrix (documents: 2246, terms: 10473)>>
#> Non-/sparse entries: 302031/23220327
#> Sparsity           : 99%

# Remove sparse terms (keep terms appearing in at least 2% of docs)
ap_dtm <- removeSparseTerms(AssociatedPress, sparse = 0.98)
ap_dtm
#> Now ~1,600 terms retained

# Remove any documents that became empty after filtering
row_totals <- slam::row_sums(ap_dtm)
ap_dtm <- ap_dtm[row_totals > 0, ]
#> 2,244 documents remain

# Fit LDA with 10 topics using Gibbs sampling
set.seed(12345)
lda_model <- LDA(
  ap_dtm,
  k = 10,
  method = "Gibbs",
  control = list(
    seed = 12345,
    burnin = 1000,
    iter = 2000,
    thin = 100
  )
)

# View top 10 words per topic
terms(lda_model, 10)
#>       Topic 1    Topic 2     Topic 3   Topic 4    Topic 5
#> [1,]  "percent"  "soviet"    "police"  "bush"     "court"
#> [2,]  "year"     "united"    "people"  "house"    "case"
#> [3,]  "million"  "states"    "city"    "president" "judge"
#> ...

# Get topic assignments for each document
doc_topics <- topics(lda_model)
head(doc_topics)
#> [1] 10  5  7  3  2  8

# Get topic probabilities for each document (theta matrix)
doc_topic_probs <- posterior(lda_model)$topics
head(round(doc_topic_probs, 3))
#>          1     2     3     4     5     6     7     8     9    10
#> [1,] 0.012 0.012 0.012 0.012 0.012 0.012 0.012 0.012 0.012 0.880
#> [2,] 0.011 0.011 0.011 0.011 0.792 0.011 0.011 0.011 0.011 0.011
#> ...
```

#### Choosing the Number of Topics

Use perplexity (lower is better) or coherence metrics to guide K selection.

**Note:** For Gibbs-sampled LDA models, perplexity calculation requires the VEM method or using held-out data. Here we use VEM for model comparison:

```r
# Compare models with different K values using VEM (faster for comparison)
k_values <- c(5, 10, 15, 20, 25)
perplexities <- numeric(length(k_values))

set.seed(12345)
for (i in seq_along(k_values)) {
  model <- LDA(
    ap_dtm,
    k = k_values[i],
    method = "VEM",  # VEM method supports perplexity directly
    control = list(seed = 12345)
  )
  perplexities[i] <- perplexity(model)
}

# Plot perplexity by K
plot(k_values, perplexities, type = "b",
     xlab = "Number of Topics (K)",
     ylab = "Perplexity",
     main = "Model Selection: Perplexity vs K")

# Results (approximate):
#> K=5:  ~2800
#> K=10: ~2500
#> K=15: ~2350
#> K=20: ~2250  <- Elbow often around here
#> K=25: ~2200

# Alternative: Use log-likelihood for Gibbs models
# logLik(lda_model)  # Returns log-likelihood
```

#### Visualizing Topics with LDAvis

```r
library(LDAvis)
library(servr)

# Prepare data for visualization
phi <- posterior(lda_model)$terms      # Topic-word distributions
theta <- posterior(lda_model)$topics   # Document-topic distributions
vocab <- colnames(phi)
doc_length <- slam::row_sums(ap_dtm)
term_freq <- slam::col_sums(ap_dtm)

# Create JSON for visualization
json <- createJSON(
  phi = phi,
  theta = theta,
  vocab = vocab,
  doc.length = doc_length,
  term.frequency = term_freq
)

# Launch interactive visualization
serVis(json)
```

---

### 1.2 Structural Topic Model (STM)

**When to use STM over LDA:**
- Document metadata (author, date, source) may explain topic prevalence
- You hypothesize that covariates affect what topics appear
- You want to model how topic expression varies by group
- Need statistical inference on covariate effects

**Key advantages:**
- Prevalence covariates: What topics are discussed?
- Content covariates: How topics are discussed differently by groups
- Built-in tools for model selection and validation

```r
library(stm)

# Load built-in gadarian dataset
# Survey responses about immigration with treatment/control
data(gadarian)

# Inspect the data
str(gadarian)
#> 'data.frame': 341 obs. of 4 variables:
#>  $ MetaID   : int  1 2 3 4 5 6 7 ...
#>  $ treatment: int  1 0 1 0 1 1 0 ...
#>  $ pid_rep  : int  0 0 1 0 1 0 0 ...
#>  $ open.ended.response: chr "..." ...

head(gadarian$open.ended.response, 2)
#> [1] "..."  # Open-ended responses about immigration

# Preprocess the text
processed <- textProcessor(
  documents = gadarian$open.ended.response,
  metadata = gadarian,
  lowercase = TRUE,
  removestopwords = TRUE,
  removenumbers = TRUE,
  removepunctuation = TRUE,
  stem = TRUE,
  verbose = FALSE
)

# Prepare documents (remove sparse terms)
out <- prepDocuments(
  processed$documents,
  processed$vocab,
  processed$meta,
  lower.thresh = 5  # Terms must appear in 5+ documents
)
#> Removing 970 of 1102 terms (1579 of 3789 tokens) due to frequency
#> Your corpus now has 334 documents, 132 terms and 2210 tokens.

# Check what was removed
out$meta         # Metadata aligned with documents
length(out$vocab) # Vocabulary size after filtering
#> [1] 132
```

#### Selecting Number of Topics with searchK

```r
# Search over candidate K values
set.seed(12345)
K_search <- searchK(
  out$documents,
  out$vocab,
  K = c(5, 7, 10, 15),
  prevalence = ~ treatment + pid_rep,
  data = out$meta,
  verbose = FALSE
)

# Plot diagnostics
plot(K_search)
#> Look for:
#> - High semantic coherence
#> - High exclusivity
#> - Lower residuals
#> - Held-out likelihood plateau
```

#### Fitting STM with Prevalence Covariates

```r
# Fit STM with 7 topics
# Prevalence: treatment and party ID affect topic proportions
set.seed(12345)
stm_model <- stm(
  documents = out$documents,
  vocab = out$vocab,
  K = 7,
  prevalence = ~ treatment + pid_rep,
  data = out$meta,
  seed = 12345,
  verbose = FALSE
)

# View top words per topic (multiple metrics)
labelTopics(stm_model, n = 7)
#> Topic 1 Top Words:
#>   Highest Prob: immigr, illeg, countri, work, come, job, live
#>   FREX: illeg, citizenship, border, deport, amnesti, crimin, green
#>   Lift: amnesti, citizenship, deport, applic, citizen, document, fine
#>   Score: illeg, amnesti, citizenship, border, deport, citizen, card

# Summary of topic proportions
plot(stm_model, type = "summary", xlim = c(0, 0.4))
```

#### Estimating Covariate Effects

```r
# Estimate effect of treatment on topic prevalence
effects <- estimateEffect(
  formula = 1:7 ~ treatment + pid_rep,
  stmobj = stm_model,
  metadata = out$meta,
  uncertainty = "Global"
)

# Summary for specific topics
summary(effects, topics = c(1, 3, 5))
#> Topic 1:
#>   Covariate: treatment
#>   Estimate: 0.05 (SE: 0.02), p < 0.05
#>   Interpretation: Treatment increases discussion of Topic 1

# Visualize treatment effect
plot(
  effects,
  covariate = "treatment",
  topics = c(1, 3, 5),
  model = stm_model,
  method = "difference",
  cov.value1 = 1,
  cov.value2 = 0,
  xlab = "Treatment Effect on Topic Prevalence",
  main = "Effect of Anxiety Treatment on Immigration Topics",
  xlim = c(-0.15, 0.15)
)
```

#### Finding Representative Documents

```r
# Find documents most associated with each topic
findThoughts(
  stm_model,
  texts = gadarian$open.ended.response,
  topics = 1,
  n = 3
)
#> Topic 1:
#>  [1] "I think we need stronger border security..."
#>  [2] "Illegal immigration is a serious problem..."
#>  [3] "We should enforce existing laws..."
```

#### Content Covariates: How Topics Differ by Group

Content covariates model how the *words used* within a topic vary by group (not just topic prevalence):

```r
# Fit STM with both prevalence AND content covariates
set.seed(12345)
stm_content <- stm(
  documents = out$documents,
  vocab = out$vocab,
  K = 5,
  prevalence = ~ treatment + pid_rep,   # What topics appear
  content = ~ treatment,                 # How words differ by treatment
  data = out$meta,
  seed = 12345,
  verbose = FALSE
)

# View how word usage differs by treatment within a topic
plot(stm_content, type = "perspectives", topics = 1)
#> Shows words more associated with treatment=0 vs treatment=1
#> within the same topic

# Example interpretation:
#> Topic about "immigration concerns" might use:
#> - Treatment group (anxious): "dangerous", "threat", "crime"
#> - Control group: "policy", "reform", "workers"
```

#### Topic Correlation

Examine which topics tend to co-occur in documents:

```r
# Calculate topic correlations
topic_corr <- topicCorr(stm_model, method = "simple")

# View correlation matrix
print(round(topic_corr$cor, 2))
#>       [,1]  [,2]  [,3]  [,4]  [,5]
#> [1,]  1.00 -0.15  0.08 -0.32 -0.21
#> [2,] -0.15  1.00 -0.28  0.12 -0.18
#> [3,]  0.08 -0.28  1.00 -0.25 -0.10
#> ...

# Positive correlation: Topics co-occur
# Negative correlation: Topics are mutually exclusive

# Visualize topic network (requires igraph)
# plot(topic_corr)
```

#### Model Diagnostics: Semantic Coherence and Exclusivity

```r
# For model selection, balance coherence and exclusivity
# Coherence: Do top words co-occur in documents? (higher = better)
# Exclusivity: Are top words unique to this topic? (higher = better)

# Compare models with different K
models <- list()
for (k in c(5, 7, 10)) {
  models[[as.character(k)]] <- stm(
    documents = out$documents,
    vocab = out$vocab,
    K = k,
    prevalence = ~ treatment,
    data = out$meta,
    seed = 12345,
    verbose = FALSE,
    max.em.its = 20
  )
}

# Extract diagnostics
diagnostics <- lapply(names(models), function(k) {
  data.frame(
    K = k,
    coherence = mean(semanticCoherence(models[[k]], out$documents)),
    exclusivity = mean(exclusivity(models[[k]]))
  )
})
diagnostics <- do.call(rbind, diagnostics)
print(diagnostics)
#>   K coherence exclusivity
#> 1 5     -85.2        9.42
#> 2 7     -92.1        9.58
#> 3 10    -98.7        9.71

# Trade-off: More topics = higher exclusivity but lower coherence
# Choose K where both are reasonably high
```

---

## 2. Sentiment Analysis

Sentiment analysis measures the emotional tone or opinion expressed in text.

### 2.1 Dictionary-Based Methods

**When to use dictionary methods:**
- Large-scale analysis where manual coding is impractical
- Domain has established, validated lexicons
- Need reproducible, transparent scoring
- Exploratory analysis before more complex methods

**Limitations:**
- Ignores context, negation, sarcasm
- Domain mismatch (lexicons often built for product reviews)
- Cannot capture nuance or implicit sentiment
- Word-level aggregation loses sentence structure

**Important:** The sentiment lexicons require a one-time download via the `textdata` package. When you first call `get_sentiments()`, you'll be prompted to download the lexicon.

```r
library(tidytext)
library(dplyr)
library(tidyr)
library(janeaustenr)
library(ggplot2)
library(stringr)

# Load Jane Austen novels
austen_books <- austen_books()
head(austen_books)
#>   book                text
#> 1 Sense & Sensibility SENSE AND SENSIBILITY
#> 2 Sense & Sensibility by Jane Austen
#> ...

# Tokenize to one word per row
tidy_austen <- austen_books %>%
  group_by(book) %>%
  mutate(
    linenumber = row_number(),
    chapter = cumsum(str_detect(text, regex("^chapter [\\divxlc]",
                                            ignore_case = TRUE)))
  ) %>%
  ungroup() %>%
  unnest_tokens(word, text)

head(tidy_austen)
#>   book                linenumber chapter word
#> 1 Sense & Sensibility          1       0 sense
#> 2 Sense & Sensibility          1       0 and
#> 3 Sense & Sensibility          1       0 sensibility
```

### 2.2 Comparing Lexicons

Three main sentiment lexicons are available:

| Lexicon | Type | Scale | Best for |
|---------|------|-------|----------|
| AFINN | Numeric | -5 to +5 | Intensity measurement |
| Bing | Binary | pos/neg | Simple polarity |
| NRC | Categorical | 8 emotions + pos/neg | Emotional analysis |

```r
# First-time use: You'll be prompted to download each lexicon
# After download, they're cached locally

# View available lexicons
get_sentiments("afinn") %>% head()
#>   word       value
#> 1 abandon       -2
#> 2 abandoned     -2
#> 3 abandons      -2

get_sentiments("bing") %>% head()
#>   word        sentiment
#> 1 2-faces     negative
#> 2 abnormal    negative

get_sentiments("nrc") %>% head()
#>   word        sentiment
#> 1 abacus      trust
#> 2 abandon     fear
#> 3 abandon     negative
```

#### AFINN: Numeric Sentiment Scores

```r
# Join with AFINN lexicon
afinn_sentiment <- tidy_austen %>%
  inner_join(get_sentiments("afinn"), by = "word") %>%
  group_by(book, index = linenumber %/% 80) %>%  # 80-line chunks
  summarize(
    sentiment = sum(value),
    n_words = n(),
    .groups = "drop"
  )

# Plot sentiment trajectory for Pride & Prejudice
afinn_sentiment %>%
  filter(book == "Pride & Prejudice") %>%
  ggplot(aes(index, sentiment)) +
  geom_col(show.legend = FALSE) +
  labs(
    title = "Sentiment Trajectory: Pride & Prejudice",
    x = "Narrative Time (80-line chunks)",
    y = "Sentiment Score (AFINN)"
  )

# Summary statistics by book
afinn_sentiment %>%
  group_by(book) %>%
  summarize(
    mean_sentiment = mean(sentiment),
    sd_sentiment = sd(sentiment),
    min_sentiment = min(sentiment),
    max_sentiment = max(sentiment)
  )
#>   book                mean_sentiment sd_sentiment
#> 1 Emma                         12.5         15.2
#> 2 Mansfield Park                8.3         12.1
#> 3 Northanger Abbey             10.1         13.8
#> 4 Persuasion                    9.7         11.9
#> 5 Pride & Prejudice            11.8         14.6
#> 6 Sense & Sensibility           9.4         13.2
```

#### Bing: Binary Sentiment Classification

```r
# Calculate net sentiment (positive - negative)
bing_sentiment <- tidy_austen %>%
  inner_join(get_sentiments("bing"), by = "word") %>%
  count(book, index = linenumber %/% 80, sentiment) %>%
  pivot_wider(names_from = sentiment, values_from = n, values_fill = 0) %>%
  mutate(net_sentiment = positive - negative)

# Compare all books
bing_sentiment %>%
  ggplot(aes(index, net_sentiment, fill = book)) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~book, ncol = 2, scales = "free_x") +
  labs(
    title = "Sentiment Across Jane Austen Novels",
    x = "Narrative Time",
    y = "Net Sentiment (Bing)"
  )
```

#### NRC: Emotional Content Analysis

```r
# Analyze emotions in Pride & Prejudice
nrc_emotions <- tidy_austen %>%
  filter(book == "Pride & Prejudice") %>%
  inner_join(get_sentiments("nrc"), by = "word") %>%
  filter(!sentiment %in% c("positive", "negative")) %>%
  count(sentiment, sort = TRUE)

nrc_emotions
#>   sentiment     n
#> 1 trust      2017
#> 2 fear       1381
#> 3 anticipation 1279
#> 4 joy        1148
#> 5 sadness    1062
#> 6 anger       863
#> 7 surprise    629
#> 8 disgust     567

# Plot emotional profile
nrc_emotions %>%
  mutate(sentiment = reorder(sentiment, n)) %>%
  ggplot(aes(n, sentiment)) +
  geom_col() +
  labs(
    title = "Emotional Profile: Pride & Prejudice",
    x = "Word Count",
    y = "Emotion (NRC)"
  )
```

#### Comparing Lexicon Results

```r
# Compare lexicons on same data
comparison <- bind_rows(
  tidy_austen %>%
    inner_join(get_sentiments("afinn"), by = "word") %>%
    group_by(book, index = linenumber %/% 80) %>%
    summarize(sentiment = sum(value), .groups = "drop") %>%
    mutate(method = "AFINN"),

  tidy_austen %>%
    inner_join(get_sentiments("bing"), by = "word") %>%
    count(book, index = linenumber %/% 80, sentiment) %>%
    pivot_wider(names_from = sentiment, values_from = n, values_fill = 0) %>%
    mutate(sentiment = positive - negative, method = "Bing") %>%
    select(book, index, sentiment, method)
)

# Correlation between methods
comparison %>%
  pivot_wider(names_from = method, values_from = sentiment) %>%
  summarize(correlation = cor(AFINN, Bing, use = "complete.obs"))
#> Typically r ~ 0.7-0.8 (lexicons capture similar but not identical signal)
```

### 2.3 TF-IDF: Term Frequency-Inverse Document Frequency

**When to use TF-IDF:**
- Finding words that distinguish documents from each other
- Identifying characteristic vocabulary of texts
- Feature engineering for document classification
- Reducing impact of common words without a stopword list

**How it works:**
- TF (Term Frequency): How often a word appears in a document
- IDF (Inverse Document Frequency): Penalizes words common across all documents
- TF-IDF = TF x IDF: High for words frequent in a document but rare overall

```r
library(tidytext)
library(dplyr)
library(janeaustenr)

# Count words per book
book_words <- austen_books() %>%
  unnest_tokens(word, text) %>%
  count(book, word, sort = TRUE)

# Calculate total words per book
total_words <- book_words %>%
  group_by(book) %>%
  summarize(total = sum(n))

book_words <- left_join(book_words, total_words, by = "book")

head(book_words)
#>   book                word      n  total
#> 1 Mansfield Park      the   6206 160460
#> 2 Mansfield Park      to    5475 160460
#> 3 Mansfield Park      and   5438 160460
#> ...

# Calculate TF-IDF
book_tf_idf <- book_words %>%
  bind_tf_idf(word, book, n)

head(book_tf_idf)
#>   book           word      n  total     tf   idf tf_idf
#> 1 Mansfield Park the   6206 160460 0.0387 0     0
#> 2 Mansfield Park to    5475 160460 0.0341 0     0
#> ...
#> Common words have idf=0 and tf_idf=0
```

#### Finding Characteristic Words

```r
# Top TF-IDF words per book (most distinctive)
book_tf_idf %>%
  group_by(book) %>%
  slice_max(tf_idf, n = 5) %>%
  ungroup() %>%
  select(book, word, tf_idf)

#>   book                word       tf_idf
#> 1 Emma                emma       0.00536
#> 2 Emma                weston     0.00433
#> 3 Emma                knightley  0.00396
#> 4 Emma                elton      0.00355
#> 5 Emma                woodhouse  0.00308
#> 6 Mansfield Park      fanny      0.00471
#> 7 Mansfield Park      crawford   0.00410
#> ...

# Character names emerge as most distinctive!
# This is expected - names are unique to each book
```

#### Visualizing TF-IDF

```r
library(ggplot2)

# Plot top 10 words per book
book_tf_idf %>%
  group_by(book) %>%
  slice_max(tf_idf, n = 10) %>%
  ungroup() %>%
  mutate(word = reorder_within(word, tf_idf, book)) %>%
  ggplot(aes(tf_idf, word, fill = book)) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~book, scales = "free_y") +
  scale_y_reordered() +
  labs(
    title = "Most Distinctive Words by Book (TF-IDF)",
    x = "TF-IDF",
    y = NULL
  )
```

#### TF-IDF for Document Classification

```r
# TF-IDF is often used as features for ML classifiers
# Create a document-term matrix with TF-IDF weights

# Example: Prepare for classification
dtm_tfidf <- book_tf_idf %>%
  # Keep only top 1000 words by mean TF-IDF
  group_by(word) %>%
  mutate(mean_tfidf = mean(tf_idf)) %>%
  ungroup() %>%
  filter(dense_rank(desc(mean_tfidf)) <= 1000) %>%
  # Pivot to wide format
  select(book, word, tf_idf) %>%
  pivot_wider(names_from = word, values_from = tf_idf, values_fill = 0)

dim(dtm_tfidf)
#> [1] 6 1001  (6 books x 1000 features + book column)
```

---

## 3. Machine Learning for Causal Inference

### 3.1 Causal Forests

**When to use causal forests:**
- Estimating heterogeneous treatment effects (HTEs)
- Treatment effects may vary by observed covariates
- Want data-driven discovery of effect heterogeneity
- Large sample sizes available (n > 1000 recommended)

**Assumptions (same as standard causal inference):**
- Unconfoundedness: No unmeasured confounders
- Overlap: Positive probability of treatment for all X
- SUTVA: No interference between units

**Key features of GRF:**
- Honest estimation (sample splitting)
- Valid confidence intervals
- Automatic covariate selection for HTE

```r
library(grf)

# Simulate data with heterogeneous treatment effects
set.seed(12345)
n <- 2000
p <- 10

# Covariates
X <- matrix(rnorm(n * p), n, p)
colnames(X) <- paste0("X", 1:p)

# Treatment assignment (randomized)
W <- rbinom(n, 1, 0.5)

# True treatment effect varies with X1 and X2
# tau(x) = 1 + 2*X1 + X2 (heterogeneous effect)
tau <- 1 + 2 * X[, 1] + X[, 2]

# Outcome with heterogeneous effect
Y <- X[, 1] + X[, 2] + tau * W + rnorm(n)

# Summary of true effects
summary(tau)
#>    Min. 1st Qu.  Median    Mean 3rd Qu.    Max.
#>  -4.89   -0.32    1.01    1.00    2.31    6.84
```

#### Fitting the Causal Forest

```r
# Fit causal forest
cf <- causal_forest(
  X = X,
  Y = Y,
  W = W,
  num.trees = 2000,
  honesty = TRUE,
  seed = 12345
)

# Predict individual treatment effects (CATEs)
predictions <- predict(cf, estimate.variance = TRUE)

# Add predictions to data
results <- data.frame(
  X,
  W = W,
  Y = Y,
  true_tau = tau,
  estimated_tau = predictions$predictions,
  se = sqrt(predictions$variance.estimates)
)

# Compare estimated vs true effects
cor(results$true_tau, results$estimated_tau)
#> [1] 0.89  # High correlation indicates good recovery

# Plot estimated vs true
plot(results$true_tau, results$estimated_tau,
     xlab = "True Treatment Effect",
     ylab = "Estimated Treatment Effect",
     main = "Causal Forest: Estimated vs True CATE")
abline(0, 1, col = "red", lwd = 2)
```

#### Average Treatment Effect (ATE)

```r
# Estimate ATE with confidence interval
ate <- average_treatment_effect(cf, target.sample = "all")
print(ate)
#>   estimate   std.err
#> 1    1.02     0.05

# 95% CI
cat(sprintf("ATE: %.3f [%.3f, %.3f]\n",
            ate[1], ate[1] - 1.96*ate[2], ate[1] + 1.96*ate[2]))
#> ATE: 1.020 [0.922, 1.118]

# True ATE is mean(tau) = 1.0, so well-recovered
```

#### Variable Importance for Heterogeneity

```r
# Which variables drive treatment effect heterogeneity?
var_imp <- variable_importance(cf)
var_imp_df <- data.frame(
  variable = colnames(X),
  importance = as.numeric(var_imp)
) %>%
  arrange(desc(importance))

print(var_imp_df)
#>    variable importance
#> 1        X1      0.412
#> 2        X2      0.198
#> 3        X5      0.082
#> 4        X3      0.075
#> ...

# X1 and X2 correctly identified as most important
# (they are the true HTE drivers)

# Visualize
barplot(var_imp_df$importance,
        names.arg = var_imp_df$variable,
        main = "Variable Importance for Treatment Effect Heterogeneity",
        ylab = "Importance")
```

#### Calibration Test

```r
# Test whether there is meaningful heterogeneity
test_calibration(cf)
#> Best linear fit using forest predictions (on held-out data):
#>
#>                               Estimate Std. Error t value  Pr(>|t|)
#> mean.forest.prediction         1.005     0.048    21.02   < 2e-16 ***
#> differential.forest.prediction 0.987     0.052    19.13   < 2e-16 ***
#>
#> Interpretation:
#> - mean.forest.prediction ~ 1: ATE correctly estimated
#> - differential.forest.prediction ~ 1: Heterogeneity correctly captured
```

#### Examining Conditional Effects

```r
# Predict effects at specific covariate values
X_test <- matrix(0, 5, p)
X_test[, 1] <- c(-2, -1, 0, 1, 2)  # Vary X1
colnames(X_test) <- colnames(X)

predictions_test <- predict(cf, X_test, estimate.variance = TRUE)

# True effect: tau = 1 + 2*X1 + X2, with X2=0
true_test <- 1 + 2 * X_test[, 1]

data.frame(
  X1 = X_test[, 1],
  true_tau = true_test,
  estimated_tau = predictions_test$predictions,
  se = sqrt(predictions_test$variance.estimates)
)
#>   X1 true_tau estimated_tau    se
#> 1 -2       -3         -2.85  0.18
#> 2 -1       -1         -0.92  0.12
#> 3  0        1          1.05  0.09
#> 4  1        3          2.98  0.12
#> 5  2        5          4.91  0.17
```

---

### 3.2 Random Forests

**When to use random forests:**
- Prediction is primary goal (not causal inference)
- Non-linear relationships and interactions expected
- Variable importance ranking needed
- Robust to outliers and scale differences

**Advantages:**
- No assumptions about functional form
- Handles high-dimensional data well
- Built-in cross-validation (OOB error)
- Feature importance measures

```r
library(ranger)

# Use mtcars for regression example
data(mtcars)
str(mtcars)
#> 32 obs, 11 variables
#> mpg: miles per gallon (outcome)
#> predictors: cyl, disp, hp, drat, wt, qsec, vs, am, gear, carb

# Split into training and test sets
set.seed(12345)
train_idx <- sample(1:nrow(mtcars), 24)
train_df <- mtcars[train_idx, ]
test_df <- mtcars[-train_idx, ]
```

#### Regression Random Forest

```r
# Fit random forest for mpg prediction
rf_reg <- ranger(
  mpg ~ .,
  data = train_df,
  num.trees = 500,
  importance = "impurity",
  seed = 12345
)

print(rf_reg)
#> Ranger result
#> Type:                             Regression
#> Number of trees:                  500
#> Sample size:                      24
#> Number of independent variables:  10
#> Mtry:                             3
#> Target node size:                 5
#> OOB prediction error (MSE):       6.82
#> R squared (OOB):                  0.81

# Predict on test set
predictions <- predict(rf_reg, data = test_df)$predictions

# Evaluate
rmse <- sqrt(mean((predictions - test_df$mpg)^2))
cat(sprintf("Test RMSE: %.2f\n", rmse))
#> Test RMSE: 2.45

# Compare predicted vs actual
data.frame(
  actual = test_df$mpg,
  predicted = round(predictions, 1)
)
```

#### Variable Importance

```r
# Extract importance scores
importance_scores <- rf_reg$variable.importance
importance_df <- data.frame(
  variable = names(importance_scores),
  importance = importance_scores
) %>%
  arrange(desc(importance))

print(importance_df)
#>    variable importance
#> 1       wt      131.5
#> 2      cyl       77.3
#> 3     disp       69.8
#> 4       hp       48.2
#> 5     drat       15.1
#> ...

# Visualize
barplot(importance_df$importance,
        names.arg = importance_df$variable,
        las = 2,
        main = "Variable Importance for MPG Prediction",
        ylab = "Importance (Node Impurity)")
```

#### Classification Random Forest

```r
# Use iris for classification
data(iris)
set.seed(12345)
train_idx <- sample(1:nrow(iris), 100)
train_iris <- iris[train_idx, ]
test_iris <- iris[-train_idx, ]

# Fit classification forest
rf_class <- ranger(
  Species ~ .,
  data = train_iris,
  num.trees = 500,
  importance = "impurity",
  probability = TRUE,  # Return class probabilities
  seed = 12345
)

print(rf_class)
#> OOB prediction error: 4.00%

# Predict class probabilities
probs <- predict(rf_class, data = test_iris)$predictions
head(round(probs, 3))
#>      setosa versicolor virginica
#> [1,]  0.998      0.002     0.000
#> [2,]  0.000      0.892     0.108
#> ...

# Predict classes
pred_class <- colnames(probs)[apply(probs, 1, which.max)]

# Confusion matrix
table(Predicted = pred_class, Actual = test_iris$Species)
#>             Actual
#> Predicted    setosa versicolor virginica
#>   setosa         17          0         0
#>   versicolor      0         16         1
#>   virginica       0          1        15

# Accuracy
mean(pred_class == test_iris$Species)
#> [1] 0.96
```

#### Tuning Random Forest Parameters

```r
# Key parameters to tune:
# - num.trees: More is generally better (diminishing returns after ~500)
# - mtry: Number of variables to try at each split
#         Default: sqrt(p) for classification, p/3 for regression
# - min.node.size: Minimum observations in terminal node

# Grid search example
tune_grid <- expand.grid(
  mtry = c(2, 3, 4),
  min.node.size = c(1, 3, 5)
)

results <- lapply(1:nrow(tune_grid), function(i) {
  rf <- ranger(
    mpg ~ .,
    data = train_df,
    num.trees = 500,
    mtry = tune_grid$mtry[i],
    min.node.size = tune_grid$min.node.size[i],
    seed = 12345
  )
  data.frame(
    mtry = tune_grid$mtry[i],
    min.node.size = tune_grid$min.node.size[i],
    oob_mse = rf$prediction.error
  )
})

tune_results <- do.call(rbind, results)
tune_results[order(tune_results$oob_mse), ]
#>   mtry min.node.size oob_mse
#> 4    2             3    6.21  <- Best
#> 1    2             1    6.45
#> 7    2             5    6.58
#> ...
```

---

## 4. Classification Methods

### 4.1 Support Vector Machines (SVM)

**When to use SVM:**
- Binary or multi-class classification
- High-dimensional data (p can exceed n)
- Clear margin of separation expected
- Need non-linear decision boundaries (with kernels)

**Key concepts:**
- Maximizes margin between classes
- Uses kernel trick for non-linear boundaries
- C parameter controls bias-variance tradeoff
- Must scale features for optimal performance

```r
library(caret)
library(e1071)

# Prepare iris data for binary classification
data(iris)
# Focus on distinguishing versicolor vs virginica (harder problem)
iris_binary <- iris[iris$Species != "setosa", ]
iris_binary$Species <- factor(iris_binary$Species)

set.seed(12345)
train_idx <- createDataPartition(iris_binary$Species, p = 0.7, list = FALSE)
train_data <- iris_binary[train_idx, ]
test_data <- iris_binary[-train_idx, ]

# Scale predictors (important for SVM)
preproc <- preProcess(train_data[, 1:4], method = c("center", "scale"))
train_scaled <- predict(preproc, train_data)
test_scaled <- predict(preproc, test_data)
```

#### Linear SVM

```r
# Train linear SVM with cross-validation
ctrl <- trainControl(
  method = "repeatedcv",
  number = 10,
  repeats = 3,
  classProbs = TRUE,
  summaryFunction = twoClassSummary
)

set.seed(12345)
svm_linear <- train(
  Species ~ .,
  data = train_scaled,
  method = "svmLinear",
  trControl = ctrl,
  metric = "ROC",
  tuneGrid = expand.grid(C = c(0.01, 0.1, 1, 10))
)

print(svm_linear)
#> Support Vector Machines with Linear Kernel
#> 70 samples, 4 predictors, 2 classes
#>
#> Resampling: Cross-Validated (10 fold, repeated 3 times)
#>
#>   C     ROC    Sens   Spec
#>   0.01  0.971  0.914  0.943
#>   0.10  0.980  0.943  0.957
#>   1.00  0.979  0.943  0.943  <- Selected
#>   10.00 0.974  0.929  0.929

# Best C value
svm_linear$bestTune
#>   C
#> 3 1

# Test set predictions
pred_linear <- predict(svm_linear, test_scaled)
confusionMatrix(pred_linear, test_scaled$Species)
#> Accuracy: 0.933
#> Sensitivity: 0.933
#> Specificity: 0.933
```

#### Radial Basis Function (RBF) Kernel

```r
# RBF kernel with tuning
set.seed(12345)
svm_rbf <- train(
  Species ~ .,
  data = train_scaled,
  method = "svmRadial",
  trControl = ctrl,
  metric = "ROC",
  tuneLength = 5  # Auto-generate 5 values for sigma and C
)

print(svm_rbf)
#>   sigma  C     ROC    Sens   Spec
#>   0.25   0.25  0.969  0.914  0.943
#>   0.25   0.50  0.976  0.929  0.957
#>   0.25   1.00  0.980  0.943  0.957  <- Selected
#>   0.25   2.00  0.979  0.943  0.943
#>   0.25   4.00  0.974  0.929  0.929

# Compare kernels
pred_rbf <- predict(svm_rbf, test_scaled)
confusionMatrix(pred_rbf, test_scaled$Species)
#> Accuracy: 0.967 (slightly better than linear)
```

#### Interpreting SVM Results

```r
# Get class probabilities
probs <- predict(svm_rbf, test_scaled, type = "prob")
head(probs)
#>   versicolor virginica
#> 1      0.892     0.108
#> 2      0.034     0.966
#> ...

# ROC curve
library(pROC)
roc_obj <- roc(test_scaled$Species, probs$virginica)
plot(roc_obj, main = sprintf("SVM ROC Curve (AUC = %.3f)", auc(roc_obj)))
#> AUC: ~0.98
```

---

### 4.2 Cross-Validation Framework

**Types of cross-validation:**

| Method | Description | Use when |
|--------|-------------|----------|
| k-fold | Split into k parts, rotate test set | Standard choice |
| Repeated k-fold | Multiple k-fold runs | Reduce variance in estimates |
| LOOCV | Leave-one-out | Small datasets |
| Stratified | Maintain class proportions | Imbalanced classes |
| Time series | Preserve temporal order | Time-dependent data |

```r
library(caret)
library(mlbench)

# Load Pima Indians Diabetes dataset
data(PimaIndiansDiabetes2)
pima <- na.omit(PimaIndiansDiabetes2)  # Remove NAs
str(pima)
#> 392 obs, 9 variables
#> diabetes: outcome (pos/neg)

# Check class balance
table(pima$diabetes)
#>  neg  pos
#>  262  130  (imbalanced: 67% negative)
```

#### Basic k-fold Cross-Validation

```r
# 10-fold CV
ctrl_kfold <- trainControl(
  method = "cv",
  number = 10,
  classProbs = TRUE,
  summaryFunction = twoClassSummary,
  savePredictions = "final"
)

# Train logistic regression
set.seed(12345)
model_kfold <- train(
  diabetes ~ .,
  data = pima,
  method = "glm",
  family = "binomial",
  trControl = ctrl_kfold,
  metric = "ROC"
)

print(model_kfold)
#> Generalized Linear Model
#> 392 samples, 8 predictors, 2 classes
#>
#> Resampling: Cross-Validated (10 fold)
#> Summary of sample sizes: 352, 353, 353, 353, ...
#>
#> ROC        Sens       Spec
#> 0.838      0.859      0.654
```

#### Repeated k-fold for Variance Reduction

```r
# 10-fold CV repeated 5 times
ctrl_repeated <- trainControl(
  method = "repeatedcv",
  number = 10,
  repeats = 5,
  classProbs = TRUE,
  summaryFunction = twoClassSummary
)

set.seed(12345)
model_repeated <- train(
  diabetes ~ .,
  data = pima,
  method = "glm",
  family = "binomial",
  trControl = ctrl_repeated,
  metric = "ROC"
)

# More stable estimates (averaged over 50 folds)
print(model_repeated)
#> ROC        Sens       Spec
#> 0.835      0.855      0.661
#> (SE reduced compared to single 10-fold)
```

#### Stratified Sampling for Imbalanced Data

```r
# Ensure class proportions maintained in each fold
ctrl_stratified <- trainControl(
  method = "cv",
  number = 10,
  classProbs = TRUE,
  summaryFunction = twoClassSummary,
  sampling = "up"  # Upsample minority class within folds
)

set.seed(12345)
model_stratified <- train(
  diabetes ~ .,
  data = pima,
  method = "glm",
  family = "binomial",
  trControl = ctrl_stratified,
  metric = "ROC"
)

print(model_stratified)
#> Sensitivity improved (better at detecting positive cases)
```

#### Comparing Multiple Models

```r
# Compare logistic regression, random forest, and SVM
set.seed(12345)
model_glm <- train(diabetes ~ ., data = pima, method = "glm",
                   family = "binomial", trControl = ctrl_repeated, metric = "ROC")

set.seed(12345)
model_rf <- train(diabetes ~ ., data = pima, method = "ranger",
                  trControl = ctrl_repeated, metric = "ROC")

set.seed(12345)
model_svm <- train(diabetes ~ ., data = pima, method = "svmRadial",
                   trControl = ctrl_repeated, metric = "ROC",
                   preProcess = c("center", "scale"))

# Compare results
results <- resamples(list(
  Logistic = model_glm,
  RandomForest = model_rf,
  SVM = model_svm
))

summary(results)
#>              ROC
#>              Mean    SD
#> Logistic     0.835   0.06
#> RandomForest 0.827   0.07
#> SVM          0.829   0.06

# Visualize comparison
bwplot(results, metric = "ROC")

# Statistical test for differences
diff_results <- diff(results)
summary(diff_results)
#> p-values for pairwise comparisons
```

#### Nested Cross-Validation (Avoiding Data Leakage)

```r
# Outer loop: Evaluate model performance
# Inner loop: Tune hyperparameters

# Inner CV for tuning
inner_ctrl <- trainControl(
  method = "cv",
  number = 5,
  classProbs = TRUE,
  summaryFunction = twoClassSummary
)

# Outer CV for evaluation
outer_ctrl <- trainControl(
  method = "cv",
  number = 10,
  classProbs = TRUE,
  summaryFunction = twoClassSummary,
  savePredictions = "final"
)

# This avoids optimistic bias from tuning on same data used for evaluation
set.seed(12345)
nested_model <- train(
  diabetes ~ .,
  data = pima,
  method = "svmRadial",
  trControl = outer_ctrl,
  tuneLength = 5,
  preProcess = c("center", "scale"),
  metric = "ROC"
)
```

---

## 5. Nonparametric Regression

### 5.1 Generalized Additive Models (GAMs)

**When to use GAMs:**
- Relationships may be non-linear but smoothly varying
- Want interpretable effects (not black box)
- Need confidence intervals and hypothesis tests
- Partial dependence on individual predictors matters

**Advantages over linear models:**
- Automatically discover non-linear relationships
- No need to specify polynomial degree
- Penalties prevent overfitting
- Uncertainty quantification built in

```r
library(mgcv)

# Simulate data with known smooth functions
set.seed(12345)
sim_data <- gamSim(1, n = 400, dist = "normal", scale = 2, verbose = FALSE)

# gamSim(1) creates:
# y = f0(x0) + f1(x1) + f2(x2) + f3(x3) + noise
# where f0-f3 are known smooth functions

head(sim_data)
#>          y        x0        x1        x2        x3
#> 1  7.23142  0.515619  0.327731  0.651753  0.893749
#> 2  5.12878  0.276391  0.721562  0.512698  0.298461
#> ...
```

#### Basic GAM with Smooth Terms

```r
# Fit GAM with smooth terms for each predictor
gam_model <- gam(
  y ~ s(x0) + s(x1) + s(x2) + s(x3),
  data = sim_data,
  method = "REML"  # Restricted maximum likelihood for smoothing
)

summary(gam_model)
#> Family: gaussian
#> Link function: identity
#>
#> Parametric coefficients:
#>             Estimate Std. Error t value Pr(>|t|)
#> (Intercept)   7.832      0.100    78.3   <2e-16 ***
#>
#> Approximate significance of smooth terms:
#>         edf Ref.df     F p-value
#> s(x0) 3.72   4.57  33.1  <2e-16 ***
#> s(x1) 2.41   3.01  71.2  <2e-16 ***
#> s(x2) 7.83   8.58  78.5  <2e-16 ***
#> s(x3) 1.00   1.00   0.3    0.59     <- Linear (no smooth needed)
#>
#> R-sq.(adj) = 0.72   Deviance explained = 73.1%
#> -REML = 879.5   Scale est. = 3.98    n = 400

# Interpretation:
# - edf (effective degrees of freedom): Higher = more wiggly
# - edf = 1 suggests linear relationship
# - s(x3) not significant: could simplify model
```

#### Visualizing Smooth Terms

```r
# Plot smooth functions with confidence bands
par(mfrow = c(2, 2))
plot(gam_model, shade = TRUE, pages = 0)

# Each plot shows:
# - Estimated smooth function (solid line)
# - 95% confidence band (shaded)
# - Rug plot showing data density

# Compare to true functions
# s(x0): Should show sine-like curve
# s(x1): Should show exponential-like increase
# s(x2): Should show bimodal pattern
# s(x3): Should be nearly flat (linear)
```

#### Model Diagnostics

```r
# Check model assumptions
par(mfrow = c(2, 2))
gam.check(gam_model)

# Output includes:
# 1. QQ plot of residuals (should be linear)
# 2. Residuals vs fitted (should be random scatter)
# 3. Histogram of residuals (should be normal)
# 4. Response vs fitted (should be linear)

# Also prints basis dimension checks:
# k-index: If < 1, may need more basis functions (higher k)
# p-value: If significant, k may be too low
```

#### Model Comparison and Selection

```r
# Compare nested models using likelihood ratio test
gam_full <- gam(y ~ s(x0) + s(x1) + s(x2) + s(x3), data = sim_data, method = "REML")
gam_reduced <- gam(y ~ s(x0) + s(x1) + s(x2), data = sim_data, method = "REML")

anova(gam_reduced, gam_full, test = "F")
#> Analysis of Deviance Table
#>
#> Model 1: y ~ s(x0) + s(x1) + s(x2)
#> Model 2: y ~ s(x0) + s(x1) + s(x2) + s(x3)
#>   Resid. Df Resid. Dev     Df Deviance     F  Pr(>F)
#> 1    385.1     1583.2
#> 2    384.1     1582.0   1.00    1.189  0.30    0.59
#>
#> Not significant: x3 can be dropped

# Compare models using AIC
AIC(gam_full, gam_reduced)
#>              df      AIC
#> gam_full     16.0   1794.1
#> gam_reduced  15.0   1792.9  <- Lower AIC, simpler model preferred
```

#### Tensor Product Smooths for Interactions

```r
# Model interaction between two continuous predictors
gam_tensor <- gam(
  y ~ te(x0, x1) + s(x2),  # Tensor product smooth for x0*x1
  data = sim_data,
  method = "REML"
)

summary(gam_tensor)

# Visualize interaction surface
vis.gam(gam_tensor,
        view = c("x0", "x1"),
        plot.type = "contour",
        main = "Interaction: x0 and x1")

# Or 3D perspective plot
vis.gam(gam_tensor,
        view = c("x0", "x1"),
        plot.type = "persp",
        theta = 45,
        phi = 30)
```

#### GAM with Binary Outcome

```r
# Simulate binary outcome
set.seed(12345)
n <- 500
x <- runif(n, 0, 10)
prob <- plogis(-2 + 0.5 * sin(x))  # Non-linear probability
y <- rbinom(n, 1, prob)
binary_data <- data.frame(x = x, y = y)

# Fit logistic GAM
gam_logit <- gam(
  y ~ s(x),
  family = binomial(link = "logit"),
  data = binary_data,
  method = "REML"
)

summary(gam_logit)

# Plot on probability scale
plot(gam_logit, trans = plogis, shift = coef(gam_logit)[1],
     shade = TRUE, rug = FALSE,
     ylab = "Probability",
     main = "GAM: Estimated Probability Function")
```

#### Key GAM Options

| Argument | Options | Use |
|----------|---------|-----|
| `s()` | Smooth term | Single predictor smooth |
| `te()` | Tensor product | Interaction of 2+ predictors |
| `ti()` | Tensor interaction | Pure interaction (no main effects) |
| `bs` | `"tp"`, `"cr"`, `"cs"` | Basis type (thin plate, cubic regression) |
| `k` | Integer | Maximum basis dimension |
| `method` | `"REML"`, `"GCV.Cp"` | Smoothing parameter selection |
| `family` | `gaussian()`, `binomial()`, etc. | Response distribution |

---

## 6. Measurement & Scale Construction

Methods for developing and validating psychological and social measures.

### 6.1 Exploratory Factor Analysis (EFA)

**When to use EFA:**
- Developing a new scale with unknown structure
- Exploring dimensionality of item sets
- No strong theory about factor structure
- Reducing many items to fewer latent constructs

**Key decisions:**
- Number of factors (parallel analysis, scree plot)
- Extraction method (principal axis, maximum likelihood)
- Rotation (orthogonal vs oblique)
- Item retention criteria

```r
library(psych)

# Load Big Five Inventory dataset
data(bfi)
str(bfi)
#> 2,800 observations, 28 variables
#> 25 personality items (A1-A5, C1-C5, E1-E5, N1-N5, O1-O5)
#> 3 demographic variables (gender, education, age)

# Extract just the 25 personality items
items <- bfi[, 1:25]

# Check for missing data
colSums(is.na(items))
#> Some missingness; use complete cases for demonstration
items_complete <- na.omit(items)
nrow(items_complete)
#> 2,436 complete cases
```

#### Step 1: Determine Number of Factors

```r
# Parallel analysis (gold standard for factor number)
set.seed(12345)
fa.parallel(items_complete, fa = "fa", n.iter = 100)

# Output plot shows:
# - Actual eigenvalues (solid line)
# - Simulated eigenvalues from random data (dashed)
# - Factors to retain: Where actual > simulated

# Text output:
#> Parallel analysis suggests that the number of factors = 6
#> (actual eigenvalues: 5.2, 2.8, 2.1, 1.5, 1.2, 1.0)

# Also check Kaiser criterion (eigenvalues > 1) and scree plot
# But parallel analysis is more accurate
```

#### Step 2: Check Sampling Adequacy

```r
# Correlation matrix
R <- cor(items_complete, use = "pairwise.complete.obs")

# Kaiser-Meyer-Olkin (KMO) measure
KMO(R)
#> Overall MSA = 0.85
#> Interpretation: > 0.80 is "meritorious"
#>                > 0.90 is "marvelous"
#>                < 0.50 is unacceptable

# Bartlett's test of sphericity
cortest.bartlett(R, n = nrow(items_complete))
#> chi-square = 17523.1, df = 300, p < 0.001
#> Significant: Correlations are not all zero
```

#### Step 3: Extract Factors

```r
# Principal axis factoring with oblimin rotation
# (oblique rotation allows factors to correlate)
set.seed(12345)
fa_result <- fa(
  items_complete,
  nfactors = 5,       # Big Five theory suggests 5
  rotate = "oblimin",
  fm = "pa",          # Principal axis factoring
  scores = "regression"
)

print(fa_result, cut = 0.3, sort = TRUE)
#>
#> Standardized loadings (pattern matrix):
#>      PA1   PA2   PA3   PA4   PA5   h2    u2   com
#> N1  0.81                           0.67  0.33 1.0
#> N2  0.78                           0.63  0.37 1.1
#> N3  0.71                           0.53  0.47 1.1
#> N4  0.62                           0.46  0.54 1.3
#> N5  0.52                           0.36  0.64 1.5
#> E1        0.58                     0.42  0.58 1.3
#> E2        0.72                     0.57  0.43 1.1
#> E3        0.48                     0.44  0.56 1.8
#> ...
#>
#> Factor correlations:
#>      PA1   PA2   PA3   PA4   PA5
#> PA1  1.00
#> PA2 -0.22  1.00
#> PA3  0.28 -0.35  1.00
#> PA4 -0.09  0.19 -0.12  1.00
#> PA5 -0.07  0.17 -0.13  0.11  1.00

# h2 = communality (variance explained by factors)
# u2 = uniqueness (1 - h2)
# Items with h2 < 0.20 may be problematic
```

#### Step 4: Evaluate Solution

```r
# Fit indices
fa_result$RMSEA
#> [1] 0.052  # < 0.06 is good fit

fa_result$TLI
#> [1] 0.89   # > 0.90 is good fit

# Factor loadings criteria:
# - Primary loading > 0.40 (ideally > 0.50)
# - Cross-loadings < 0.30
# - Communality > 0.20

# Identify problematic items
# Low communality
which(fa_result$communalities < 0.20)
# Cross-loading items (loading > 0.30 on multiple factors)
# Check pattern matrix manually
```

#### Step 5: Internal Consistency

```r
# Cronbach's alpha for each factor
# First, identify items per factor based on loadings
neuroticism <- c("N1", "N2", "N3", "N4", "N5")
extraversion <- c("E1", "E2", "E3", "E4", "E5")
openness <- c("O1", "O2", "O3", "O4", "O5")
agreeableness <- c("A1", "A2", "A3", "A4", "A5")
conscientiousness <- c("C1", "C2", "C3", "C4", "C5")

# Calculate alpha for each scale
alpha(items_complete[, neuroticism])
#> raw_alpha = 0.81 (good)

alpha(items_complete[, extraversion])
#> raw_alpha = 0.76 (acceptable)

alpha(items_complete[, openness])
#> raw_alpha = 0.60 (questionable - some items may need revision)

# Full alpha output includes:
# - raw_alpha: Cronbach's alpha
# - std.alpha: Standardized alpha
# - alpha if item dropped: Identifies problematic items
```

#### Computing Factor Scores

```r
# Factor scores are in fa_result$scores
factor_scores <- fa_result$scores
head(factor_scores)
#>        PA1     PA2     PA3     PA4     PA5
#> 1  -0.523   0.124  -0.892   0.341   0.156
#> 2   1.234  -0.456   0.123  -0.234   0.567
#> ...

# Add to original data
items_complete$N_score <- factor_scores[, "PA1"]
items_complete$E_score <- factor_scores[, "PA2"]
# etc.
```

#### Visualizing Factor Structure

```r
# Create factor loading diagram
fa.diagram(fa_result, main = "Big Five Factor Structure")

# Shows:
# - Items connected to their primary factor
# - Loading values on paths
# - Factor correlations (curved arrows)

# For publication-quality output
pdf("factor_diagram.pdf", width = 10, height = 8)
fa.diagram(fa_result,
           cut = 0.3,      # Only show loadings > 0.3
           digits = 2,
           main = "Five-Factor Solution")
dev.off()
```

#### Omega: Better Reliability Than Alpha

Cronbach's alpha assumes all items have equal loadings (tau-equivalence). McDonald's omega relaxes this assumption:

```r
# Calculate omega for a single scale
neuroticism_items <- items_complete[, c("N1", "N2", "N3", "N4", "N5")]

# omega() fits a factor model and computes reliability
omega_result <- omega(neuroticism_items, nfactors = 1, plot = FALSE)

# Key outputs
cat("Omega total:", round(omega_result$omega.tot, 3), "\n")
#> Omega total: 0.822

# For comparison
cat("Alpha:", round(omega_result$alpha, 3), "\n")
#> Alpha: 0.817

# omega.tot >= alpha always (omega is more accurate)
# Large difference suggests unequal loadings

# For multidimensional scales, use omega on full item set
omega_full <- omega(items_complete[, 1:25], nfactors = 5, plot = FALSE)
cat("Omega hierarchical:", round(omega_full$omega_h, 3), "\n")
#> omega_h: Reliability of general factor
#> omega_t: Total reliable variance
```

#### Scale Scoring with scoreItems()

```r
# Define scales by item names
keys <- list(
  neuroticism = c("N1", "N2", "N3", "N4", "N5"),
  extraversion = c("-E1", "-E2", "E3", "E4", "E5"),  # Note: E1, E2 reversed
  openness = c("O1", "-O2", "O3", "O4", "-O5"),
  agreeableness = c("-A1", "A2", "A3", "A4", "A5"),
  conscientiousness = c("C1", "C2", "C3", "-C4", "-C5")
)

# Score all scales at once
scores <- scoreItems(keys, items_complete[, 1:25])

# View reliabilities
print(scores$alpha)
#>      neuroticism extraversion openness agreeableness conscientiousness
#> alpha       0.82         0.76     0.60          0.70              0.73

# Get scale scores
scale_scores <- scores$scores
head(scale_scores)
#>      neuroticism extraversion openness agreeableness conscientiousness
#> [1,]        3.40         3.60     3.80          4.00              3.80
#> [2,]        2.60         2.80     3.20          3.40              4.20
```

---

### 6.2 Confirmatory Factor Analysis (CFA)

**When to use CFA:**
- Testing a pre-specified factor structure
- Validating a scale in new population
- Comparing alternative structures
- Assessing measurement invariance across groups

**CFA vs EFA:**
- EFA: "What is the structure?" (exploratory)
- CFA: "Does this structure fit?" (confirmatory)

```r
library(lavaan)
library(semTools)

# Load classic CFA dataset
data(HolzingerSwineford1939)
hs <- HolzingerSwineford1939

str(hs)
#> 301 observations
#> 9 mental ability tests (x1-x9)
#> From two schools (Pasteur, Grant-White)

head(hs[, c("school", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9")])
```

#### Specifying the CFA Model

```r
# Classic three-factor model
# Visual: x1, x2, x3
# Textual: x4, x5, x6
# Speed: x7, x8, x9

model_3factor <- '
  visual  =~ x1 + x2 + x3
  textual =~ x4 + x5 + x6
  speed   =~ x7 + x8 + x9
'

# Fit the model
fit_3f <- cfa(
  model_3factor,
  data = hs,
  estimator = "MLM"  # Robust to non-normality
)

summary(fit_3f, fit.measures = TRUE, standardized = TRUE)
```

#### Interpreting CFA Output

```r
# Model Fit Indices:
# =================
# Chi-square (test of exact fit):
#   chi-sq = 85.306, df = 24, p < 0.001
#   Significant p: Model doesn't fit perfectly
#   But chi-square is sensitive to sample size

# CFI (Comparative Fit Index):
#   0.931 (> 0.90 acceptable, > 0.95 good)

# TLI (Tucker-Lewis Index):
#   0.896 (> 0.90 acceptable, > 0.95 good)

# RMSEA (Root Mean Square Error of Approximation):
#   0.092, 90% CI [0.071, 0.114]
#   < 0.06 good, < 0.08 acceptable, > 0.10 poor

# SRMR (Standardized Root Mean Residual):
#   0.065 (< 0.08 good)

# Factor Loadings (Standardized):
# ==============================
#                    Estimate  Std.Err  z-value  P(>|z|)   Std.all
# visual =~
#   x1                  1.000                               0.772
#   x2                  0.554    0.100    5.554    0.000    0.424
#   x3                  0.729    0.109    6.685    0.000    0.581
#
# Std.all = standardized loadings
# Should be > 0.40, ideally > 0.70
```

#### Model Comparison

```r
# Compare 3-factor vs 1-factor model
model_1factor <- '
  general =~ x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9
'

fit_1f <- cfa(model_1factor, data = hs, estimator = "MLM")

# Compare fit
summary(fit_1f, fit.measures = TRUE)
#> CFI = 0.697, RMSEA = 0.175
#> Much worse fit than 3-factor

# Formal comparison (Satorra-Bentler scaled chi-square difference)
lavTestLRT(fit_3f, fit_1f, method = "satorra.bentler.2010")
#>
#> Chi-Squared Difference Test
#>
#>          Df AIC BIC  Chisq Chisq diff Df diff Pr(>Chisq)
#> fit_3f   24             85.306
#> fit_1f   27            280.170   194.86       3     <2e-16 ***
#>
#> Significant: 3-factor model fits significantly better
```

#### Reliability from CFA

```r
# Omega reliability (preferred over alpha for CFA)
compRelSEM(fit_3f)
#>  visual textual   speed
#>   0.601   0.885   0.689

#> omega > 0.70 generally acceptable
#> textual factor has best reliability
```

#### Measurement Invariance Testing

```r
# Test whether factor structure is equivalent across schools

# Step 1: Configural invariance (same structure)
fit_config <- cfa(model_3factor, data = hs, group = "school")

# Step 2: Metric invariance (equal loadings)
fit_metric <- cfa(model_3factor, data = hs, group = "school",
                  group.equal = "loadings")

# Step 3: Scalar invariance (equal intercepts)
fit_scalar <- cfa(model_3factor, data = hs, group = "school",
                  group.equal = c("loadings", "intercepts"))

# Compare nested models
lavTestLRT(fit_config, fit_metric, fit_scalar)
#>
#>             Df    AIC    BIC  Chisq Chisq diff Df diff Pr(>Chisq)
#> fit_config  48 7484.4 7706.8 115.85
#> fit_metric  54 7480.6 7680.8 124.04     8.19       6      0.224
#> fit_scalar  60 7484.4 7662.4 139.82    15.77       6      0.015 *
#>
#> Interpretation:
#> - Config -> Metric: p = 0.224 (metric invariance holds)
#> - Metric -> Scalar: p = 0.015 (scalar invariance may not hold)
#> - Can compare factor means across schools with metric invariance
#> - Cannot compare observed means without scalar invariance
```

#### Modification Indices

```r
# Identify potential model improvements
modindices(fit_3f, sort = TRUE, minimum.value = 10)
#>
#>     lhs op rhs    mi    epc sepc.all
#> 1    x7 ~~  x8 34.15  0.536    0.488
#> 2    x4 ~~  x6 10.23  0.182    0.163
#>
#> x7 and x8 residuals may be correlated
#> Consider adding: x7 ~~ x8 to model
#> But only if theoretically justified!
```

---

### 6.3 Item Response Theory (IRT)

**When to use IRT:**
- Developing assessments or tests
- Items vary in difficulty and discrimination
- Need item-level diagnostics
- Want ability estimates on common scale
- Adaptive testing design

**IRT vs Factor Analysis:**
- FA focuses on inter-item correlations
- IRT models probability of response as function of latent trait
- IRT provides item-specific parameters (difficulty, discrimination)

```r
library(mirt)

# Simulate graded response data (5-point Likert scale)
set.seed(12345)

# Generate 500 respondents, 10 items
# Items vary in difficulty and discrimination
a <- c(1.5, 1.2, 0.8, 1.0, 1.3, 0.9, 1.1, 1.4, 0.7, 1.6)  # Discrimination
d <- matrix(c(
  2.0, 1.0, -0.5, -1.5,  # Item 1 thresholds
  1.5, 0.5, -0.5, -1.0,  # Item 2
  2.5, 1.5,  0.0, -1.0,  # Item 3
  1.0, 0.0, -1.0, -2.0,  # Item 4
  2.0, 1.0,  0.0, -1.5,  # Item 5
  1.5, 0.5, -0.5, -1.5,  # Item 6
  2.5, 1.0, -0.5, -2.0,  # Item 7
  1.0, 0.5, -0.5, -1.0,  # Item 8
  3.0, 1.5,  0.5, -0.5,  # Item 9 (harder item)
  1.5, 0.5, -1.0, -2.0   # Item 10
), ncol = 4, byrow = TRUE)

# Simulate responses
sim_data <- simdata(
  a = a,
  d = d,
  N = 500,
  itemtype = "graded"
)

# Convert to data frame
irt_data <- as.data.frame(sim_data)
names(irt_data) <- paste0("Item", 1:10)
head(irt_data)
#>   Item1 Item2 Item3 Item4 Item5 Item6 Item7 Item8 Item9 Item10
#> 1     4     3     4     4     4     3     4     3     3      4
#> 2     2     2     1     3     2     2     2     2     1      3
#> ...
```

#### Fitting the Graded Response Model

```r
# Fit unidimensional graded response model
irt_model <- mirt(
  data = irt_data,
  model = 1,              # Unidimensional
  itemtype = "graded",
  verbose = FALSE
)

summary(irt_model)
#> Unidimensional model with 10 items
#> Factor loadings (F1) and h2 (communality)
```

#### Item Parameters

```r
# Extract item parameters
coef(irt_model, IRTpars = TRUE, simplify = TRUE)
#>
#> $items
#>         a      b1     b2     b3     b4
#> Item1  1.52  -1.32  -0.65   0.32   0.98
#> Item2  1.18  -1.25  -0.42   0.42   0.84
#> ...
#>
#> a = discrimination (slope)
#>     Higher = better at distinguishing ability levels
#>     > 1.0 is good, > 1.5 is very good
#>
#> b1-b4 = threshold parameters (difficulty)
#>     Location on theta scale where P(X >= k) = 0.5
#>     b1 < b2 < b3 < b4 (ordered thresholds)

# Summary table
item_params <- coef(irt_model, IRTpars = TRUE, simplify = TRUE)$items
round(item_params, 2)
```

#### Item Information Curves

```r
# Item information shows where each item is most informative
# Plot all item information curves (using base mirt plotting)
plot(irt_model, type = "infotrace", which.items = 1:5)

# Items with higher discrimination have taller, narrower curves
# Peak location indicates where item is most useful

# Numerical: Area under information curve
for (i in 1:10) {
  info <- areainfo(irt_model, c(-4, 4), which.items = i)
  cat(sprintf("Item %d: %.2f\n", i, info$Info))
}
#> Item 1: 3.82
#> Item 2: 2.45
#> ...
#> Items with higher discrimination contribute more information
```

#### Test Information Curve

```r
# Total test information across theta range
plot(irt_model, type = "info")

# Test is most informative around theta = 0 (average ability)
# Less information at extremes

# Where does the test measure well?
info_total <- areainfo(irt_model, c(-2, 2))  # Middle range
info_extremes <- areainfo(irt_model, c(-4, -2))  # Low ability

cat(sprintf("Information in [-2, 2]: %.1f\n", info_total$Info))
cat(sprintf("Information in [-4, -2]: %.1f\n", info_extremes$Info))
```

#### Person Ability Estimates

```r
# Extract theta (ability) estimates
theta_estimates <- fscores(irt_model, method = "EAP")
head(theta_estimates)
#>          F1
#> [1,]  1.234
#> [2,] -0.567
#> ...

# Add to data
irt_data$theta <- theta_estimates[, 1]

# Summary of ability distribution
summary(irt_data$theta)
#>    Min. 1st Qu.  Median    Mean 3rd Qu.    Max.
#>  -2.89   -0.67   -0.02    0.00    0.70    2.51
hist(irt_data$theta, main = "Distribution of Ability Estimates",
     xlab = "Theta")
```

#### Item Selection for Short Forms

```r
# Compare information retained with fewer items
full_info <- areainfo(irt_model, c(-3, 3), which.items = 1:10)

# Select best 5 items based on discrimination
best_items <- order(item_params[, "a"], decreasing = TRUE)[1:5]
short_info <- areainfo(irt_model, c(-3, 3), which.items = best_items)

cat(sprintf("Full test (10 items): %.1f information\n", full_info$Info))
cat(sprintf("Short form (5 items): %.1f information (%.0f%%)\n",
            short_info$Info, 100 * short_info$Info / full_info$Info))

#> Full test (10 items): 24.5 information
#> Short form (5 items): 15.8 information (64%)
#> 5 best items retain 64% of information
```

#### Using Real Test Data: LSAT6

The `LSAT6` dataset contains responses to 5 items from the Law School Admission Test:

```r
# Load LSAT6 data (frequency-weighted format)
data(LSAT6)
head(LSAT6)
#>   Item_1 Item_2 Item_3 Item_4 Item_5 Freq
#> 1      0      0      0      0      0    3
#> 2      0      0      0      0      1    6
#> ...

# Expand to individual responses
items <- LSAT6[, 1:5]
freq <- LSAT6$Freq
lsat_data <- items[rep(1:nrow(items), freq), ]
cat("Sample size:", nrow(lsat_data), "\n")
#> Sample size: 1000

# Fit 2PL model (dichotomous items)
lsat_model <- mirt(lsat_data, model = 1, itemtype = "2PL", verbose = FALSE)

# Item parameters
coef(lsat_model, IRTpars = TRUE, simplify = TRUE)$items
#>           a      b g u
#> Item_1 0.83  -3.36 0 1
#> Item_2 0.72  -1.37 0 1
#> Item_3 0.89  -0.28 0 1
#> Item_4 0.69  -1.87 0 1
#> Item_5 0.66  -3.12 0 1

# Interpretation:
#> - Item_3 has highest discrimination (a = 0.89)
#> - Item_1 is easiest (b = -3.36, most negative)
#> - Item_3 is hardest (b = -0.28, closest to zero)
```

#### Item Fit Diagnostics

Check whether items fit the assumed IRT model:

```r
# Item fit using S-X2 statistic (Orlando & Thissen, 2000)
item_fit <- itemfit(lsat_model)
print(round(item_fit[, c("S_X2", "df.S_X2", "p.S_X2")], 3))

#>        S_X2 df.S_X2 p.S_X2
#> Item_1 0.45       2  0.799
#> Item_2 1.69       2  0.429
#> Item_3 0.67       1  0.415
#> Item_4 0.18       2  0.916
#> Item_5 0.11       2  0.946

# Interpretation:
#> - p > 0.05: Item fits the model (all items fit here)
#> - p < 0.05: Item may not fit; investigate further

# Alternative: Zh statistic for person fit
person_fit <- personfit(lsat_model)
#> Zh < -2 suggests aberrant response pattern
```

#### Model Fit Statistics

Assess overall model fit:

```r
# M2 statistic (Maydeu-Olivares & Joe, 2006)
m2_fit <- M2(lsat_model)

cat("Model fit statistics:\n")
cat("  M2 =", round(m2_fit$M2, 2),
    ", df =", m2_fit$df,
    ", p =", round(m2_fit$p, 4), "\n")
cat("  RMSEA =", round(m2_fit$RMSEA, 3),
    ", 95% CI [", round(m2_fit$RMSEA_5, 3), ",",
    round(m2_fit$RMSEA_95, 3), "]\n")
cat("  SRMSR =", round(m2_fit$SRMSR, 3), "\n")

# Example output:
#> Model fit statistics:
#>   M2 = 4.74 , df = 5 , p = 0.4487
#>   RMSEA = 0 , 95% CI [ 0 , 0.058 ]
#>   SRMSR = 0.029

# Interpretation:
#> - p > 0.05: Model fits well
#> - RMSEA < 0.05: Good fit
#> - SRMSR < 0.05: Good fit

# Compare models (e.g., 1PL vs 2PL)
lsat_1pl <- mirt(lsat_data, model = 1, itemtype = "Rasch", verbose = FALSE)
anova(lsat_1pl, lsat_model)
#> Significant p: 2PL fits better than 1PL
```

---

### 6.4 Reliability Assessment

**Types of reliability:**
- Internal consistency: Do items measure same construct?
- Test-retest: Stability over time
- Inter-rater: Agreement between raters

```r
library(psych)

# Create simulated test-retest data
set.seed(12345)
n <- 100

# True scores
true_score <- rnorm(n, mean = 50, sd = 10)

# Three measurement occasions with error
time1 <- true_score + rnorm(n, sd = 5)
time2 <- true_score + rnorm(n, sd = 5)
time3 <- true_score + rnorm(n, sd = 5)

retest_data <- data.frame(
  T1 = time1,
  T2 = time2,
  T3 = time3
)

head(retest_data)
#>        T1     T2     T3
#> 1  52.34  54.21  51.89
#> 2  45.67  44.23  46.12
#> ...
```

#### Intraclass Correlations (ICC)

**Note:** The `ICC()` function in psych requires the `lme4` package for some calculations. Make sure it's installed.

```r
# ICC for test-retest reliability
icc_results <- ICC(retest_data)
print(icc_results)
#>
#> Intraclass correlation coefficients
#>                          type  ICC   F df1 df2       p lower bound upper bound
#> Single_raters_absolute   ICC1 0.75 10.1  99 200 < 0.001        0.67        0.82
#> Single_random_raters     ICC2 0.76 10.3  99 198 < 0.001        0.68        0.83
#> Single_fixed_raters      ICC3 0.76 10.3  99 198 < 0.001        0.68        0.83
#> Average_raters_absolute  ICC1k 0.90 10.1  99 200 < 0.001        0.86        0.93
#> Average_random_raters    ICC2k 0.90 10.3  99 198 < 0.001        0.87        0.94
#> Average_fixed_raters     ICC3k 0.91 10.3  99 198 < 0.001        0.87        0.94

# Interpretation:
#> ICC1: One-way random effects (each subject rated by different raters)
#> ICC2: Two-way random effects, absolute agreement
#> ICC3: Two-way mixed effects, consistency
#>
#> For test-retest, use ICC2 (two-way, absolute agreement)
#> 0.75 = "moderate" to "good" reliability
#>
#> Guidelines:
#> < 0.50 = poor
#> 0.50-0.75 = moderate
#> 0.75-0.90 = good
#> > 0.90 = excellent
```

#### Heise Reliability (Three-Wave)

```r
# Heise (1969) method for three-wave reliability
# Adjusts for systematic change over time

cors <- cor(retest_data)
print(round(cors, 3))
#>        T1    T2    T3
#> T1  1.000 0.761 0.750
#> T2  0.761 1.000 0.768
#> T3  0.750 0.768 1.000

# Heise reliability formula:
# reliability = r(T1,T2) * r(T2,T3) / r(T1,T3)
heise_reliability <- cors["T1", "T2"] * cors["T2", "T3"] / cors["T1", "T3"]
cat(sprintf("Heise reliability estimate: %.3f\n", heise_reliability))
#> Heise reliability estimate: 0.779

# This estimates true score reliability
# Accounting for measurement error AND true change
```

#### Cronbach's Alpha with Detailed Diagnostics

```r
# Use BFI data for internal consistency example
data(bfi)
neuroticism <- bfi[, c("N1", "N2", "N3", "N4", "N5")]
neuroticism <- na.omit(neuroticism)

alpha_result <- alpha(neuroticism)
print(alpha_result)
#>
#> Reliability analysis
#> raw_alpha std.alpha G6(smc) average_r   S/N    ase mean   sd median_r
#>      0.81      0.82    0.81      0.48  4.6  0.006  3.0  1.3     0.47
#>
#> Reliability if an item is dropped:
#>    raw_alpha std.alpha G6(smc) average_r  S/N alpha se  var.r med.r
#> N1      0.76      0.77    0.74      0.46  3.3    0.008 0.0091  0.46
#> N2      0.77      0.78    0.76      0.47  3.5    0.007 0.0057  0.46
#> N3      0.80      0.80    0.78      0.50  4.1    0.006 0.0064  0.49
#> N4      0.79      0.80    0.78      0.50  4.0    0.007 0.0047  0.50
#> N5      0.81      0.82    0.79      0.53  4.5    0.006 0.0019  0.53
#>
#> Item statistics:
#>       n  raw.r std.r  r.cor r.drop mean  sd
#> N1 2769  0.82  0.81  0.77   0.68  2.9 1.6
#> N2 2771  0.80  0.79  0.74   0.65  3.5 1.5
#> N3 2767  0.71  0.73  0.62   0.55  3.2 1.6
#> N4 2765  0.73  0.74  0.64   0.57  3.2 1.6
#> N5 2771  0.64  0.66  0.53   0.47  3.0 1.6

# Interpretation:
#> - raw_alpha = 0.81 (good internal consistency)
#> - All items contribute positively (alpha doesn't improve if dropped)
#> - r.drop = corrected item-total correlation (should be > 0.30)
```

#### McDonald's Omega (Preferred to Alpha)

```r
# Omega handles items with different loadings better than alpha
omega_result <- omega(neuroticism, nfactors = 1)

print(omega_result)
#> Omega
#> omega_h   omega_t
#>   0.82      0.82
#>
#> omega_h = omega hierarchical (general factor)
#> omega_t = omega total
#> Generally similar to alpha for unidimensional scales
#> More accurate when items have unequal loadings
```

---

## Troubleshooting Common Issues

### Sentiment Lexicons Not Available

The sentiment lexicons (AFINN, Bing, NRC) require a one-time download:

```r
# This will prompt to download the lexicon
library(tidytext)
library(textdata)

# First time only - will prompt for download
afinn <- get_sentiments("afinn")  # Downloads AFINN lexicon
bing <- get_sentiments("bing")    # Downloads Bing lexicon
nrc <- get_sentiments("nrc")      # Downloads NRC lexicon
```

### ICC Function Errors

The `ICC()` function may require the `lme4` package:

```r
# Install if not present
install.packages("lme4")
library(psych)
library(lme4)  # Load before using ICC

# Now ICC should work
ICC(retest_data)
```

### Memory Issues with Large Topic Models

For large corpora, reduce memory usage:

```r
# Use VEM instead of Gibbs for large datasets
lda_model <- LDA(dtm, k = 10, method = "VEM")

# Or reduce vocabulary first
dtm_sparse <- removeSparseTerms(dtm, sparse = 0.95)
```

### Caret Warnings About Factors

When using caret with factor outcomes, ensure factor levels are valid R names:

```r
# This may cause issues
levels(data$outcome)
#> [1] "0" "1"

# Fix by renaming levels
data$outcome <- factor(data$outcome, labels = c("No", "Yes"))
```
