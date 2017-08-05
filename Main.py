from Application import *
from FrameProcessor import *
from Config import *


def main():
    config = Config()

    application = Application(
        Meter(config),
        FrameProcessor(config),
        FrameSource(config),
        config)

    application.start()
    return


if __name__ == "__main__":
    main()
