"""
Unit tests for scheduler timezone conversion utility.
"""
import unittest
from app.core.scheduler import convert_vn_to_utc


class TestConvertVnToUtc(unittest.TestCase):
    """Test convert_vn_to_utc: VN time (UTC+7) -> UTC"""

    def test_morning_8am_vn(self):
        """08:00 VN = 01:00 UTC"""
        h, m = convert_vn_to_utc("08:00")
        assert h == 1 and m == 0

    def test_afternoon_14pm_vn(self):
        """14:00 VN = 07:00 UTC"""
        h, m = convert_vn_to_utc("14:00")
        assert h == 7 and m == 0

    def test_midnight_vn(self):
        """00:00 VN = 17:00 UTC (previous day)"""
        h, m = convert_vn_to_utc("00:00")
        assert h == 17 and m == 0

    def test_early_morning_wraps_day(self):
        """06:00 VN = 23:00 UTC (previous day)"""
        h, m = convert_vn_to_utc("06:00")
        assert h == 23 and m == 0

    def test_with_minutes(self):
        """08:30 VN = 01:30 UTC"""
        h, m = convert_vn_to_utc("08:30")
        assert h == 1 and m == 30

    def test_quarter_hour(self):
        """14:15 VN = 07:15 UTC"""
        h, m = convert_vn_to_utc("14:15")
        assert h == 7 and m == 15

    def test_late_night_23pm(self):
        """23:00 VN = 16:00 UTC"""
        h, m = convert_vn_to_utc("23:00")
        assert h == 16 and m == 0

    def test_invalid_string_returns_default(self):
        """Invalid input should fallback to 01:00 UTC (08:00 VN)"""
        h, m = convert_vn_to_utc("abc")
        assert h == 1 and m == 0

    def test_empty_string_returns_default(self):
        """Empty input should fallback to default"""
        h, m = convert_vn_to_utc("")
        assert h == 1 and m == 0

    def test_boundary_7am_vn(self):
        """07:00 VN = 00:00 UTC (exactly midnight)"""
        h, m = convert_vn_to_utc("07:00")
        assert h == 0 and m == 0
