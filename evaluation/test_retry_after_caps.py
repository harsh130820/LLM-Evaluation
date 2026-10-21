"""Issue-specific regression tests supplied by the evaluator.

These tests intentionally fail on the baseline implementation. Apply the patch
in patches/fix-retry-after-cap.patch to make the full evaluation suite pass.
"""

from datetime import datetime, timedelta, timezone
from email.utils import format_datetime

from retrykit import compute_delay


def test_numeric_retry_after_is_capped_by_max_delay():
    assert compute_delay(1, retry_after="120", max_delay=30.0) == 30.0


def test_http_date_retry_after_is_capped_by_max_delay():
    now = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    header = format_datetime(now + timedelta(seconds=120), usegmt=True)
    assert compute_delay(1, retry_after=header, max_delay=30.0, now=now) == 30.0


def test_server_delay_below_cap_is_preserved():
    assert compute_delay(1, retry_after="12", max_delay=30.0) == 12.0


def test_server_delay_equal_to_cap_is_preserved():
    assert compute_delay(1, retry_after="30", max_delay=30.0) == 30.0
