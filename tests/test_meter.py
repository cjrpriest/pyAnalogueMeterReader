from datetime import datetime
from unittest import TestCase

from Meter import *
from Config import *


class TestMeter(TestCase):
    def test_Given_no_dial_position_updates__When_we_get_average_usage__Then_average_is_0(self):
        # Arrange
        meter = Meter(Config())

        # Act
        average = meter.get_average_per_min(5, self.__time("2017-04-26 13:01:00.000"))

        # Assert
        self.assertEqual(average, 0)

    def test_Given_one_dial_position_update__When_we_get_average_usage__Then_average_is_0(self):
        # Arrange
        meter = Meter(Config())

        meter.update_with_dial_position((self.__time("2017-04-26 13:00:00.000"), 0.5))

        # Act
        average = meter.get_average_per_min(5, self.__time("2017-04-26 13:00:01.000"))

        # Assert
        self.assertEqual(average, 0)

    def test_Given_dial_has_moved_0_1_in_1m__When_get_average_usage__Then_average_is_0_1(self):
        dial_positions = [
            (self.__time("2017-04-26 13:00:00.000"), 0.5),
            (self.__time("2017-04-26 13:00:30.000"), 0.55),
            (self.__time("2017-04-26 13:01:00.000"), 0.6)
        ]
        self.__assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=60,
                                          expected_average=0.1,
                                          current_time=self.__time("2017-04-26 13:01:00.000"))

    def test_Given_dial_has_moved_0_2_in_2m__When_get_average_usage__Then_average_is_0_1(self):
        dial_positions = [
            (self.__time("2017-04-26 13:00:00.000"), 0.5),
            (self.__time("2017-04-26 13:01:00.000"), 0.6),
            (self.__time("2017-04-26 13:02:00.000"), 0.7)
        ]
        self.__assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=120,
                                          expected_average=0.1,
                                          current_time=self.__time("2017-04-26 13:02:00.000"))

    def test_Given_dial_has_moved_0_2_in_2m_with_a_None_dial_position__When_get_average_usage__Then_average_is_0_1(
            self):
        dial_positions = [
            (self.__time("2017-04-26 13:00:00.000"), 0.5),
            (self.__time("2017-04-26 13:01:00.000"), None),
            (self.__time("2017-04-26 13:01:30.000"), 0.6),
            (self.__time("2017-04-26 13:02:00.000"), 0.7)
        ]
        self.__assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=120,
                                          expected_average=0.1,
                                          current_time=self.__time("2017-04-26 13:02:00.000"))

    def test_Given_dial_has_moved_0_3_in_2m__When_get_average_usage__Then_average_is_0_15(self):
        dial_positions = [
            (self.__time("2017-04-26 13:00:00.000"), 0.5),
            (self.__time("2017-04-26 13:01:00.000"), 0.6),
            (self.__time("2017-04-26 13:02:00.000"), 0.8)
        ]
        self.__assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=120,
                                          expected_average=0.15,
                                          current_time=self.__time("2017-04-26 13:02:00.000"))

    def test_Given_dial_moved_0_3_in_2m_with_readings_every_30s__When_get_average_usage__Then_average_is_0_15(self):
        dial_positions = [
            (self.__time("2017-04-26 13:00:00.000"), 0.5),
            (self.__time("2017-04-26 13:00:30.000"), 0.55),
            (self.__time("2017-04-26 13:01:00.000"), 0.6),
            (self.__time("2017-04-26 13:01:30.000"), 0.65),
            (self.__time("2017-04-26 13:02:00.000"), 0.8)
        ]
        self.__assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=120,
                                          expected_average=0.15,
                                          current_time=self.__time("2017-04-26 13:02:00.000"))

    def test_Given_dial_moved_0_3_in_2m_30s_with_readings_every_30s__When_get_average_usage__Then_average_is_0_12(self):
        dial_positions = [
            (self.__time("2017-04-26 13:00:00.000"), 0.5),
            (self.__time("2017-04-26 13:00:30.000"), 0.55),
            (self.__time("2017-04-26 13:01:00.000"), 0.6),
            (self.__time("2017-04-26 13:01:30.000"), 0.65),
            (self.__time("2017-04-26 13:02:00.000"), 0.7),
            (self.__time("2017-04-26 13:02:30.000"), 0.8)
        ]
        self.__assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=150,
                                          expected_average=0.12,
                                          current_time=self.__time("2017-04-26 13:02:30.000"))

    def test_Given_dial_moved_1_5_in_1m_30s_with_readings_every_30s__When_get_average_usage__Then_average_is_1(self):
        dial_positions = [
            (self.__time("2017-04-26 13:00:00.000"), 0.3),
            (self.__time("2017-04-26 13:00:30.000"), 0.9),
            (self.__time("2017-04-26 13:01:00.000"), 0.3),
            (self.__time("2017-04-26 13:01:30.000"), 0.8),
        ]
        self.__assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=90,
                                          expected_average=1,
                                          current_time=self.__time("2017-04-26 13:01:30.000"))

    def test_Given_dial_moved_3_in_1m_30s_with_irregular_readings__When_get_average_usage__Then_average_is_2(
            self):
        dial_positions = [
            (self.__time("2017-04-26 13:00:00.000"), 0.1),
            (self.__time("2017-04-26 13:00:15.000"), 0.55),
            (self.__time("2017-04-26 13:00:30.000"), 0),
            (self.__time("2017-04-26 13:00:45.000"), 0.45),
            (self.__time("2017-04-26 13:01:00.000"), 0.90),
            (self.__time("2017-04-26 13:01:15.000"), 0.35),
            (self.__time("2017-04-26 13:01:20.000"), 0.80),
            (self.__time("2017-04-26 13:01:30.000"), 0.1),
        ]
        self.__assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=90,
                                          expected_average=2,
                                          current_time=self.__time("2017-04-26 13:01:30.000"))

    def test_Given_dial_has_moved_0_in_2m__When_get_average_usage__Then_average_is_0(self):
        dial_positions = [
            (self.__time("2017-04-26 13:00:00.000"), 0.5),
            (self.__time("2017-04-26 13:01:00.000"), 0.5),
            (self.__time("2017-04-26 13:02:00.000"), 0.5)
        ]
        self.__assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=120,
                                          expected_average=0,
                                          current_time=self.__time("2017-04-26 13:02:00.000"))

    def test_Given_dial_moved_0_4_in_2m_with_even_movement__When_get_average_usage_over_last_60s__Then_average_is_2(
            self):
        dial_positions = [
            (self.__time("2017-04-26 13:00:00.000"), 0.1),
            (self.__time("2017-04-26 13:00:30.000"), 0.2),
            (self.__time("2017-04-26 13:01:00.000"), 0.3),
            (self.__time("2017-04-26 13:01:30.000"), 0.4),
            (self.__time("2017-04-26 13:02:00.000"), 0.5),
        ]
        self.__assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=60,
                                          expected_average=0.2,
                                          current_time=self.__time("2017-04-26 13:02:00.000"))

    def test_Given_dial_moved_0_4_in_2m_with_uneven_movement__When_get_average_usage_over_last_60s__Then_average_is_2(
            self):
        dial_positions = [
            (self.__time("2017-04-26 13:00:00.000"), 0.1),
            (self.__time("2017-04-26 13:00:30.000"), 0.2),
            (self.__time("2017-04-26 13:01:00.000"), 0.3),
            (self.__time("2017-04-26 13:01:30.000"), 0.4),
            (self.__time("2017-04-26 13:02:00.000"), 0.7),
        ]
        self.__assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=60,
                                          expected_average=0.4,
                                          current_time=self.__time("2017-04-26 13:02:00.000"))

    def test_Given_dial_moved_1_2_in_12s__When_get_average_usage_over_last_5s__Then_average_is_6(
            self):
        dial_positions = [
            (self.__time("2017-04-26 13:00:00.000"), 0.1),
            (self.__time("2017-04-26 13:00:01.000"), 0.2),
            (self.__time("2017-04-26 13:00:02.000"), 0.3),
            (self.__time("2017-04-26 13:00:03.000"), 0.4),
            (self.__time("2017-04-26 13:00:04.000"), 0.5),
            (self.__time("2017-04-26 13:00:05.000"), 0.6),
            (self.__time("2017-04-26 13:00:06.000"), 0.7),
            (self.__time("2017-04-26 13:00:07.000"), 0.8),
            (self.__time("2017-04-26 13:00:08.000"), 0.9),
            (self.__time("2017-04-26 13:00:09.000"), 0.0),
            (self.__time("2017-04-26 13:00:10.000"), 0.1),
            (self.__time("2017-04-26 13:00:11.000"), 0.2),
            (self.__time("2017-04-26 13:00:12.000"), 0.3),
        ]
        self.__assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=5,
                                          expected_average=6,
                                          current_time=self.__time("2017-04-26 13:00:12.000"))

    def test_Given_dial_moved_2_4_in_12s_with_uneven_movement__When_get_average_usage_over_last_5s__Then_average_is_12(
            self):
        dial_positions = [
            (self.__time("2017-04-26 13:00:00.000"), 0.1),
            (self.__time("2017-04-26 13:00:01.000"), 0.2),
            (self.__time("2017-04-26 13:00:02.000"), 0.3),
            (self.__time("2017-04-26 13:00:03.000"), 0.4),
            (self.__time("2017-04-26 13:00:04.000"), 0.5),
            (self.__time("2017-04-26 13:00:05.000"), 0.6),
            (self.__time("2017-04-26 13:00:06.000"), 0.7),
            (self.__time("2017-04-26 13:00:07.000"), 0.8),
            (self.__time("2017-04-26 13:00:08.000"), 0.0),
            (self.__time("2017-04-26 13:00:09.000"), 0.2),
            (self.__time("2017-04-26 13:00:10.000"), 0.4),
            (self.__time("2017-04-26 13:00:11.000"), 0.6),
            (self.__time("2017-04-26 13:00:12.000"), 0.8),
        ]
        self.__assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=5,
                                          expected_average=12,
                                          current_time=self.__time("2017-04-26 13:00:12.000"))

    def test_Given_dial_moved_0_1_in_5s_with_some_jitter__When_get_average_usage_over_last_5s__Then_average_is_1_2(
            self):
        dial_positions = [
            (self.__time("2017-04-26 13:00:00.000"), 0.1),
            (self.__time("2017-04-26 13:00:01.000"), 0.14),
            (self.__time("2017-04-26 13:00:02.000"), 0.15),
            (self.__time("2017-04-26 13:00:03.000"), 0.14),
            (self.__time("2017-04-26 13:00:04.000"), 0.15),
            (self.__time("2017-04-26 13:00:05.000"), 0.2),
        ]
        self.__assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=5,
                                          expected_average=1.2,
                                          current_time=self.__time("2017-04-26 13:00:05.000"))

    def test_Given_dial_moved_0_in_6s_with_some_jitter__When_get_average_usage_over_last_6s__Then_average_is_0(
            self):
        dial_positions = [
            (self.__time("2017-04-26 13:00:00.000"), 0.2),
            (self.__time("2017-04-26 13:00:01.000"), 0.1),
            (self.__time("2017-04-26 13:00:02.000"), 0.2),
            (self.__time("2017-04-26 13:00:03.000"), 0.1),
            (self.__time("2017-04-26 13:00:04.000"), 0.2),
            (self.__time("2017-04-26 13:00:05.000"), 0.1),
            (self.__time("2017-04-26 13:00:06.000"), 0.2),
        ]
        self.__assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=6,
                                          expected_average=0,
                                          current_time=self.__time("2017-04-26 13:00:06.000"))

    def test_Given_dial_moved_0_in_6s_with_some_jitter__When_get_average_usage_at_5s_and_6s__Then_averages_are_both_0(
            self):
        # Arrange
        meter = Meter(Config())

        dial_positions = [
            (self.__time("2017-04-26 13:00:00.000"), 0.2),
            (self.__time("2017-04-26 13:00:01.000"), 0.1),
            (self.__time("2017-04-26 13:00:02.000"), 0.2),
            (self.__time("2017-04-26 13:00:03.000"), 0.1),
            (self.__time("2017-04-26 13:00:04.000"), 0.2),
            (self.__time("2017-04-26 13:00:05.000"), 0.1),
        ]

        for dial_position in dial_positions:
            meter.update_with_dial_position(dial_position)

        # Act
        first_average = meter.get_average_per_min(5, self.__time("2017-04-26 13:00:05.000"))
        meter.update_with_dial_position((self.__time("2017-04-26 13:00:06.000"), 0.2))
        second_average = meter.get_average_per_min(5, self.__time("2017-04-26 13:00:06.000"))

        # Assert
        self.assertEqual(first_average, 0)
        self.assertEqual(second_average, 0)

    def test_Given_lots_of_jitter__When_the_dial_turns_slowly__Then_usage_is_not_missed_by_jitter_compensation(self):
        # Arrange
        meter = Meter(Config())

        for dial_position in [
            (self.__time("2017-04-26 13:00:00.000"), 0.0),
            (self.__time("2017-04-26 13:00:01.000"), 0.1),
            (self.__time("2017-04-26 13:00:02.000"), 0.0),
            (self.__time("2017-04-26 13:00:03.000"), 0.1),
        ]:
            meter.update_with_dial_position(dial_position)

        first_average = meter.get_average_per_min(60, self.__time("2017-04-26 13:00:03.000"))
        self.assertEqual(first_average, 0)

        for dial_position in [
            (self.__time("2017-04-26 13:00:04.000"), 0.2),
            (self.__time("2017-04-26 13:00:05.000"), 0.1),
            (self.__time("2017-04-26 13:00:06.000"), 0.2),
            (self.__time("2017-04-26 13:00:07.000"), 0.1),
        ]:
            meter.update_with_dial_position(dial_position)

        second_average = meter.get_average_per_min(60, self.__time("2017-04-26 13:00:07.000"))
        self.assertEqual(second_average, 0.2)

        for dial_position in [
            (self.__time("2017-04-26 13:00:04.000"), 0.2),
            (self.__time("2017-04-26 13:00:05.000"), 0.3),
            (self.__time("2017-04-26 13:00:06.000"), 0.2),
            (self.__time("2017-04-26 13:00:07.000"), 0.3),
            (self.__time("2017-04-26 13:00:06.000"), 0.2)
        ]:
            meter.update_with_dial_position(dial_position)

        third_average = meter.get_average_per_min(60, self.__time("2017-04-26 13:00:07.000"))
        self.assertEqual(third_average, 0.3)


    def test_Given_some_jitter_followed_by_actual_movement__When_we_get_average__Then_average_is_taken_from_highest_jitter_dial_position(
            self):
        dial_positions = [
            (self.__time("2017-04-26 13:00:00.000"), 0.2),
            (self.__time("2017-04-26 13:00:01.000"), 0.1),
            (self.__time("2017-04-26 13:00:02.000"), 0.2),
            (self.__time("2017-04-26 13:00:03.000"), 0.1),
            (self.__time("2017-04-26 13:00:04.000"), 0.2),
            (self.__time("2017-04-26 13:00:05.000"), 0.1),
            (self.__time("2017-04-26 13:00:06.000"), 0.2),
            (self.__time("2017-04-26 13:00:07.000"), 0.3),
            (self.__time("2017-04-26 13:00:07.000"), 0.4),
        ]

        self.__assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=60,
                                          expected_average=0.2,
                                          current_time=self.__time("2017-04-26 13:00:07.000"))

    def test_Given_dial_moved_0_1_in_5s_data_sent_out_of_order__When_get_average_usage_over_last_5s__Then_average_is_1_2(
            self):
        dial_positions = [
            (self.__time("2017-04-26 13:00:05.000"), 0.2),
            (self.__time("2017-04-26 13:00:04.000"), 0.18),
            (self.__time("2017-04-26 13:00:03.000"), 0.16),
            (self.__time("2017-04-26 13:00:02.000"), 0.14),
            (self.__time("2017-04-26 13:00:01.000"), 0.12),
            (self.__time("2017-04-26 13:00:00.000"), 0.1),
        ]
        self.__assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=5,
                                          expected_average=1.2,
                                          current_time=self.__time("2017-04-26 13:00:05.000"))

    def test_Given_some_real_world_data__When_third_reading_is_taken__Then_the_average_is_taken_over_the_whole_lookback_period(self):
        # Arrange
        meter = Meter(Config())

        dial_positions = [
            (self.__time("2017-05-22 19:49:11.367"), 0.41),
            (self.__time("2017-05-22 19:49:13.365"), 0.45),
            (self.__time("2017-05-22 19:49:15.366"), 0.49),
            (self.__time("2017-05-22 19:49:17.367"), 0.53),
            (self.__time("2017-05-22 19:49:19.367"), 0.56),
            (self.__time("2017-05-22 19:49:21.364"), 0.59),
            (self.__time("2017-05-22 19:49:23.366"), 0.63),
            (self.__time("2017-05-22 19:49:25.368"), 0.68),
            (self.__time("2017-05-22 19:49:27.366"), 0.73),
            (self.__time("2017-05-22 19:49:29.363"), 0.79),
            (self.__time("2017-05-22 19:49:31.364"), 0.83),
            (self.__time("2017-05-22 19:49:33.365"), 0.88),
            (self.__time("2017-05-22 19:49:35.367"), 0.94),
        ]

        for dial_position in dial_positions:
            meter.update_with_dial_position(dial_position)

        meter.get_average_per_min(120, self.__time("2017-05-22 19:49:37.338"))

        meter.update_with_dial_position((self.__time("2017-05-22 19:49:37.364"), 0.99))

        meter.get_average_per_min(120, self.__time("2017-05-22 19:49:37.450"))

        # Act
        average = meter.get_average_per_min(120, self.__time("2017-05-22 19:49:37.565"))

        # Assert
        self.assertEqual(average, 0.29)

    def test_Given_some_early_jitter_and_then_a_period_of_stability_over_90s__When_get_average_over_90s__Then_average_is_0(
            self):
        dial_positions = [
            (self.__time("2017-05-28 11:49:33.461"), 0.12),
            (self.__time("2017-05-28 11:49:38.462"), 0.13),
            (self.__time("2017-05-28 11:49:43.461"), 0.13),
            (self.__time("2017-05-28 11:49:48.463"), 0.12),
            (self.__time("2017-05-28 11:49:53.461"), 0.13),
            (self.__time("2017-05-28 11:49:58.458"), 0.13),
            (self.__time("2017-05-28 11:50:03.460"), 0.13),
            (self.__time("2017-05-28 11:50:08.460"), 0.13),
            (self.__time("2017-05-28 11:50:13.462"), 0.13),
            (self.__time("2017-05-28 11:50:18.461"), 0.13),
            (self.__time("2017-05-28 11:50:23.461"), 0.13),
            (self.__time("2017-05-28 11:50:28.458"), 0.13),
            (self.__time("2017-05-28 11:50:33.460"), 0.13),
            (self.__time("2017-05-28 11:50:38.461"), 0.13),
            (self.__time("2017-05-28 11:50:43.458"), 0.13),
            (self.__time("2017-05-28 11:50:48.458"), 0.13),
            (self.__time("2017-05-28 11:50:53.461"), 0.13),
            (self.__time("2017-05-28 11:50:58.459"), 0.13),
        ]
        self.__assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=90,
                                          expected_average=0,
                                          current_time=self.__time("2017-05-28 11:51:02.468"))

    def __assert_get_average_per_min(self, dial_positions, lookback_in_seconds, expected_average, current_time):
        # Arrange
        meter = Meter(Config())

        for dial_position in dial_positions:
            meter.update_with_dial_position(dial_position)

        # Act
        average = meter.get_average_per_min(lookback_in_seconds, current_time)

        # Assert
        self.assertEqual(average, expected_average)

    @staticmethod
    def __time(date_time_string):
        return datetime.strptime(date_time_string, "%Y-%m-%d %H:%M:%S.%f")
