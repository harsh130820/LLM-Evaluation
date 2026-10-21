# Repository Validation & LLM Bug-Fix Evaluation — Portfolio Sample

A compact, reproducible case study demonstrating a workflow for validating repositories used in software-engineering and LLM bug-fixing evaluations.

> **Transparency note:** This is an authored portfolio fixture. It is not an analysis of a real upstream GitHub issue, not a contribution to an existing open-source project, and not evidence of running an LLM benchmark. The issue, baseline implementation, tests, and reference fix were created specifically to demonstrate the workflow.

## What this sample demonstrates

- **Issue triage:** a concise report with severity/priority rationale, reproducible steps, expected behavior, acceptance criteria, and non-goals.
- **Reproducible setup:** Python packaging, bounded test dependency, Docker targets, Compose configuration, and CI workflow.
- **Test-quality assessment:** review of existing coverage, identification of a contract gap, and focused regression tests.
- **Bug reproduction and repair:** a baseline that reproduces the issue and a patch/reference implementation that fixes it.
- **LLM evaluation design:** a controlled prompt, test sequence, 100-point rubric, failure conditions, and a scorecard template.
- **Research communication:** a findings report that distinguishes observed fixture behavior from claims that have not been measured.

## Case summary

`retrykit.compute_delay()` supports local exponential backoff and HTTP `Retry-After` headers. The baseline caps exponential delays but returns a valid server-supplied delay without applying `max_delay`. The added regression tests show that numeric and HTTP-date values can exceed the configured cap.

## Quick start

Python 3.11+ is required.

```bash
python -m venv .venv
# Activate the virtual environment for your operating system, then:
python -m pip install -e '.[test]'
pytest -q tests
```

The baseline tests should pass. To reproduce the reported bug:

```bash
pytest -q evaluation
```

The issue-specific suite is expected to report two failures on the baseline and two passing control tests. Apply the proposed patch in a clean checkout:

```bash
git apply patches/fix-retry-after-cap.patch
pytest -q tests evaluation
```

All tests should pass after the patch.

## Run it with Docker

```bash
docker build --target baseline -t retrykit-demo:baseline .
docker run --rm retrykit-demo:baseline

docker build --target fixed -t retrykit-demo:fixed .
docker run --rm retrykit-demo:fixed
```

The `baseline` target runs the existing tests. The `fixed` target installs the reference implementation and runs both test directories. Docker is optional; the local commands above are enough to reproduce the issue.

## Repository map

```text
.
├── src/retrykit/                 # Baseline implementation (contains the defect)
├── tests/                        # Existing baseline unit tests
├── evaluation/                   # Issue-specific regression tests
├── solutions/backoff.py           # Reference fixed implementation
├── patches/fix-retry-after-cap.patch
├── docs/
│   ├── issue-triage.md
│   ├── reproducibility.md
│   ├── test-quality-review.md
│   ├── llm-evaluation-protocol.md
│   ├── findings-report.md
│   ├── reproducibility.md
│   ├── publish-to-github.md
│   └── evaluation-scorecard.csv
├── Dockerfile
├── compose.yaml
└── .github/workflows/tests.yml
```

## Validation status

Observed test counts and limitations are recorded in [`docs/findings-report.md`](docs/findings-report.md). The baseline has 12 passing unit tests; the issue-specific tests expose two expected failures before the fix; the full suite passes all 16 tests after applying the reference patch. Docker was not built in the authoring environment.

## Evaluation notes

The scorecard and protocol are designed for evaluating model-generated patches. No model has been evaluated in this sample, so the scorecard is intentionally blank and no model success rate is claimed. For an actual model trial, create a task-only copy without `solutions/` and `patches/` so the reference answer is not visible to the model.

## Suggested resume entry

**Repository Validation & LLM Bug-Fix Evaluation — Portfolio Project**

- Built a reproducible Python repository fixture with a deterministic bug report, baseline tests, issue-specific regression tests, and a reference fix patch.
- Reviewed unit-test coverage and identified a missing contract assertion across numeric and HTTP-date retry headers.
- Added Docker-based baseline/fixed test targets and CI checks; documented a model-evaluation protocol with a 100-point rubric.

Use this entry after you have personally run the setup and can explain each file. Describe it as a portfolio project, not a paid engagement or an upstream open-source contribution.

## License

MIT for the authored sample materials. This license does not imply that any external project or third-party code is included.
