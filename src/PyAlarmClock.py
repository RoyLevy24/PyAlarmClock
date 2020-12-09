import argparse
import os
import sys

# tells the os to ignore Kivy's argument parser
os.environ["KIVY_NO_ARGS"] = "1"

sys.path.append("..")
sys.path.append("./src/")
sys.path.append("./src/frontend/")
sys.path.append("./src/backend/")
sys.path.append("./src/service/")

from frontend.frontend import *


class PyAlarmClock():
    """
    This class is the main entry point of the app.
    """

    def __init__(self, args):
        # creates KivyMD alarm clock app
        self.app = AlarmApp(args)

    def run(self):
        # running KivyMD alarm clock app
        self.app.run()


def get_command_line_args():
    """
    Returns the application arguments parser.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--camera_num', type=int, default=0,
                        help="camera device number for open eyes recognition")
    parser.add_argument('-e', '--ear', type=float, default=0.31,
                        help="eye aspect ratio for open eyes recognition")
    parser.add_argument('-m', '--microphone_num', type=int, default=0,
                        help="microphone device number for speech recognition")
    parser.add_argument('-s', '--sim_thresh', type=float, default=0.65,
                        help="similarity ratio between words for speech recognition")
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = get_command_line_args()
    app = PyAlarmClock(args)
    app.run()
