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


    def test_Given_some_real_world_data__When_third_reading_is_taken__Then_the_average_is_taken_over_the_whole_lookback_period(self):
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

        meter.get_average_per_min(120, TestMeterBase.time("2017-05-22 19:49:37.338"))

        meter.update_with_dial_position((TestMeterBase.time("2017-05-22 19:49:37.364"), 0.99))

        meter.get_average_per_min(120, TestMeterBase.time("2017-05-22 19:49:37.450"))

        # Act
        average = meter.get_average_per_min(120, TestMeterBase.time("2017-05-22 19:49:37.565"))

        # Assert
        self.assertEqual(average, 0.29)

