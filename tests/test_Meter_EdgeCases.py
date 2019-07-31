from test_Meter_Base import *


class TestMeterEdgeCases(TestMeterBase):
    def test_Given_no_dial_position_updates__When_we_get_average_usage__Then_average_is_0(self):
        # Arrange
        meter = Meter(Config())

        # Act
        average = meter.get_average_per_min(5, TestMeterBase.time("2017-04-26 13:01:00.000"))

        # Assert
        self.assertEqual(average, 0)

    def test_Given_one_dial_position_update__When_we_get_average_usage__Then_average_is_0(self):
        # Arrange
        meter = Meter(Config())

        meter.update_with_dial_position((TestMeterBase.time("2017-04-26 13:00:00.000"), 0.5))

        # Act
        average = meter.get_average_per_min(5, TestMeterBase.time("2017-04-26 13:00:01.000"))

        # Assert
        self.assertEqual(average, 0)


    def test_Given_some_real_world_data__When_second_reading_is_taken__Then_the_average_is_taken_over_the_whole_lookback_period(self):
        # Arrange
        meter = Meter(Config())

        dial_positions = [
            (TestMeterBase.time("2017-05-22 19:49:11.367"), 0.41),
            (TestMeterBase.time("2017-05-22 19:49:13.365"), 0.45),
            (TestMeterBase.time("2017-05-22 19:49:15.366"), 0.49),
            (TestMeterBase.time("2017-05-22 19:49:17.367"), 0.53),
            (TestMeterBase.time("2017-05-22 19:49:19.367"), 0.56),
            (TestMeterBase.time("2017-05-22 19:49:21.364"), 0.59),
            (TestMeterBase.time("2017-05-22 19:49:23.366"), 0.63),
            (TestMeterBase.time("2017-05-22 19:49:25.368"), 0.68),
            (TestMeterBase.time("2017-05-22 19:49:27.366"), 0.73),
            (TestMeterBase.time("2017-05-22 19:49:29.363"), 0.79),
            (TestMeterBase.time("2017-05-22 19:49:31.364"), 0.83),
            (TestMeterBase.time("2017-05-22 19:49:33.365"), 0.88),
            (TestMeterBase.time("2017-05-22 19:49:35.367"), 0.94),
        ]

        for dial_position in dial_positions:
            meter.update_with_dial_position(dial_position)

        average1 = meter.get_average_per_min(120, TestMeterBase.time("2017-05-22 19:49:37.338"))

        meter.update_with_dial_position((TestMeterBase.time("2017-05-22 19:49:37.364"), 0.99))

        # Act
        average2 = meter.get_average_per_min(120, TestMeterBase.time("2017-05-22 19:49:37.450"))

        # Assert
        self.assertEqual(0.29, average2)

    def test_Given_some_jitter_beyond_one_dial_increment__When_readings_are_taken_over_two_non_overlapping_periods__Then_the_first_reports_usage_but_the_second_does_not(self):
        # Arrange
        meter = Meter(Config())

        dial_positions = [
            (TestMeterBase.time("2017-05-22 12:00:00.000"), 0.5),
            (TestMeterBase.time("2017-05-22 12:00:01.000"), 0.51),
            (TestMeterBase.time("2017-05-22 12:00:02.000"), 0.5),
            (TestMeterBase.time("2017-05-22 12:00:03.000"), 0.51),
            (TestMeterBase.time("2017-05-22 12:00:04.000"), 0.5),
            (TestMeterBase.time("2017-05-22 12:00:05.000"), 0.52),
            (TestMeterBase.time("2017-05-22 12:00:06.000"), 0.5),
            (TestMeterBase.time("2017-05-22 12:00:07.000"), 0.51),
            (TestMeterBase.time("2017-05-22 12:00:08.000"), 0.5),
            (TestMeterBase.time("2017-05-22 12:00:09.000"), 0.51),
            (TestMeterBase.time("2017-05-22 12:00:10.000"), 0.5),
            (TestMeterBase.time("2017-05-22 12:00:11.000"), 0.52),
        ]

        for dial_position in dial_positions:
            meter.update_with_dial_position(dial_position)

        # Act
        first_average = meter.get_average_per_min(5, TestMeterBase.time("2017-05-22 12:00:05.000"))
        second_average = meter.get_average_per_min(5, TestMeterBase.time("2017-05-22 12:00:11.000"))

        # Assert
        self.assertGreater(first_average, 0)
        self.assertEqual(second_average, 0)

    def test_Given_some_jitter_beyond_one_dial_increment__When_readings_are_taken_over_two_non_overlapping_periods__Then_the_first_reports_usage_but_the_second_does_not2(self):
        # Arrange
        meter = Meter(Config())

        dial_positions = [
            (TestMeterBase.time("2017-05-22 12:00:00.000"), 0.41),
            (TestMeterBase.time("2017-05-22 12:00:01.000"), 0.42),
            (TestMeterBase.time("2017-05-22 12:00:02.000"), 0.38),
            (TestMeterBase.time("2017-05-22 12:00:03.000"), 0.42),
            (TestMeterBase.time("2017-05-22 12:00:04.000"), 0.42),
            (TestMeterBase.time("2017-05-22 12:00:05.000"), 0.41),
            (TestMeterBase.time("2017-05-22 12:00:06.000"), 0.42),
            (TestMeterBase.time("2017-05-22 12:00:07.000"), 0.42),
            (TestMeterBase.time("2017-05-22 12:00:08.000"), 0.42),
        ]

        for dial_position in dial_positions:
            meter.update_with_dial_position(dial_position)

        # Act
        first_average = meter.get_average_per_min(5, TestMeterBase.time("2017-05-22 12:00:05.000"))
        second_average = meter.get_average_per_min(5, TestMeterBase.time("2017-05-22 12:00:07.000"))

        # Assert
        self.assertEqual(first_average, 0)
        self.assertEqual(second_average, 0)


    def test_Given_some_meter_movements__When_two_readings_are_taken_with_no_new_dial_position_in_between_them__Then_both_are_non_zero(self):
        # Arrange
        meter = Meter(Config())

        dial_positions = [
            (TestMeterBase.time("2017-05-22 19:49:31.364"), 0.83),
            (TestMeterBase.time("2017-05-22 19:49:33.365"), 0.88),
            (TestMeterBase.time("2017-05-22 19:49:35.367"), 0.94),
        ]

        for dial_position in dial_positions:
            meter.update_with_dial_position(dial_position)

        # Act
        average1 = meter.get_average_per_min(120, TestMeterBase.time("2017-05-22 19:49:37.338"))
        average2 = meter.get_average_per_min(120, TestMeterBase.time("2017-05-22 19:49:37.450"))

        # Assert
        self.assertNotEqual(0, average1)
        self.assertNotEqual(0, average2)
