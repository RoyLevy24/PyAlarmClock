import sys
sys.path.append("./src/")
from backend.OpenEyesDetection.OpenEyesDetect import *
from backend.AlarmClock.Alarm import *
import datetime

class OpenEyesAlarm(Alarm):

    def __init__(self, alarm_id, time, days, description, staring_time):
        Alarm.__init__(self, alarm_id, time, days, description)
        self.staring_time = staring_time

    def execute_alarm(self):
        open_eyes_detector = OpenEyesDetect.getInstance()
        open_eyes_detector.detect_open_eyes(self.staring_time)