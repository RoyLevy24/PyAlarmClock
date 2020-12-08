import sys
sys.path.append("./src/")
from backend.OpenEyesDetection.OpenEyesDetect import *
from backend.AlarmClock.Alarm import *
import datetime

class OpenEyesAlarm(Alarm):

    def __init__(self, alarm_id, main_screen, time, days, description, staring_time, camera_num=0, ear=0.31):
        Alarm.__init__(self, alarm_id, main_screen, time, days, description)
        self.staring_time = staring_time
        self.camera_num = camera_num
        self.ear = ear

    def execute_alarm(self):
        open_eyes_detector = OpenEyesDetect.getInstance()
        open_eyes_detector.detect_open_eyes(self.staring_time, self.camera_num, self.ear)
        super(OpenEyesAlarm, self).execute_alarm()