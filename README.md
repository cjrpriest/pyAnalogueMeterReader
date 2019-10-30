# pyAnalogueMeterReader
Read an analogue meter with a simple video feed

![](/readme-assets/pyAnalogueMeterReaderDebug.gif)

Watch my talk at Full Stack 2019 on how I used this software to read the analogue dial on my 1980s gas meter:

[![foo](https://i.vimeocdn.com/video/798146069_640x360.jpg)](https://skillsmatter.com/skillscasts/13853-how-i-turned-my-gas-meter-smart-using-my-own-software-a-raspberry-pi-and-some-other-bits)

[How I Turned My Gas Meter Smart Using My Own Software, A Raspberry Pi & Some Other Bits](https://skillsmatter.com/skillscasts/13853-how-i-turned-my-gas-meter-smart-using-my-own-software-a-raspberry-pi-and-some-other-bits)

### Features
Fully tested on a [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/), this project features the following:
* Use any source of frames (video), including the standard [Raspberry Pi Camera](https://www.raspberrypi.org/products/camera-module-v2/) or [any OpenCV supported source](https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-videocapture) 
* Fully configurable thresholds for recognising the dial position
* Dial tracking and calculation of rate of rotation
* Browser-based debug view
* Internal web-server to expose meter rate to other systems
* Algorithms to detect and remove misreads
* Comprehensive unit tests

## Getting Started

### Prerequisites

This project should work on any device running python with OpenCV libraries, that has some kind of OpenCV VideoCapture compatible camera connected. However, it is known to work well (especially in front of a remote meter ) with: 

* A [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)
* A [Raspberry Pi Camera](https://www.raspberrypi.org/products/camera-module-v2/)

### Raspberry Pi Setup

1. Flash your SD card with Raspbian Jessie (outside the scope of this README, [but you might want to check out the official documentation](https://www.raspberrypi.org/documentation/installation/installing-images/))
1. Run the following commands to upgrade packages
    * `sudo apt-get update`
    * `sudo apt-get upgrade`
    * `sudo reboot`
    * `sudo apt-get -y install screen build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk2.0-dev libatlas-base-dev gfortran python2.7-dev python3-dev`
1. Download and unzip OpenCV
    * `wget -O opencv345.zip https://github.com/opencv/opencv/archive/3.4.5.zip`
    * `wget -O opencv_contrib345.zip https://github.com/opencv/opencv_contrib/archive/3.4.5.zip`
    * `unzip opencv345.zip`
    * `unzip opencv_contrib345.zip`
1. Setup VirtualEnv.
    * `wget https://bootstrap.pypa.io/get-pip.py`
    * `sudo python get-pip.py`
    * `sudo pip install virtualenv virtualenvwrapper`
    * Add this to ~/.profile
        ```
        # virtualenv and virtualenvwrapper
        export WORKON_HOME=$HOME/.virtualenvs
        source /usr/local/bin/virtualenvwrapper.sh
        ```
    * `source ~/.profile`
    * `mkvirtualenv cv -p python2` (this also automatically puts us in ‘cv’ virtual environment)
1. Install NumPy
    * `pip install numpy`
1. Compile OpenCV
    * `cd ~/opencv-3.4.5/`
    * `mkdir build`
    * `cd build`
    * `cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D INSTALL_PYTHON_EXAMPLES=ON -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.4.5/modules -D BUILD_EXAMPLES=ON -D BUILD_NEW_PYTHON_SUPPORT=ON -D BUILD__PYTHON_SUPPORT=ON -D PYTHON_INCLUDE_DIR=/usr/include/python2.7 -D PYTHON_LIBRARY=/usr/lib/python2.7/config-arm-linux-gnueabihf/libpython2.7.so ..`
        * If you need to keep running cmake, consider `rm CMakeCache.txt` before each attempt.
    * `make` (consider running this in `screen`, it can take some time)
    * If your compile of OpenCV fails with `virtual memory exhausted: Cannot allocate memory`, then you can do the following to increased the virtual memory allocation
        * Change `CONF_SWAPSIZE=100` to `CONF_SWAPSIZE=512` in `/etc/dphys-swapfile`
        * `sudo /etc/init.d/dphys-swapfile stop`
        * `sudo /etc/init.d/dphys-swapfile start`
1. Install OpenCV
    * `sudo make install`
    * `sudo ldconfig`
    * And then to make the python opencv library available to the cv virtual environment:
        * `cd ~/.virtualenvs/cv/lib/python2.7/site-packages/`
        * `ln -s /usr/local/lib/python2.7/site-packages/cv2.so cv2.so`
1. Verify install completed successful
    * running `python` should return something like
        ```
        Python 2.7.13 (default, Sep 26 2018, 18:42:22)
        [GCC 6.3.0 20170516] on linux2
        Type "help", "copyright", "credits" or "license" for more information.
        >>>
        ```
    * and then executing the commands `import cv2` and `cv2.__version__` should return `'3.4.5'`

If you are using the Raspberry Pi Camera, then you'll need to set that up, and install the relevant python modules

1. `sudo raspi-config`
    * Option 5 (Interfacing Options) → P1 Camera → Yes, OK → Finish
    * Reboot the pi
1. `pip install flask`
1. `pip install imutils`
1. `pip install "picamera[array]"`

### Installing, configuring & running

`git clone https://github.com/cjrpriest/pyAnalogueMeterReader.git`

Create a `pyAnalogueMeterReader.Config.py` in the current directory

`cd pyAnalogueMeterReader`

`cp ../pyAnalogueMeterReader.Config.py Config.py`

`python Main.py`

#### Config.py

| Config Item | Type | Description |
|-------------|------|-------------|
| `frame_input` | String | Use `picamera` to use the Raspberry Pi Camera as the video source, otherwise a filename to read from a video file (primarily for testing), or a device index for attached devices such as USB cameras |
| `generate_full_debug_frame` | Boolean | Generate the full debug video (an example of which is shown at the top of this README). Very useful for debugging and/or check configuration | 
| `image_rotation_degrees` | Integer | (Degrees) Sometimes the camera isn't always exactly lined up withe meter. Use this configuration item to indicate by how much the feed should be rotated to bring the top of the dial to the top of the feed |
| `frame_size` | Tuple | The resolution to request from the video feed. (320, 240) should be more than sufficient -- sometimes lower resolutions are easier to process and have less 'noise' |
| `centre_of_dial` | Tuple | The location in the feed of the centre of the meter dial |
| `red_threshold_lower_boundary` | Integer | The lower colour boundary for which an area of the video feed is considered to be the dial |
| `red_threshold_upper_boundary` | Integer | The upper colour boundary for which an area of the video feed is considered to be the dial | 
| `min_approx_poly_area` | Integer | The minimum area of polygon that is to considered the dial (red areas forming a polygon that has a smaller area than this is disregarded) |
| `meter_measurement_interval_ms ` | Integer | Interval between meter measurements in milliseconds (suggest a value of around 5000, to not over-stress the Raspberry Pi |
| `meter_max_historical_measurements` | Integer | The number of historic measurements to maintain in memory. pyAnalogueMeterReader uses the historic meter readings to iron out erratic or inconsistent measurements |
| `average_rate_calculation_period_s` | Integer | Over what historic period (in seconds) should the average rate (or speed of dial) be measured. A lower number gives a more responsive reading. A large number smoothes out inconsistencies. Suggest a value around 5 seconds.  |
| `print_debug_info` | Boolean | Print debug information to console |

## Running the tests

Run `./runTests.sh`!

## Authors

* **Chris Priest** - *Initial work* - https://chrisprie.st, https://www.github.com/cjrpriest, https://twitter.com/cjrpriest

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
* Adrian Rosebrock at the excellent [https://www.pyimagesearch.com](https://www.pyimagesearch.com) for learning material, and the Raspberry Pi setup instructions upon which this README is loosely based.

