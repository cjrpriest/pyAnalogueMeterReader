import time

import cv2

class FrameSource:
    __frame_source = None

    get_next_frame = None

    frame_no = 0

    def __init__(self, config):


        """

        :param config: 
        :type config: Config
        """

        frame_size = config.frame_size
        input = config.frame_input

        if input == "picamera":
            from PiVideoStream import PiVideoStream
            video_stream = PiVideoStream(resolution=frame_size)\
                .start()

            def get_next_frame():
                return video_stream.read()

            time.sleep(2.0)

            self.get_next_frame = get_next_frame
        else:
            video_capture = cv2.VideoCapture(input)

            # self.__skip_to_frame(video_capture, 1300)

            def get_next_frame():
                time.sleep(0.1)
                self.frame_no = self.frame_no + 1
                # print("frame:" + str(self.__frame_no))
                ret, frame = video_capture.read()
                frame = cv2.resize(frame, frame_size)
                return frame

            self.get_next_frame = get_next_frame

    def __skip_to_frame(self, video_capture, frame_no):
        print("Skipping to frame " + str(frame_no))
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        self.frame_no = frame_no
