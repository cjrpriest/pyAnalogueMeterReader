from test_Meter_Base import *


class TestMeterRemoveJitter(TestMeterBase):
    def test_Given_basic_incrementing_dial_positions__When_processed__Then_the_most_recent_is_the_highest_reading(self):
        # Arrange
        meter = Meter(Config())

        dial_positions = [
            (TestMeterBase.time("2017-05-22 19:49:31.364"), 0.83),
            (TestMeterBase.time("2017-05-22 19:49:33.365"), 0.88),
            (TestMeterBase.time("2017-05-22 19:49:35.367"), 0.94),
        ]

        # Act
        clean_dial_positions = meter._Meter__remove_jitter_from_readings(dial_positions)

        # Assert
        rightmost_dial_position = clean_dial_positions[-1]

        self.assertEqual(rightmost_dial_position[1], 0.94)

    def test_Given_jittering_dial_positions__When_processed__Then_the_most_recent_is_the_highest_reading_and_there_are_five_readings(self):
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

        # Act
        clean_dial_positions = meter._Meter__remove_jitter_from_readings(dial_positions)

        # Assert
        self.assertEqual(0.52, clean_dial_positions[-1][1])
        self.assertEqual(5, len(clean_dial_positions))

    def test_Given_dial_positions_that_go_past_zero__When_processed__Then_the_most_recent_is_the_highest_reading_and_there_are_six_readings(self):
        # Arrange
        meter = Meter(Config())

        dial_positions = [
            (TestMeterBase.time("2017-05-22 12:00:00.000"), 0.8),
            (TestMeterBase.time("2017-05-22 12:00:01.000"), 0.9),
            (TestMeterBase.time("2017-05-22 12:00:02.000"), 0.0),
            (TestMeterBase.time("2017-05-22 12:00:03.000"), 0.1),
            (TestMeterBase.time("2017-05-22 12:00:04.000"), 0.2),
            (TestMeterBase.time("2017-05-22 12:00:05.000"), 0.3),
        ]

        # Act
        clean_dial_positions = meter._Meter__remove_jitter_from_readings(dial_positions)

        # Assert
        self.assertEqual(0.3, clean_dial_positions[-1][1])
        self.assertEqual(6, len(clean_dial_positions))

    def test_Given_dial_positions_that_stay_stagnant__When_processed__Then_the_stagnant_readings_remain(self):
        # Arrange
        meter = Meter(Config())

        dial_positions = [
            (TestMeterBase.time("2017-05-22 12:00:00.000"), 0.1),
            (TestMeterBase.time("2017-05-22 12:00:01.000"), 0.2),
            (TestMeterBase.time("2017-05-22 12:00:02.000"), 0.2),
            (TestMeterBase.time("2017-05-22 12:00:03.000"), 0.2),
            (TestMeterBase.time("2017-05-22 12:00:04.000"), 0.3),
            (TestMeterBase.time("2017-05-22 12:00:05.000"), 0.4),
        ]

        # Act
        clean_dial_positions = meter._Meter__remove_jitter_from_readings(dial_positions)

        # Assert
        self.assertEqual(0.4, clean_dial_positions[-1][1])
        self.assertEqual(6, len(clean_dial_positions))


