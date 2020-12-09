import sys
sys.path.append("./src/")
from backend.OpenEyesDetection.OpenEyesDetect import *
from backend.AlarmClock.Alarm import *
import datetime

class OpenEyesAlarm(Alarm):
    """
    This class represents Face Detection Alarm
    """

    def __init__(self, alarm_id, main_screen, time, days, description, staring_time, camera_num=0, ear=0.31):
        """
        Creates a new OpenEyesAlarm.

        Args:
            alarm_id (String): unique identifier for the alarm.
            main_screen (Screen): screen to return to after the alarm is done executing.
            time (datetime.time): time for the alarm to ring.
            days (list(int)): days indexes for the days the alarm should ring.
            description (String): description of the alarm.
            staring_time (int): time in seconds the user needs to open his eyes for the alarm to dismiss.
            camera_num (int), default=0: camera device number the alarm uses to detect open eyes.
            ear (float), default=0.31: eye aspect ratio threshold to detect open eyes.
        """
        
        Alarm.__init__(self, alarm_id, main_screen, time, days, description)
        self.staring_time = staring_time
        self.camera_num = camera_num
        self.ear = ear

    def execute_alarm(self):
        """
        Invokes open eyes detection algorithm for the staring time the user entered. 
        """
        open_eyes_detector = OpenEyesDetect.getInstance()
        open_eyes_detector.detect_open_eyes(self.staring_time, self.camera_num, self.ear)
        # navigating the user to the main screen
        super(OpenEyesAlarm, self).execute_alarm()