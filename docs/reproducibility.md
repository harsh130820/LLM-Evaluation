# Reproducible environment and runbook

## Requirements

- Python 3.11 or newer
- `pip`
- Optional: Docker with Docker Compose

The package has no runtime dependencies. Pytest is the only test dependency and is version-bounded in `pyproject.toml`.

## Local setup

From the repository root:

```bash
python -m venv .venv
```

Activate the environment, then run:

```bash
python -m pip install --upgrade pip
python -m pip install -e '.[test]'
pytest -q tests
```

The baseline suite should pass. It captures the behavior already covered before the issue-specific tests were added.

## Reproduce the defect

```bash
pytest -q evaluation
```

On the baseline implementation, two tests should fail: the numeric and HTTP-date forms both exceed `max_delay`. The other two regression tests should pass. Exact pytest formatting can vary by version.

## Apply the candidate fix

Use a clean checkout, then run:

```bash
git apply patches/fix-retry-after-cap.patch
pytest -q tests evaluation
```

The full suite should pass. If the patch was already applied, `git apply` will report that it cannot apply; inspect the current diff instead of forcing it.

## Docker

Baseline test suite:

```bash
docker build --target baseline -t retrykit-demo:baseline .
docker run --rm retrykit-demo:baseline
```

Fixed full suite:

```bash
docker build --target fixed -t retrykit-demo:fixed .
docker run --rm retrykit-demo:fixed
```

The `fixed` Docker target installs `solutions/backoff.py` over the baseline module and executes both test folders. This preserves the baseline source for issue reproduction while making the passing fixed environment reproducible.

## Environment assumptions and limitations

- Tests are offline and deterministic; no external API, credential, or service is needed.
- The HTTP-date regression test injects `now` rather than depending on the machine clock.
- This fixture has one Python package and does not model native libraries, databases, or multi-service deployments.
- The Docker image uses a floating patch release within the `python:3.12-slim` family. For archival-grade reproducibility, pin the image by digest and lock all transitive packages.

## Validation record

See [`findings-report.md`](findings-report.md) for the observed local test counts, including the two expected failures on the baseline and the 16 passing tests after applying the fix. Docker and editable package installation were not verified in the authoring environment.
