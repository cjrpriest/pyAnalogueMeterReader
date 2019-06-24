from test_Meter_Base import *


class TestMeterJitter(TestMeterBase):
    def test_Given_dial_moved_0_1_in_5s_with_some_jitter__When_get_average_usage_over_last_5s__Then_average_is_1_2(
            self):
        dial_positions = [
            (TestMeterBase.time("2017-04-26 13:00:00.000"), 0.1),
            (TestMeterBase.time("2017-04-26 13:00:01.000"), 0.14),
            (TestMeterBase.time("2017-04-26 13:00:02.000"), 0.15),
            (TestMeterBase.time("2017-04-26 13:00:03.000"), 0.14),
            (TestMeterBase.time("2017-04-26 13:00:04.000"), 0.15),
            (TestMeterBase.time("2017-04-26 13:00:05.000"), 0.2),
        ]
        self.assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=5,
                                          expected_average=1.2,
                                          current_time=TestMeterBase.time("2017-04-26 13:00:05.000"))

    def test_Given_dial_moved_0_in_6s_with_some_jitter__When_get_average_usage_over_last_6s__Then_average_is_0(
            self):
        dial_positions = [
            (TestMeterBase.time("2017-04-26 13:00:00.000"), 0.2),
            (TestMeterBase.time("2017-04-26 13:00:01.000"), 0.1),
            (TestMeterBase.time("2017-04-26 13:00:02.000"), 0.2),
            (TestMeterBase.time("2017-04-26 13:00:03.000"), 0.1),
            (TestMeterBase.time("2017-04-26 13:00:04.000"), 0.2),
            (TestMeterBase.time("2017-04-26 13:00:05.000"), 0.1),
            (TestMeterBase.time("2017-04-26 13:00:06.000"), 0.2),
        ]
        self.assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=6,
                                          expected_average=0,
                                          current_time=TestMeterBase.time("2017-04-26 13:00:06.000"))

    def test_Given_dial_moved_0_in_6s_with_some_jitter__When_get_average_usage_at_5s_and_6s__Then_averages_are_both_0(
            self):
        # Arrange
        meter = Meter(Config())

        dial_positions = [
            (TestMeterBase.time("2017-04-26 13:00:00.000"), 0.2),
            (TestMeterBase.time("2017-04-26 13:00:01.000"), 0.1),
            (TestMeterBase.time("2017-04-26 13:00:02.000"), 0.2),
            (TestMeterBase.time("2017-04-26 13:00:03.000"), 0.1),
            (TestMeterBase.time("2017-04-26 13:00:04.000"), 0.2),
            (TestMeterBase.time("2017-04-26 13:00:05.000"), 0.1),
        ]

        for dial_position in dial_positions:
            meter.update_with_dial_position(dial_position)

        # Act
        first_average = meter.get_average_per_min(5, TestMeterBase.time("2017-04-26 13:00:05.000"))
        meter.update_with_dial_position((TestMeterBase.time("2017-04-26 13:00:06.000"), 0.2))
        second_average = meter.get_average_per_min(5, TestMeterBase.time("2017-04-26 13:00:06.000"))

        # Assert
        self.assertEqual(first_average, 0)
        self.assertEqual(second_average, 0)

    def test_Given_lots_of_jitter__When_the_dial_turns_slowly__Then_usage_is_not_missed_by_jitter_compensation(self):
        # Arrange
        meter = Meter(Config())

        for dial_position in [
            (TestMeterBase.time("2017-04-26 13:00:00.000"), 0.0),
            (TestMeterBase.time("2017-04-26 13:00:01.000"), 0.1),
            (TestMeterBase.time("2017-04-26 13:00:02.000"), 0.0),
            (TestMeterBase.time("2017-04-26 13:00:03.000"), 0.1),
        ]:
            meter.update_with_dial_position(dial_position)

        first_average = meter.get_average_per_min(60, TestMeterBase.time("2017-04-26 13:00:03.000"))
        self.assertEqual(0, first_average)

        for dial_position in [
            (TestMeterBase.time("2017-04-26 13:00:04.000"), 0.2),
            (TestMeterBase.time("2017-04-26 13:00:05.000"), 0.1),
            (TestMeterBase.time("2017-04-26 13:00:06.000"), 0.2),
            (TestMeterBase.time("2017-04-26 13:00:07.000"), 0.1),
        ]:
            meter.update_with_dial_position(dial_position)

        second_average = meter.get_average_per_min(60, TestMeterBase.time("2017-04-26 13:00:07.000"))
        self.assertEqual(0, second_average)

        for dial_position in [
            (TestMeterBase.time("2017-04-26 13:00:04.000"), 0.2),
            (TestMeterBase.time("2017-04-26 13:00:05.000"), 0.3),
            (TestMeterBase.time("2017-04-26 13:00:06.000"), 0.2),
            (TestMeterBase.time("2017-04-26 13:00:07.000"), 0.3),
            (TestMeterBase.time("2017-04-26 13:00:08.000"), 0.2)
        ]:
            meter.update_with_dial_position(dial_position)

        third_average = meter.get_average_per_min(60, TestMeterBase.time("2017-04-26 13:00:07.000"))
        self.assertEqual(0.3, third_average)


    def test_Given_some_jitter_followed_by_actual_movement__When_we_get_average__Then_average_is_taken_from_highest_jitter_dial_position(
            self):
        dial_positions = [
            (TestMeterBase.time("2017-04-26 13:00:00.000"), 0.2),
            (TestMeterBase.time("2017-04-26 13:00:01.000"), 0.1),
            (TestMeterBase.time("2017-04-26 13:00:02.000"), 0.2),
            (TestMeterBase.time("2017-04-26 13:00:03.000"), 0.1),
            (TestMeterBase.time("2017-04-26 13:00:04.000"), 0.2),
            (TestMeterBase.time("2017-04-26 13:00:05.000"), 0.1),
            (TestMeterBase.time("2017-04-26 13:00:06.000"), 0.2),
            (TestMeterBase.time("2017-04-26 13:00:07.000"), 0.3),
            (TestMeterBase.time("2017-04-26 13:00:07.000"), 0.4),
        ]

        self.assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=60,
                                          expected_average=0.2,
                                          current_time=TestMeterBase.time("2017-04-26 13:00:07.000"))

    def test_Given_some_early_jitter_and_then_a_period_of_stability_over_90s__When_get_average_over_90s__Then_average_is_0(
            self):
        dial_positions = [
            (TestMeterBase.time("2017-05-28 11:49:33.461"), 0.12),
            (TestMeterBase.time("2017-05-28 11:49:38.462"), 0.13),
            (TestMeterBase.time("2017-05-28 11:49:43.461"), 0.13),
            (TestMeterBase.time("2017-05-28 11:49:48.463"), 0.12),
            (TestMeterBase.time("2017-05-28 11:49:53.461"), 0.13),
            (TestMeterBase.time("2017-05-28 11:49:58.458"), 0.13),
            (TestMeterBase.time("2017-05-28 11:50:03.460"), 0.13),
            (TestMeterBase.time("2017-05-28 11:50:08.460"), 0.13),
            (TestMeterBase.time("2017-05-28 11:50:13.462"), 0.13),
            (TestMeterBase.time("2017-05-28 11:50:18.461"), 0.13),
            (TestMeterBase.time("2017-05-28 11:50:23.461"), 0.13),
            (TestMeterBase.time("2017-05-28 11:50:28.458"), 0.13),
            (TestMeterBase.time("2017-05-28 11:50:33.460"), 0.13),
            (TestMeterBase.time("2017-05-28 11:50:38.461"), 0.13),
            (TestMeterBase.time("2017-05-28 11:50:43.458"), 0.13),
            (TestMeterBase.time("2017-05-28 11:50:48.458"), 0.13),
            (TestMeterBase.time("2017-05-28 11:50:53.461"), 0.13),
            (TestMeterBase.time("2017-05-28 11:50:58.459"), 0.13),
        ]
        self.assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=90,
                                          expected_average=0,
                                          current_time=TestMeterBase.time("2017-05-28 11:51:02.468"))