import datetime
import time

import thread
import WebServer
import logging
import logging.config
import logging.handlers

from FrameSource import FrameSource
from Meter import Meter
from FrameProcessor import FrameProcessor
from Config import *


class Application:
    __latest_frame = None
    __latest_dial_position = None
    __latest_usage_rate = None

    def __init__(self, meter, frame_processor, frame_source, config):
        """

        :param meter: 
        :type meter: Meter
        :param config: 
        :type config: Config
        :param frame_source: 
        :type frame_source: FrameSource
        :param frame_processor: 
        :type frame_processor: FrameProcessor
        """
        self.__meter = meter
        self.__frame_processor = frame_processor
        self.__frame_source = frame_source
        self.__config = config

        logging.config.dictConfig(self.__logging_config)
        self.__logger = logging.getLogger(__name__)
#        self.__logger.addHandler(logging.handlers.SysLogHandler(address='/var/run/syslog'))
        return

    def start(self):
        self.__logger.info("Starting application")

        WebServer.start(
            self.__get_latest_frame,
            self.__get_latest_usage_rate)

        self.__meter.start_taking_regular_measurements(
            self.__config.meter_measurement_interval_ms,
            self.__get_latest_dial_position
        )

        # self.start_debug_data_collecting_thread()

        self.__logger.info("Starting frame processing")
        while True:
            frame = self.__frame_source.get_next_frame()
            (dial_position, debug_frame) = self.__frame_processor.process_frame_for_dial_position(frame)
            self.__latest_dial_position = dial_position
            self.__latest_frame = debug_frame

            # print(str(self.__get_latest_usage_rate()))


    def __get_latest_frame(self):
        return self.__latest_frame

    def __get_latest_usage_rate(self):
        return self.__meter.get_average_per_min(
            lookback_in_seconds=self.__config.average_rate_calculation_period_s,
            current_date_time=datetime.datetime.utcnow())

    def __get_latest_dial_position(self):
        return self.__latest_dial_position

    def start_debug_data_collecting_thread(self):
        thread.start_new_thread(self.collect_debug_data, ())

    def collect_debug_data(self):
        interval_in_sec = 5.5
        start_time = time.time()
        while True:
            time.sleep(interval_in_sec - ((time.time() - start_time) % interval_in_sec))
            average = self.__meter.get_average_per_min(
                lookback_in_seconds=self.__config.average_rate_calculation_period_s,
                current_date_time=datetime.datetime.utcnow())

            print("frameNo:" + str(self.__frame_source.frame_no) + ", average:" + str(average))

    __logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
            'file_handler': {
                'level': 'INFO',
                'filename': 'test.log',
                'class': 'logging.FileHandler',
                'formatter': 'standard'
            }
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': 'INFO',
                'propagate': True
            },
        }
    }