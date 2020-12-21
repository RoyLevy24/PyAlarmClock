import os
import sys
# tells the os to ignore Kivy's argument parser
os.environ["KIVY_NO_ARGS"] = "1"

sys.path.append("..")
sys.path.append("./src/")
sys.path.append("./src/frontend/")
sys.path.append("./src/backend/")
sys.path.append("./src/service/")

import argparse
from service.utils import *
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


def check_args(args):
    if args.camera_num < 0:
        raise Exception("camera_num must be greater than 0!")
    if get_num_camera_devices() < args.camera_num:
        raise Exception("camera_num is too high!")
    if check_ratio(args.ear, 0, 1) == False:
        raise Exception("eye aspect ratio must be between 0 - 1")
    if args.microphone_num < 0:
        raise Exception("microphone_num must be greater than 0!")
    if get_num_microphone_devices() < args.microphone_num:
        raise Exception("microphone_num is too high!")
    if check_ratio(args.sim_thresh, 0, 1) == False:
        raise Exception("similarity threshold must be between 0 - 1")


if __name__ == '__main__':
    args = get_command_line_args()
    check_args(args)
    app = PyAlarmClock(args)
    app.run()
