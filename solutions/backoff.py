"""Compute retry delays from exponential backoff and Retry-After headers."""

from __future__ import annotations

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime


def _parse_retry_after(value: str | None, now: datetime | None = None) -> float | None:
    """Parse Retry-After as delta-seconds or an HTTP-date.

    Invalid values return None so callers can fall back to exponential backoff.
    A date in the past is treated as zero seconds.
    """
    if value is None or not isinstance(value, str):
        return None

    candidate = value.strip()
    if not candidate:
        return None

    try:
        seconds = int(candidate)
        if seconds < 0:
            return None
        return float(seconds)
    except ValueError:
        pass

    try:
        target = parsedate_to_datetime(candidate)
        if target.tzinfo is None:
            target = target.replace(tzinfo=timezone.utc)
        reference = now or datetime.now(timezone.utc)
        if reference.tzinfo is None:
            raise ValueError("now must be timezone-aware")
        return max(0.0, (target - reference).total_seconds())
    except (TypeError, ValueError, OverflowError, IndexError):
        return None


def compute_delay(
    attempt: int,
    retry_after: str | None = None,
    *,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    now: datetime | None = None,
) -> float:
    """Return a retry delay in seconds.

    ``attempt`` is one-based. A valid Retry-After header takes precedence over
    exponential backoff. Exponential delays are capped at ``max_delay``.
    """
    if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt < 1:
        raise ValueError("attempt must be an integer greater than or equal to 1")
    if base_delay < 0 or max_delay < 0:
        raise ValueError("base_delay and max_delay must be non-negative")

    exponential_delay = min(base_delay * (2 ** (attempt - 1)), max_delay)

    if retry_after is not None:
        server_delay = _parse_retry_after(retry_after, now=now)
        if server_delay is not None:
            # Apply the configured cap consistently to server-provided delays.
            return min(server_delay, max_delay)

    return exponential_delay
