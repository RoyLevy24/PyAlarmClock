import sys
sys.path.append("./src/")
from OpenEyesDetection.OpenEyesDetect import *
from AlarmClock.Alarm import *
import datetime

class OpenEyesAlarm(Alarm):

    def __init__(self, time, days, description, ring, staring_time):
        Alarm.__init__(self, time, days, description, ring)
        self.staring_time = staring_time
        Alarm.dismiss_function = self.dismiss_alarm

    def execute_alarm(self):
        super(OpenEyesAlarm, self).execute_alarm()

    def dismiss_alarm(self):
        open_eyes_detector = OpenEyesDetect.getInstance()
        open_eyes_detector.detect_open_eyes(self.staring_time)
