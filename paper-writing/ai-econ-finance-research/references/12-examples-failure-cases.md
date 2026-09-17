# Examples And Failure Cases

Use this to calibrate judgment.

## Failure Patterns

| Failure | Why it looks plausible | How to catch it |
| --- | --- | --- |
| fake citation | title sounds real | DOI/journal page check |
| wrong Stata/R/Python code that runs | no error message | toy-data known-answer test |
| wrong DiD interpretation | event-study plot looks clean | estimator/timing/heterogeneity check |
| finance look-ahead bias | variable seems standard | verify formation date and data availability |
| survivorship bias | sample loads cleanly | check delisting and inactive firms |
| LLM text measure drift | labels look consistent | model/version/prompt sensitivity check |
| overclaiming slides | story is clear | claim-to-evidence map |
| AI-written response letter | tone is polished | verify manuscript changes match response |

## Worked-Example Pattern

For any example, produce:

1. research task;
2. skill used;
3. user input;
4. good AI output;
5. bad AI output;
6. what researcher verifies;
7. final safer output.

## Copy-Ready Instruction

```text
Act as a failure-case reviewer for an AI-assisted economics/finance research workflow.

First ask what AI output, code, literature claim, method paragraph, slide, or data workflow I want to evaluate.

Identify what could be wrong even if it sounds plausible. Explain why the error is tempting. Give a concrete verification test. Rewrite the output into a safer version only after stating what must be checked.
```
