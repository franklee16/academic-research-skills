# Literature and DOI Guide

Use this file when the user needs citations, DOI, literature grounding, or a referee-facing explanation. Do not dump all references into the paper. Select only the methods actually used.

## Baseline and Censored Outcomes

- Tobin, James. 1958. "Estimation of Relationships for Limited Dependent Variables." *Econometrica*, 26(1): 24-36. DOI: `10.2307/1907382`.
  - Use when justifying Tobit for censored or limited dependent variables.

## Instrumental Variables and Weak-IV Diagnostics

- Sargan, J. D. 1958. "The Estimation of Economic Relationships using Instrumental Variables." *Econometrica*, 26(3): 393-415. DOI: `10.2307/1907619`.
  - Use for classical IV and overidentifying restriction logic.

- Hansen, Lars Peter. 1982. "Large Sample Properties of Generalized Method of Moments Estimators." *Econometrica*, 50(4): 1029-1054. DOI: `10.2307/1912775`.
  - Use for GMM/Hansen overidentification background.

- Bound, John, David A. Jaeger, and Regina M. Baker. 1995. "Problems with Instrumental Variables Estimation when the Correlation between the Instruments and the Endogenous Explanatory Variable is Weak." *Journal of the American Statistical Association*, 90(430): 443-450. DOI: `10.1080/01621459.1995.10476536`.
  - Use when explaining why first-stage strength must be reported.

- Staiger, Douglas, and James H. Stock. 1997. "Instrumental Variables Regression with Weak Instruments." *Econometrica*, 65(3): 557-586. DOI: `10.2307/2171753`.
  - Use when discussing weak-IV risks, finite-sample bias, LIML, and first-stage diagnostics.

- Stock, James H., and Jonathan H. Wright. 2000. "GMM with Weak Identification." *Econometrica*, 68(5): 1055-1096. DOI: `10.1111/1468-0262.00151`.
  - Use for weak-identification robust GMM tests and confidence sets.

- Kleibergen, Frank, and Richard Paap. 2006. "Generalized Reduced Rank Tests Using the Singular Value Decomposition." *Journal of Econometrics*, 133(1): 97-126. DOI: `10.1016/j.jeconom.2005.02.011`.
  - Use when reporting Kleibergen-Paap rk Wald F, underidentification, or robust weak-IV diagnostics.

## Selection and Omitted Variables

- Heckman, James J. 1979. "Sample Selection Bias as a Specification Error." *Econometrica*, 47(1): 153-161. DOI: `10.2307/1912352`.
  - Use only when there is a real sample-selection process where the outcome is observed for selected units.

- Oster, Emily. 2019. "Unobservable Selection and Coefficient Stability: Theory and Evidence." *Journal of Business & Economic Statistics*, 37(2): 187-204. DOI: `10.1080/07350015.2016.1227711`.
  - Use for coefficient-stability sensitivity analysis with `beta_short`, `R_short`, `beta_full`, `R_full`, `Rmax`, and `delta`.

## Many-IV and Invalid-IV Methods

- Lin, Yiqi, Frank Windmeijer, Xinyuan Song, and Qingliang Fan. 2024. "On the Instrumental Variable Estimation with Many Weak and Invalid Instruments." *Journal of the Royal Statistical Society: Series B*, 86(4): 1068-1088. DOI: `10.1093/jrsssb/qkae025`.
  - Use when a genuine many-candidate-IV setting exists and the user wants WIT-style screening or many weak/invalid IV discussion.

- Carl, David, Corinne Emmenegger, Peter Bühlmann, and Zijian Guo. 2025. "TSCI: Two Stage Curvature Identification for Causal Inference with Invalid Instruments in R." *Journal of Statistical Software*, 114(7). DOI: `10.18637/jss.v114.i07`.
  - Use when testing whether TSCI is applicable. Explain that TSCI estimates treatment effects with invalid instruments by modeling nonlinear treatment structure and projecting out violation space; it is not a simple IV-strengthening or averaging device.

## Citation Selection Rules

- Cite Tobin (1958) only when the outcome model is Tobit or limited dependent variable.
- Cite Bound et al. (1995), Staiger and Stock (1997), Stock and Wright (2000), and Kleibergen and Paap (2006) when weak-IV diagnostics are central.
- Cite Oster (2019) only for coefficient stability, not as a generic robustness synonym.
- Cite Heckman (1979) only when the selection mechanism is substantively appropriate.
- Cite Lin et al. (2024) or Carl et al. (2025) only when the method is actually implemented or explicitly discussed as not applicable.
