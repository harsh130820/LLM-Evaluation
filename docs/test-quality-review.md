# Test-quality review

## Existing baseline tests

| Area | Covered? | Evidence | Assessment |
|---|---:|---|---|
| One-based exponential backoff | Yes | attempts 1–3 | Clear examples for the normal path |
| Exponential cap | Yes | high attempt, cap 10 | Guards existing cap behavior |
| Numeric `Retry-After` precedence | Yes | value below cap | Does not test a server value above the cap |
| HTTP-date parsing | Yes | fixed injected timestamp | Deterministic and independent of machine clock |
| Past HTTP-date | Yes | target before injected clock | Confirms zero-floor behavior |
| Invalid / empty header fallback | Yes | malformed and whitespace | Confirms fallback rather than exception |
| Invalid attempt inputs | Yes | parametrized boundaries and types | Good compact boundary coverage |
| Negative configuration | Yes | base and maximum delay | Covers negative values, but not NaN/infinity in baseline |

## Missing assertion that allowed the bug

The baseline suite checks that `max_delay` caps exponential backoff but never asserts that the same cap applies to a server-supplied delay. This is a **contract coverage gap**: two branches that return the same kind of value have inconsistent policy guarantees.

## Added regression tests

The evaluation tests cover:

- numeric server hint above the cap;
- date-form server hint above the cap;
- numeric value below the cap;
- value exactly equal to the cap.

The first two fail before the fix and pass after the fix. The latter two protect against an overcorrection that would ignore or unnecessarily shrink valid hints.

## Quality assessment

- **Determinism:** High. Date tests inject the reference time; no sleeps/network.
- **Isolation:** High. Each test checks one behavior in a pure function.
- **Readability:** High. Names describe observable behavior, not implementation details.
- **Failure diagnosis:** High. Numeric and date forms have separate tests.
- **Boundary coverage:** Improved by below/equal/above cap cases.
- **Integration coverage:** Not applicable to this small pure-function fixture; no HTTP client integration is included.

## Remaining useful tests

1. `max_delay=0` with a valid server hint should return zero.
2. Invalid `now` timezone awareness should have a documented and tested contract.
3. Non-finite configuration values (`NaN`, positive infinity) need an explicit contract and tests. They are outside this issue’s minimum acceptance criteria and are not changed by the reference patch.
4. A property-based invariant could assert `0 <= compute_delay(...) <= max_delay` for valid configurations across generated inputs.

## Reviewer note

Avoid writing tests that mirror the implementation line for line. The strongest tests here express the public guarantee—every returned delay is capped—through both supported header formats.
