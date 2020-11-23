import sys
sys.path.append("../OpenEyesDetection")
import OpenEyesDetect

from Alarm import *



class OpenEyesAlarm(Alarm):

    def __init__(self, time, days, description, ring, frames):
        Alarm.__init__(self, time, days, description, ring)
        self.frames = frames

    def execute(self):
        open_eyes_detector = OpenEyesDetect.getInstance()
        open_eyes_detector.detect_open_eyes()


alarm = OpenEyesAlarm("", "", "", "", "")
alarm.execute()
