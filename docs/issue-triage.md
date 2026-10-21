# Issue triage: Retry-After bypasses configured delay cap

> **Portfolio exercise:** This is a deliberately constructed evaluation fixture, not a claim about an existing upstream issue or a real production incident.

## Summary

`compute_delay()` caps exponential backoff at `max_delay`, but a valid `Retry-After` value is returned directly. A remote service can therefore make the caller wait longer than the local policy permits. The defect affects both delta-seconds (for example, `Retry-After: 120`) and HTTP-date values.

## Classification

- **Type:** Bug / inconsistent policy enforcement
- **Suggested priority:** P2 (normal-to-high, depending on product retry guarantees)
- **Affected component:** Retry delay calculation
- **Reproducibility:** Deterministic, no network required
- **Likely scope:** One return path; the date and integer parsing paths converge on the same uncapped return

Priority is an illustrative triage judgment for this sample, not an upstream maintainer decision.

## Minimal reproduction

```python
from retrykit import compute_delay

print(compute_delay(1, retry_after="120", max_delay=30.0))
# Actual baseline result: 120.0
# Expected result: 30.0
```

The equivalent HTTP-date reproduction is covered by `evaluation/test_retry_after_caps.py` with an injected clock, so the test does not depend on wall-clock time.

## Expected behavior

1. A valid server-provided delay takes precedence over exponential backoff.
2. The final returned delay is always in the inclusive range `[0, max_delay]`.
3. A valid value below the cap is preserved.
4. Invalid or missing headers fall back to the configured exponential delay.
5. Tests for HTTP-date behavior use an injected clock to remain deterministic.

## Acceptance criteria

- Both numeric and HTTP-date `Retry-After` values are capped at `max_delay`.
- Values less than the cap remain unchanged.
- The existing unit tests continue to pass.
- Regression tests fail on the baseline and pass with the proposed fix.
- No network calls or real sleeps are required to validate the fix.

## Non-goals

- Changing retryable HTTP status codes.
- Implementing a network client or retry loop.
- Changing the public function signature.
- Claiming RFC compliance beyond the behaviors exercised by this fixture.
