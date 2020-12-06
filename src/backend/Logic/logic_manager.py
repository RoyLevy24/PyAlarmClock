import datetime
import queue
import sys
import threading
import time
sys.path.append("./src/")

from backend.AlarmClock.Alarm import *
from backend.AlarmClock.OpenEyesAlarm import *
from backend.AlarmClock.SpeechAlarm import *
from service.actions.actions_types import ACTIVE_ALARM
from service.MessageReducer import *


def create_alarm(alarm_id, time, days, description, staring_time=None, num_words=None):
    alarm = None
    if staring_time:
        alarm = OpenEyesAlarm(alarm_id, time, days, description, staring_time)
    else:
        alarm = SpeechAlarm(alarm_id, time, days, description, num_words)
    return alarm


def add_alarm(alarm_id, time, days, description, staring_time=None, num_words=None):
    alarm = create_alarm(alarm_id, time, days, description, staring_time, num_words)
    alarm_list.append(alarm)


def delete_alarm(alarm_id):
    alarm_list = list(filter(lambda alarm: alarm.alarm_id != alarm_id, alarm_list))


def edit_alarm(alarm_id, time, days, description, staring_time=None, num_words=None):
    to_edit_alarm = get_alarm_by_id(alarm_id)
    if to_edit_alarm != None:
        to_edit_alarm.time = time
        to_edit_alarm.days = days
        to_edit_alarm.description = description
        to_edit_alarm.staring_time = staring_time
        to_edit_alarm.num_words = num_words

def get_alarm_by_id(alarm_id):
    alarms = list(filter(lambda a: a.alarm_id == alarm_id, alarm_list))
    if len(alarms) > 0:
        return alarms[0]
    return None

def alarm_should_ring(curr_datetime, alarm):
    if alarm.rang_today:
        return False

    curr_day = curr_datetime.weekday()
    if Days(curr_day) not in alarm.days:
        return False

    alarm_datetime = datetime.datetime.combine(
        datetime.date.today(), alarm.time)
    time_delta = curr_datetime - alarm_datetime
    if 0 <= time_delta.seconds <= 60:
        alarm.rang_today = True
        return True


def nearly_active_alarm_checker():
    while True:
        curr_time = datetime.datetime.now().replace(second=0, microsecond=0)
        for alarm in alarm_list:
            if alarm_should_ring(curr_time, alarm):
                alarm_message = {"type": ACTIVE_ALARM, "payload": alarm}
                MessageReducer.getInstance().add_message(alarm_message)
                time.sleep(60)
                
alarm_list = []

# def execute_alarm():
#     while True:
#         alarm = alarms_queue.get()
#         alarm.execute_alarm()

# if __name__ == "__main__":
#     alarm_list = []
#     # mocking threading communication
#     add_alarm(datetime.time(7,32), [Days.Mon], "mock_alarm","", num_words=6)
    
#     alarms_queue = queue.Queue()
#     alarm_time_checker = threading.Thread(
#         target=nearly_active_alarm_checker, daemon=True)
    
#     alarm_executer = threading.Thread(
#         target=execute_alarm, daemon=True)

#     alarm_time_checker.start()
#     alarm_executer.start()

#     alarm_time_checker.join()
#     alarm_executer.join()