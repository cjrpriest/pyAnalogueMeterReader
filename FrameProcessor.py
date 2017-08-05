import math

import cv2
import numpy as np

from Config import *

class FrameProcessor:
    __colour_red = (255, 0, 255)
    __colour_blue = (255, 0, 0)
    __colour_green = (0, 255, 0)
    __colour_white = (255, 255, 255)

    def __init__(self, config):

        """
        
        :param config:
        :type config: Config
        """
        self.__config = config

        self.__image_rotation_matrix = cv2.getRotationMatrix2D(
            self.__config.centre_of_dial,
            self.__config.image_rotation_degrees,
            1)
        return

    def process_frame_for_dial_position(self, original_frame):
        dial_position = None

        frame_rotated = cv2.warpAffine(
            src=original_frame,
            M=self.__image_rotation_matrix,
            dsize=self.__config.frame_size)

        debug_frame_final_result = frame_rotated.copy()

        red_only_mask_frame = cv2.inRange(
            src=frame_rotated,
            lowerb=self.__config.red_threshold_lower_boundary,
            upperb=self.__config.red_threshold_upper_boundary)

        red_only_frame = cv2.bitwise_and(
            src1=frame_rotated,
            src2=frame_rotated,
            mask=red_only_mask_frame)

        red_only_blurred_mask_frame = cv2.GaussianBlur(
            src=red_only_mask_frame,
            ksize=(11, 11),
            sigmaX=0)

        retval, result = cv2.threshold(
            src=red_only_blurred_mask_frame,
            thresh=60,
            maxval=255,
            type=cv2.THRESH_BINARY)
        red_only_blurred_mask_frame_threshold = result

        _, contours_around_red_only, hierarchy = cv2.findContours(
            image=red_only_blurred_mask_frame_threshold,
            mode=cv2.RETR_LIST,
            method=cv2.CHAIN_APPROX_SIMPLE)

        if self.__config.generate_full_debug_frame:
            contours_on_red_only_blurred_mask_frame_threshold = red_only_blurred_mask_frame_threshold.copy()
            contours_on_red_only_blurred_mask_frame_threshold = cv2.cvtColor(
                contours_on_red_only_blurred_mask_frame_threshold, cv2.COLOR_GRAY2BGR)
            cv2.drawContours(
                image=contours_on_red_only_blurred_mask_frame_threshold,
                contours=contours_around_red_only,
                contourIdx=-1,
                color=self.__colour_green,
                thickness=2)

        blank_frame = np.zeros(shape=(self.__config.frame_size[1], self.__config.frame_size[0], 3), dtype=np.uint8)
        big_area_contours_frame = blank_frame.copy()

        number_of_contours = len(contours_around_red_only)

        for contour_index in range(0, number_of_contours):
            approx_poly_made_by_contour = cv2.approxPolyDP(
                curve=contours_around_red_only[contour_index],
                epsilon=cv2.arcLength(contours_around_red_only[contour_index], True) * 0.03,
                closed=True)
            area_of_approx_poly = cv2.contourArea(approx_poly_made_by_contour)
            if (area_of_approx_poly > self.__config.min_approx_poly_area):
                if self.__config.generate_full_debug_frame:
                    cv2.drawContours(
                        image=big_area_contours_frame,
                        contours=contours_around_red_only,
                        contourIdx=contour_index,
                        color=self.__colour_green,
                        thickness=3)

                    rect = cv2.minAreaRect(contours_around_red_only[contour_index])
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(big_area_contours_frame, [box], 0, (0, 0, 255), 2)
                furthest_distance = 0
                furthest_point = (0, 0)
                for j in range(0, len(contours_around_red_only[contour_index])):
                    point = contours_around_red_only[contour_index][j][0]
                    distance = self.__distance_between_points(self.__config.centre_of_dial, point)
                    if distance > furthest_distance:
                        furthest_distance = distance
                        furthest_point = tuple(point)
                cv2.line(big_area_contours_frame, self.__config.centre_of_dial, furthest_point, self.__colour_blue, 3)
                cv2.line(debug_frame_final_result, self.__config.centre_of_dial, furthest_point, self.__colour_blue, 3)
                angle = self.__get_angle_of_line_between_two_points(furthest_point, self.__config.centre_of_dial)
                angle = angle + 270
                angle = angle % 360
                angle = round(angle, 0)
                dial_position = round(angle / 360, 2)
                cv2.putText(debug_frame_final_result, "Dial angle: " + str(angle), (20, 150), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 255, 255), 2)
                cv2.putText(debug_frame_final_result, "Dial position: " + str(dial_position), (20, 170),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                break

        debug_frame = None
        if self.__config.generate_full_debug_frame:

            red_bits_mask_frame_blurred_threshold_colour = cv2.cvtColor(red_only_blurred_mask_frame_threshold,
                                                                        cv2.COLOR_GRAY2BGR)
            red_only_mask_frame_colour = cv2.cvtColor(red_only_mask_frame, cv2.COLOR_GRAY2BGR)
            red_only_blurred_mask_frame_colour = cv2.cvtColor(red_only_blurred_mask_frame, cv2.COLOR_GRAY2BGR)

            cv2.drawMarker(img=big_area_contours_frame, position=self.__config.centre_of_dial, color=self.__colour_white)

            self.__write_header_on_frame(original_frame, "Original")
            self.__write_header_on_frame(frame_rotated, "De-skewed")
            self.__write_header_on_frame(red_only_frame, "Threshold out non-redish colour")
            self.__write_header_on_frame(red_only_mask_frame_colour, "Convert to black & white")
            self.__write_header_on_frame(red_only_blurred_mask_frame_colour, "Blur it a bit")
            self.__write_header_on_frame(red_bits_mask_frame_blurred_threshold_colour, "Convert to black & white again")
            self.__write_header_on_frame(contours_on_red_only_blurred_mask_frame_threshold,
                                         "Draw contours around everything")
            self.__write_header_on_frame(big_area_contours_frame, "Find big shape, draw line to far point")
            self.__write_header_on_frame(debug_frame_final_result, "Calculate angle of line")

            first_row = np.hstack([original_frame, frame_rotated, red_only_frame])
            second_row = np.hstack([red_only_mask_frame_colour, red_only_blurred_mask_frame_colour,
                                    red_bits_mask_frame_blurred_threshold_colour])
            third_row = np.hstack(
                [contours_on_red_only_blurred_mask_frame_threshold, big_area_contours_frame, debug_frame_final_result])

            debug_frame = np.vstack([first_row, second_row, third_row])
        else:
            debug_frame = debug_frame_final_result

        return (dial_position, debug_frame)

    @staticmethod
    def __distance_between_points(point1, point2):
        x = point2[0] - point1[0]
        y = point2[1] - point1[1]
        distance = math.hypot(x, y)
        return distance

    @staticmethod
    def __get_angle_of_line_between_two_points(point1, point2):
        x_diff = point2[0] - point1[0]
        y_diff = point2[1] - point1[1]
        return math.degrees(math.atan2(y_diff, x_diff))

    def __write_header_on_frame(self, frame, header_text):
        cv2.putText(
            img=frame,
            text=header_text,
            org=(10, 20),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=self.__colour_white,
            thickness=2)
        return
