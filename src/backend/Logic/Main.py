import datetime
import queue
import sys
import threading
import time


sys.path.append("./src/")

# from AlarmClock.Alarm import *
from AlarmClock.OpenEyesAlarm import *
from AlarmClock.SpeechAlarm import *


def create_alarm(time, days, description, ring, staring_time=None, num_words=None):
    alarm = None
    if staring_time:
        alarm = OpenEyesAlarm(time, days, description, ring, staring_time)
    else:
        alarm = SpeechAlarm(time, days, description, ring, num_words)
    return alarm


def add_alarm(time, days, description, ring, staring_time=None, num_words=None):
    # TODO: add alarm to external file
    alarm = create_alarm(time, days, description, ring, staring_time, num_words)
    alarm_list.append(alarm)


def delete_alarm(delete_index):
    # TODO: delete alarm to external file
    del alarm_list[delete_index]


def edit_alarm(edit_index, time, days, description, ring, staring_time=None, num_words=None):
    new_alarm = create_alarm(time, days, description, ring, staring_time, num_words)
    # TODO: edit alarm to external file
    alarm_list[edit_index] = new_alarm


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
                alarms_queue.put(alarm)
                time.sleep(60)
                


def execute_alarm():
    while True:
        alarm = alarms_queue.get()
        alarm.execute_alarm()

if __name__ == "__main__":
    alarm_list = []
    # mocking threading communication
    add_alarm(datetime.time(7,32), [Days.Mon], "mock_alarm","", num_words=6)
    
    alarms_queue = queue.Queue()
    alarm_time_checker = threading.Thread(
        target=nearly_active_alarm_checker, daemon=True)
    
    alarm_executer = threading.Thread(
        target=execute_alarm, daemon=True)

    alarm_time_checker.start()
    alarm_executer.start()

    alarm_time_checker.join()
    alarm_executer.join()