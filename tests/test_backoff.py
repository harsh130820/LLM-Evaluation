from datetime import datetime, timedelta, timezone
from email.utils import format_datetime

import pytest

from retrykit import compute_delay


def test_exponential_backoff_uses_one_based_attempts():
    assert compute_delay(1) == 1.0
    assert compute_delay(2) == 2.0
    assert compute_delay(3) == 4.0


def test_exponential_backoff_is_capped():
    assert compute_delay(8, base_delay=1.0, max_delay=10.0) == 10.0


def test_numeric_retry_after_takes_precedence_when_under_cap():
    assert compute_delay(4, retry_after="5", max_delay=30.0) == 5.0


def test_http_date_retry_after_uses_injected_clock():
    now = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    header = format_datetime(now + timedelta(seconds=12), usegmt=True)
    assert compute_delay(1, retry_after=header, now=now) == 12.0


def test_past_http_date_becomes_zero_delay():
    now = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    header = format_datetime(now - timedelta(seconds=5), usegmt=True)
    assert compute_delay(1, retry_after=header, now=now) == 0.0


def test_invalid_header_falls_back_to_exponential_backoff():
    assert compute_delay(3, retry_after="not-a-date", base_delay=2.0) == 8.0


def test_empty_header_falls_back_to_exponential_backoff():
    assert compute_delay(2, retry_after="   ") == 2.0


@pytest.mark.parametrize("attempt", [0, -1, True, 1.5])
def test_invalid_attempt_is_rejected(attempt):
    with pytest.raises(ValueError):
        compute_delay(attempt)


def test_negative_delay_configuration_is_rejected():
    with pytest.raises(ValueError):
        compute_delay(1, base_delay=-0.1)
    with pytest.raises(ValueError):
        compute_delay(1, max_delay=-0.1)
