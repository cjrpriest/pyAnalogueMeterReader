from test_Meter_Base import *


class TestMeterNormalUsage(TestMeterBase):
    def test_Given_dial_has_moved_0_1_in_1m__When_get_average_usage__Then_average_is_0_1(self):
        dial_positions = [
            (TestMeterBase.time("2017-04-26 13:00:00.000"), 0.5),
            (TestMeterBase.time("2017-04-26 13:00:30.000"), 0.55),
            (TestMeterBase.time("2017-04-26 13:01:00.000"), 0.6)
        ]
        self.assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=60,
                                          expected_average=0.1,
                                          current_time=TestMeterBase.time("2017-04-26 13:01:00.000"))

    def test_Given_dial_has_moved_0_2_in_2m__When_get_average_usage__Then_average_is_0_1(self):
        dial_positions = [
            (TestMeterBase.time("2017-04-26 13:00:00.000"), 0.5),
            (TestMeterBase.time("2017-04-26 13:01:00.000"), 0.6),
            (TestMeterBase.time("2017-04-26 13:02:00.000"), 0.7)
        ]
        self.assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=120,
                                          expected_average=0.1,
                                          current_time=TestMeterBase.time("2017-04-26 13:02:00.000"))

    def test_Given_dial_has_moved_0_2_in_2m_with_a_None_dial_position__When_get_average_usage__Then_average_is_0_1(
            self):
        dial_positions = [
            (TestMeterBase.time("2017-04-26 13:00:00.000"), 0.5),
            (TestMeterBase.time("2017-04-26 13:01:00.000"), None),
            (TestMeterBase.time("2017-04-26 13:01:30.000"), 0.6),
            (TestMeterBase.time("2017-04-26 13:02:00.000"), 0.7)
        ]
        self.assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=120,
                                          expected_average=0.1,
                                          current_time=TestMeterBase.time("2017-04-26 13:02:00.000"))

    def test_Given_dial_has_moved_0_3_in_2m__When_get_average_usage__Then_average_is_0_15(self):
        dial_positions = [
            (TestMeterBase.time("2017-04-26 13:00:00.000"), 0.5),
            (TestMeterBase.time("2017-04-26 13:01:00.000"), 0.6),
            (TestMeterBase.time("2017-04-26 13:02:00.000"), 0.8)
        ]
        self.assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=120,
                                          expected_average=0.15,
                                          current_time=TestMeterBase.time("2017-04-26 13:02:00.000"))

    def test_Given_dial_moved_0_3_in_2m_with_readings_every_30s__When_get_average_usage__Then_average_is_0_15(self):
        dial_positions = [
            (TestMeterBase.time("2017-04-26 13:00:00.000"), 0.5),
            (TestMeterBase.time("2017-04-26 13:00:30.000"), 0.55),
            (TestMeterBase.time("2017-04-26 13:01:00.000"), 0.6),
            (TestMeterBase.time("2017-04-26 13:01:30.000"), 0.65),
            (TestMeterBase.time("2017-04-26 13:02:00.000"), 0.8)
        ]
        self.assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=120,
                                          expected_average=0.15,
                                          current_time=TestMeterBase.time("2017-04-26 13:02:00.000"))

    def test_Given_dial_moved_0_3_in_2m_30s_with_readings_every_30s__When_get_average_usage__Then_average_is_0_12(self):
        dial_positions = [
            (TestMeterBase.time("2017-04-26 13:00:00.000"), 0.5),
            (TestMeterBase.time("2017-04-26 13:00:30.000"), 0.55),
            (TestMeterBase.time("2017-04-26 13:01:00.000"), 0.6),
            (TestMeterBase.time("2017-04-26 13:01:30.000"), 0.65),
            (TestMeterBase.time("2017-04-26 13:02:00.000"), 0.7),
            (TestMeterBase.time("2017-04-26 13:02:30.000"), 0.8)
        ]
        self.assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=150,
                                          expected_average=0.12,
                                          current_time=TestMeterBase.time("2017-04-26 13:02:30.000"))

    def test_Given_dial_moved_1_5_in_1m_30s_with_readings_every_30s__When_get_average_usage__Then_average_is_1(self):
        dial_positions = [
            (TestMeterBase.time("2017-04-26 13:00:00.000"), 0.3),
            (TestMeterBase.time("2017-04-26 13:00:30.000"), 0.9),
            (TestMeterBase.time("2017-04-26 13:01:00.000"), 0.3),
            (TestMeterBase.time("2017-04-26 13:01:30.000"), 0.8),
        ]
        self.assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=90,
                                          expected_average=1,
                                          current_time=TestMeterBase.time("2017-04-26 13:01:30.000"))

    def test_Given_dial_moved_3_in_1m_30s_with_irregular_readings__When_get_average_usage__Then_average_is_2(
            self):
        dial_positions = [
            (TestMeterBase.time("2017-04-26 13:00:00.000"), 0.1),
            (TestMeterBase.time("2017-04-26 13:00:15.000"), 0.55),
            (TestMeterBase.time("2017-04-26 13:00:30.000"), 0),
            (TestMeterBase.time("2017-04-26 13:00:45.000"), 0.45),
            (TestMeterBase.time("2017-04-26 13:01:00.000"), 0.90),
            (TestMeterBase.time("2017-04-26 13:01:15.000"), 0.35),
            (TestMeterBase.time("2017-04-26 13:01:20.000"), 0.80),
            (TestMeterBase.time("2017-04-26 13:01:30.000"), 0.1),
        ]
        self.assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=90,
                                          expected_average=2,
                                          current_time=TestMeterBase.time("2017-04-26 13:01:30.000"))

    def test_Given_dial_has_moved_0_in_2m__When_get_average_usage__Then_average_is_0(self):
        dial_positions = [
            (TestMeterBase.time("2017-04-26 13:00:00.000"), 0.5),
            (TestMeterBase.time("2017-04-26 13:01:00.000"), 0.5),
            (TestMeterBase.time("2017-04-26 13:02:00.000"), 0.5)
        ]
        self.assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=120,
                                          expected_average=0,
                                          current_time=TestMeterBase.time("2017-04-26 13:02:00.000"))

    def test_Given_dial_moved_0_4_in_2m_with_even_movement__When_get_average_usage_over_last_60s__Then_average_is_2(
            self):
        dial_positions = [
            (TestMeterBase.time("2017-04-26 13:00:00.000"), 0.1),
            (TestMeterBase.time("2017-04-26 13:00:30.000"), 0.2),
            (TestMeterBase.time("2017-04-26 13:01:00.000"), 0.3),
            (TestMeterBase.time("2017-04-26 13:01:30.000"), 0.4),
            (TestMeterBase.time("2017-04-26 13:02:00.000"), 0.5),
        ]
        self.assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=60,
                                          expected_average=0.2,
                                          current_time=TestMeterBase.time("2017-04-26 13:02:00.000"))

    def test_Given_dial_moved_0_4_in_2m_with_uneven_movement__When_get_average_usage_over_last_60s__Then_average_is_2(
            self):
        dial_positions = [
            (TestMeterBase.time("2017-04-26 13:00:00.000"), 0.1),
            (TestMeterBase.time("2017-04-26 13:00:30.000"), 0.2),
            (TestMeterBase.time("2017-04-26 13:01:00.000"), 0.3),
            (TestMeterBase.time("2017-04-26 13:01:30.000"), 0.4),
            (TestMeterBase.time("2017-04-26 13:02:00.000"), 0.7),
        ]
        self.assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=60,
                                          expected_average=0.4,
                                          current_time=TestMeterBase.time("2017-04-26 13:02:00.000"))

    def test_Given_dial_moved_1_2_in_12s__When_get_average_usage_over_last_5s__Then_average_is_6(
            self):
        dial_positions = [
            (TestMeterBase.time("2017-04-26 13:00:00.000"), 0.1),
            (TestMeterBase.time("2017-04-26 13:00:01.000"), 0.2),
            (TestMeterBase.time("2017-04-26 13:00:02.000"), 0.3),
            (TestMeterBase.time("2017-04-26 13:00:03.000"), 0.4),
            (TestMeterBase.time("2017-04-26 13:00:04.000"), 0.5),
            (TestMeterBase.time("2017-04-26 13:00:05.000"), 0.6),
            (TestMeterBase.time("2017-04-26 13:00:06.000"), 0.7),
            (TestMeterBase.time("2017-04-26 13:00:07.000"), 0.8),
            (TestMeterBase.time("2017-04-26 13:00:08.000"), 0.9),
            (TestMeterBase.time("2017-04-26 13:00:09.000"), 0.0),
            (TestMeterBase.time("2017-04-26 13:00:10.000"), 0.1),
            (TestMeterBase.time("2017-04-26 13:00:11.000"), 0.2),
            (TestMeterBase.time("2017-04-26 13:00:12.000"), 0.3),
        ]
        self.assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=5,
                                          expected_average=6,
                                          current_time=TestMeterBase.time("2017-04-26 13:00:12.000"))

    def test_Given_dial_moved_2_4_in_12s_with_uneven_movement__When_get_average_usage_over_last_5s__Then_average_is_12(
            self):
        dial_positions = [
            (TestMeterBase.time("2017-04-26 13:00:00.000"), 0.1),
            (TestMeterBase.time("2017-04-26 13:00:01.000"), 0.2),
            (TestMeterBase.time("2017-04-26 13:00:02.000"), 0.3),
            (TestMeterBase.time("2017-04-26 13:00:03.000"), 0.4),
            (TestMeterBase.time("2017-04-26 13:00:04.000"), 0.5),
            (TestMeterBase.time("2017-04-26 13:00:05.000"), 0.6),
            (TestMeterBase.time("2017-04-26 13:00:06.000"), 0.7),
            (TestMeterBase.time("2017-04-26 13:00:07.000"), 0.8),
            (TestMeterBase.time("2017-04-26 13:00:08.000"), 0.0),
            (TestMeterBase.time("2017-04-26 13:00:09.000"), 0.2),
            (TestMeterBase.time("2017-04-26 13:00:10.000"), 0.4),
            (TestMeterBase.time("2017-04-26 13:00:11.000"), 0.6),
            (TestMeterBase.time("2017-04-26 13:00:12.000"), 0.8),
        ]
        self.assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=5,
                                          expected_average=12,
                                          current_time=TestMeterBase.time("2017-04-26 13:00:12.000"))

    def test_Given_dial_moved_0_1_in_5s_data_sent_out_of_order__When_get_average_usage_over_last_5s__Then_average_is_1_2(
            self):
        dial_positions = [
            (TestMeterBase.time("2017-04-26 13:00:05.000"), 0.2),
            (TestMeterBase.time("2017-04-26 13:00:04.000"), 0.18),
            (TestMeterBase.time("2017-04-26 13:00:03.000"), 0.16),
            (TestMeterBase.time("2017-04-26 13:00:02.000"), 0.14),
            (TestMeterBase.time("2017-04-26 13:00:01.000"), 0.12),
            (TestMeterBase.time("2017-04-26 13:00:00.000"), 0.1),
        ]
        self.assert_get_average_per_min(dial_positions,
                                          lookback_in_seconds=5,
                                          expected_average=1.2,
                                          current_time=TestMeterBase.time("2017-04-26 13:00:05.000"))
