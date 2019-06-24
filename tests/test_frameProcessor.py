from unittest import TestCase

import cv2
from Config import *

from FrameProcessor import FrameProcessor


class TestFrameProcessor(TestCase):
    __test_file_name = "tests/20170411122357.avi"

    def test_dial_reads_0_59(self):
        self.Given_the_dial_is_in_position_x__When_the_dial_position_is_read__Then_position_x_is_returned(100, 0.59)
        return

    def test_dial_reads_0_86(self):
        self.Given_the_dial_is_in_position_x__When_the_dial_position_is_read__Then_position_x_is_returned(200, 0.86)
        return

    def test_dial_reads_0_99(self):
        self.Given_the_dial_is_in_position_x__When_the_dial_position_is_read__Then_position_x_is_returned(243, 0.99)
        return

    def test_dial_reads_0_01(self):
        self.Given_the_dial_is_in_position_x__When_the_dial_position_is_read__Then_position_x_is_returned(247, 0.01)
        return

    def test_dial_reads_0_17(self):
        self.Given_the_dial_is_in_position_x__When_the_dial_position_is_read__Then_position_x_is_returned(300, 0.17)
        return

    def test_dial_reads_0_41(self):
        self.Given_the_dial_is_in_position_x__When_the_dial_position_is_read__Then_position_x_is_returned(400, 0.41)
        return

    def Given_the_dial_is_in_position_x__When_the_dial_position_is_read__Then_position_x_is_returned(self, frame_no,
                                                                                                     expected_dial_position):
        # Arrange
        config = Config()
        config.generate_full_debug_frame = False
        config.centre_of_dial = (199, 86)
        frame = self.__get_frame(frame_no)
        fp = FrameProcessor(config)

        # Act
        (dial_position, debug_frame) = fp.process_frame_for_dial_position(frame)

        # Assert
        self.assertEqual(dial_position, expected_dial_position)
        return

    def __get_frame(self, frame_no):
        video_capture = cv2.VideoCapture(self.__test_file_name)
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        ret, frame = video_capture.read()
        frame = cv2.resize(frame, (320, 240))
        return frame
