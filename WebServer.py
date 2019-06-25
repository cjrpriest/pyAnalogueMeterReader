import cv2
import time

import thread
import logging
from flask import Flask, Response

_app = Flask(__name__)

_fn_get_latest_frame = None
_fn_get_latest_usage_rate = None
_fn_get_meter_reading = None

def _generate_mjpeg_stream():
    global _fn_get_latest_frame
    while True:
        time.sleep(0.2)  # regulate the amount of bandwidth being used
        jpeg_bytes = _get_jpeg_from_frame(_fn_get_latest_frame())
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg_bytes + b'\r\n\r\n')


def _web_server_start():
    _app.run(host="0.0.0.0", threaded=True)
    return


def _get_jpeg_from_frame(frame):
    ret, jpeg = cv2.imencode('.jpg', frame)
    jpeg_bytes = jpeg.tobytes()
    return jpeg_bytes


@_app.route('/video_feed')
def video_feed():
    return Response(_generate_mjpeg_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@_app.route('/usage_rate')
def usage_rate():
    global _fn_get_latest_usage_rate
    return Response(str(_fn_get_latest_usage_rate()))


@_app.route('/meter_reading')
def meter_reading():
    global _fn_get_meter_reading
    return Response(str(_fn_get_meter_reading()))


def start(fn_get_latest_frame, fn_get_latest_usage_rate, fn_get_meter_reading):
    logger = logging.getLogger(__name__)
    logger.info("Starting web server...")
    global _fn_get_latest_frame
    global _fn_get_latest_usage_rate
    global _fn_get_meter_reading
    _fn_get_latest_frame = fn_get_latest_frame
    _fn_get_latest_usage_rate = fn_get_latest_usage_rate
    _fn_get_meter_reading = fn_get_meter_reading
    thread.start_new_thread(_web_server_start, ())
    return
