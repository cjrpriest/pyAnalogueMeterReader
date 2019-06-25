import collections
import time
from datetime import timedelta, datetime

import thread
import logging

class Meter:
    __historical_dial_positions = None
    __furthest_dial_position = float(0)
    __meter_reading = float(0);

    def __init__(self, config):
        """

        :param config: 
        :type config: Config
        """

        self.__config = config
        self.__historical_dial_positions = collections.deque(
            maxlen=config.meter_max_historical_measurements)
        self.__logger = logging.getLogger(__name__)
        return

    def update_with_dial_position(self, (utc_datetime, dial_position)):
        if dial_position is not None:
            self.__historical_dial_positions.append((utc_datetime, dial_position))

    def get_meter_reading(self):
        return self.__meter_reading;


    def get_average_per_min(self, lookback_in_seconds, current_date_time):
        if len(self.__historical_dial_positions) == 0:
            return float(0)

        readings = list(self.__historical_dial_positions) # take a snapshot of the circular buffer into a list

        window_start_time = current_date_time - timedelta(seconds=lookback_in_seconds)

        readings_in_window = filter(lambda x: x[0] >= window_start_time, readings) # filter out those readings not in the time window
        readings_in_window.sort(key=lambda x: x[0]) # sort by time, so earliest reading is first

        last_dial_position = readings_in_window[len(readings_in_window)-1][1]

        if self.__config.print_debug_info:
            self.__log_debug_info(current_date_time, lookback_in_seconds, readings_in_window)

        if self.__furthest_dial_position == last_dial_position:
            return float(0)

        if last_dial_position > self.__furthest_dial_position:  # the most recent dial position appears to be further on than our furthest dial position
            self.__furthest_dial_position = last_dial_position
            self.__meter_reading = abs(self.__meter_reading) + last_dial_position
        elif last_dial_position < self.__furthest_dial_position:  # we've either gone past top position, or it's some jitter
            if (last_dial_position + 1) - self.__furthest_dial_position < 0.5:  # if the dial has moved less than half a rotation since the last know furthest position, we assume it's gone past top position
                self.__furthest_dial_position = last_dial_position
                self.__meter_reading = abs(self.__meter_reading) + 1 + last_dial_position

        total_usage = self.__get_total_usage_over_readings(readings_in_window)

        # calculate the average usage over the desired period
        readings_period_in_min = float(lookback_in_seconds) / 60
        average = total_usage / readings_period_in_min
        average = round(average, 2)

        return average

    def start_taking_regular_measurements(self, measurement_internal_ms, fn_get_latest_dial_position):
        self.__logger.info("Starting to take measurements every %sms", measurement_internal_ms)
        thread.start_new_thread(self.__take_regular_measurements,
                                (measurement_internal_ms, fn_get_latest_dial_position))

    def __get_total_usage_over_readings(self, readings):
        total_usage = 0
        absolute_total_usage = 0
        dial_movements_count = 0

        first_dial_position = readings[0][1]

        greatest_dial_position = first_dial_position
        previous_dial_position = first_dial_position

        for i in range(0, len(readings)):
            this_dial_position = float(readings[i][1])

            if this_dial_position > greatest_dial_position: # if the dial appears to have moved forward since last reading
                dial_position_movement = this_dial_position - greatest_dial_position # measure how much it's moved forward
                total_usage = total_usage + dial_position_movement # record the movement
                greatest_dial_position = this_dial_position # reset the marker for greatest known position
            # if this_dial_position == greatest_dial_position then it hasn't moved, and we do nothing
            elif this_dial_position < greatest_dial_position: # we've might have gone past top position, or it's jitter
                if (this_dial_position + 1) - greatest_dial_position < 0.5:  # if the dial has moved less than half a rotation
                    # since the last known greatest dial position, we assume it's gone past top position
                    dial_position_movement = (this_dial_position + 1) - greatest_dial_position # calc movement assuming
                    # dial has gone past top position
                    total_usage = total_usage + dial_position_movement # record the movement
                    greatest_dial_position = this_dial_position # reset the marker for greatest known position

            dial_position_difference = this_dial_position - previous_dial_position # record any apparent movement (forward or back)
            if dial_position_difference != 0:
                dial_movements_count = dial_movements_count + 1
            absolute_total_usage = absolute_total_usage + abs(dial_position_difference) # record absolute movement

            previous_dial_position = this_dial_position # reset marker for previous dial position

        if dial_movements_count >= 2:
            # look back all the readings, what was the average dial position change (forward or back) per dial movement?
            average_dial_position_change_per_movement = absolute_total_usage / dial_movements_count

            # if the average movement per reading (forward and back) was greater than or equal to the total movement
            # (forward only) then it is likely that the reading was jumping backwards and forwards, but the dial wasn't
            # actually moving, so return 0
            if average_dial_position_change_per_movement >= total_usage:
                return 0

        return total_usage

    def __take_regular_measurements(self, measurement_internal_ms, fn_get_latest_dial_position):
        interval_in_sec = float(measurement_internal_ms / 1000)
        start_time = time.time()
        while True:
            time.sleep(interval_in_sec - ((time.time() - start_time) % interval_in_sec))
            latest_dial_position = fn_get_latest_dial_position()
            self.__logger.info("Latest dial position is %s", latest_dial_position)
            self.update_with_dial_position((datetime.utcnow(), latest_dial_position))

    @staticmethod
    def __log_debug_info(current_date_time, lookback_in_seconds, dial_positions):
        Meter.__log_out_dial_positions(dial_positions)
        print("current time: " + current_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + ", lookback seconds: " + str(lookback_in_seconds))

    @staticmethod
    def __log_out_dial_positions(dial_positions):
        for i in range(0, len(dial_positions)):
            print("(self.__time(\"" + dial_positions[i][0].strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + "\"), " + str(dial_positions[i][1]) + "),")

