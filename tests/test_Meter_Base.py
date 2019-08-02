from unittest import TestCase

from Meter import *
from TestConfig import *


class TestMeterBase(TestCase):
    def assert_get_average_per_min(self, dial_positions, lookback_in_seconds, expected_average, current_time):
        # Arrange
        meter = Meter(Config())

        for dial_position in dial_positions:
            meter.update_with_dial_position(dial_position)

        # Act
        average = meter.get_average_per_min(lookback_in_seconds, current_time)

        # Assert
        self.assertEqual(expected_average, average)

    @staticmethod
    def time(date_time_string):
        return datetime.strptime(date_time_string, "%Y-%m-%d %H:%M:%S.%f")
