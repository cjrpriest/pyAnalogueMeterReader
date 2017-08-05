import numpy as np


class Config:
    def __init__(self):
        pass

    # frame_input = "tests/20170411122357.avi"
    frame_input = "tests/20170524125832.avi"
    generate_full_debug_frame = True
    image_rotation_degrees = -14
    frame_size = (320, 240)
    # centre_of_dial = (199, 86)
    centre_of_dial = (199, 92)
    red_threshold_lower_boundary = np.array([0, 20, 100], dtype="uint8")
    red_threshold_upper_boundary = np.array([40, 90, 200], dtype="uint8")
    min_approx_poly_area = 400
    meter_measurement_interval_ms = 5000
    meter_max_historical_measurements = 1000
    average_rate_calculation_period_s = 90
    print_debug_info = False
