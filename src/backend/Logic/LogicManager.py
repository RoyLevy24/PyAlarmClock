import sys
sys.path.append("./src/")

from backend.AlarmClock.SpeechAlarm import *
from backend.AlarmClock.OpenEyesAlarm import *
from backend.AlarmClock.Alarm import *
import datetime
import queue
import threading
import time



class LogicManager():

    def __init__(self):
        self.alarm_list = []
        self.alarms_queue = queue.Queue()
        self.init_threads() 

    def set_main_screen(self, main_screen):
        self.main_screen = main_screen

    def init_threads(self):
        self.alarm_time_checker = threading.Thread(
            target=self.nearly_active_alarm_checker, daemon=True)

        self.alarm_executer = threading.Thread(
            target=self.execute_alarm, daemon=True)

        self.alarm_time_checker.start()
        self.alarm_executer.start()

        # self.alarm_time_checker.join()
        # self.alarm_executer.join()


    def create_alarm(self, alarm_id, time, days, description, staring_time=None, num_words=None):
        alarm = None
        if staring_time:
            alarm = OpenEyesAlarm(alarm_id, self.main_screen, time, days,
                                  description, staring_time)
        elif num_words:
            alarm = SpeechAlarm(alarm_id, self.main_screen, time, days, description, num_words)
        
        else:
            alarm = Alarm(alarm_id, self.main_screen, time, days, description)
        
        return alarm

    def add_alarm(self, alarm_id, time, days, description, staring_time=None, num_words=None):
        alarm = self.create_alarm(
            alarm_id, time, days, description, staring_time, num_words)
        self.alarm_list.append(alarm)

    def delete_alarm(self, alarm_id):
        self.alarm_list = list(
            filter(lambda alarm: alarm.alarm_id != alarm_id, self.alarm_list))

    def edit_alarm(self, alarm_id, time, days, description, staring_time=None, num_words=None):
        alarm_idx = self.get_alarm_index_by_id(alarm_id)
        if alarm_idx != -1:
            self.alarm_list[alarm_idx] = self.create_alarm(
            alarm_id, time, days, description, staring_time, num_words)



    def get_alarm_by_id(self, alarm_id):
        alarms = list(filter(lambda a: a.alarm_id ==
                             alarm_id, self.alarm_list))
        if len(alarms) > 0:
            return alarms[0]
        return None

    def get_alarm_index_by_id(self, alarm_id):
        for i in range(len(self.alarm_list)):
            if self.alarm_list[i].alarm_id == alarm_id:
                return i
        return -1

    def alarm_should_ring(self, curr_datetime, alarm):
        if alarm.rang_today:
            return False

        curr_day = curr_datetime.weekday()
        if curr_day not in alarm.days:
            return False

        alarm_datetime = datetime.datetime.combine(
            datetime.date.today(), alarm.time)
        time_delta = curr_datetime - alarm_datetime
        if 0 <= time_delta.seconds <= 60:
            alarm.rang_today = True
            return True

    def nearly_active_alarm_checker(self):
        while True:
            curr_time = datetime.datetime.now().replace(second=0, microsecond=0)
            for alarm in self.alarm_list:
                if self.alarm_should_ring(curr_time, alarm):
                    self.alarms_queue.put(alarm)
                    time.sleep(60)

    def execute_alarm(self):
        while True:
            alarm = self.alarms_queue.get()
            alarm_details_dict = {
                "time": alarm.time.strftime("%H:%M"),
                "description": alarm.description,
                "dismiss_func": alarm.execute_alarm,
            }
            self.main_screen.load_alarm_active_details(alarm_details_dict)