# LLM bug-fix evaluation protocol

## Objective

Evaluate whether a model can diagnose and repair the retry-delay cap defect without breaking existing behavior or weakening the tests.

## Task prompt to give a model

> Inspect the repository and issue report. Reproduce the reported behavior, identify the root cause, make the smallest maintainable fix, and add or retain regression tests. Do not change the public API. Report the files changed, why the fix is correct, and the test commands/results. Do not claim tests passed unless you ran them.

## Controlled setup

- Start each candidate from a clean copy of the baseline revision.
- Use the same Python version and dependency installation for every model.
- Give every model the same issue report and repository files.
- Run baseline tests first, then issue-specific tests, then the full suite after the candidate patch.
- Do not provide `solutions/backoff.py` or `patches/fix-retry-after-cap.patch` to the model under test; those files are the reference answer for the human evaluator. For a true benchmark run, create a task-only copy without those reference artifacts.
- Preserve each model's raw patch, logs, and final explanation.

## Test sequence

1. `pytest -q tests` — baseline health check.
2. `pytest -q evaluation` — confirm the issue is reproduced before changes.
3. Apply the model-generated patch to a clean copy.
4. `pytest -q tests evaluation` — regression and compatibility check.
5. Review the diff for scope creep, unnecessary dependencies, removed tests, or altered assertions.

## Scoring rubric (100 points)

| Dimension | Points | Full-credit evidence |
|---|---:|---|
| Root-cause diagnosis | 20 | Identifies uncapped server-delay return for both input formats |
| Functional correctness | 25 | Caps both values, preserves values below cap, leaves fallback behavior intact |
| Test quality | 20 | Adds meaningful regression coverage for numeric and HTTP-date values; tests are deterministic |
| Regression safety | 15 | Existing tests pass; no public API or unrelated behavior changes |
| Reproducibility | 10 | Gives exact commands and truthful test outcomes |
| Explanation / patch quality | 10 | Focused diff and a clear description of the invariant being enforced |

## Failure conditions / deductions

- Removing or weakening an assertion to make the suite green: no credit for the affected test-quality portion.
- Hard-coding the sample values (such as 120 or 30) instead of using `max_delay`: functional correctness credit is lost.
- Fixing only numeric headers or only HTTP dates: partial functional credit.
- Making the tests depend on current wall-clock time or sleeping: deduct reproducibility points.
- Introducing an unrelated dependency or broad refactor without need: deduct patch-quality points.
- Claiming a test passed without execution evidence: reproducibility and reporting deductions.

## Important limitation

This is a single, small, authored fixture. It demonstrates an evaluation workflow but does not establish general model performance. Reliable model comparisons need multiple tasks, repeated runs where model output is stochastic, a fixed environment, and consistent grading.
