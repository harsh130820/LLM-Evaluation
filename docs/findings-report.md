# Findings report: Retry-After cap case study

## Executive summary

The baseline implementation caps exponential backoff but returns valid server-provided `Retry-After` values without enforcing `max_delay`. The same uncapped return path is reached for delta-seconds and HTTP-date headers. The minimal fix returns `min(server_delay, max_delay)`.

## Verified evidence

Validation was run in the authoring environment with Python 3.13.5 and the preinstalled pytest 9.0.2:

- `PYTHONPATH=src python -m pytest -q tests` — **12 passed**.
- `PYTHONPATH=src python -m pytest -q evaluation` on the unmodified baseline — **2 failed, 2 passed**, as expected. The failures are the over-cap numeric and HTTP-date cases.
- After applying `patches/fix-retry-after-cap.patch`, `PYTHONPATH=src python -m pytest -q tests evaluation` — **16 passed**.
- The applied patch was checked against `solutions/backoff.py`; the implementation files match.

The editable package-install step and Docker build were not verified in this environment. Docker was unavailable here. Use the commands in `reproducibility.md` and do not describe Docker as tested until you run it.

## Root cause

The implementation calculates a capped exponential delay but returns a parsed server delay without applying `max_delay`. Numeric and date header formats converge on the same return branch, so the scoped fix is one policy correction.

## Risk and trade-offs

The fix treats `max_delay` as a hard upper bound even when a server requests a longer wait. A production client should document this policy explicitly because server-directed retry guidance and local retry limits may have different product requirements.

## What was not done

- No real upstream GitHub issue was investigated.
- No external repository was modified.
- No LLM model was run; no model pass rate or comparative score is claimed.
- No Docker build, network integration, performance test, or production incident analysis was performed.
