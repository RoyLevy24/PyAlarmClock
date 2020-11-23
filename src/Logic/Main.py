import datetime
import queue
import sys
import threading

sys.path.append("./src/AlarmClock/")

from Alarm import *
from OpenEyesAlarm import *
from SpeechAlarm import *


def create_alarm(time, days, description, ring, frames=None, num_words=None):
    alarm = None
    if frames:
        alarm = OpenEyesAlarm(time, days, description, ring, frames)
    else:
        alarm = SpeechAlarm(time, days, description, ring, num_words)
    return alarm


def add_alarm(time, days, description, ring, frames=None, num_words=None):
    # TODO: add alarm to external file
    alarm = create_alarm(time, days, description, ring, frames, num_words)
    alarm_list.append(alarm)


def delete_alarm(delete_index):
    # TODO: delete alarm to external file
    del alarm_list[delete_index]


def edit_alarm(edit_index, time, days, description, ring, frames=None, num_words=None):
    new_alarm = create_alarm(time, days, description, ring, frames, num_words)
    # TODO: edit alarm to external file
    alarm_list[edit_index] = new_alarm


def alarm_should_ring(curr_datetime, alarm):
    if alarm.rang_today:
        return False

    curr_day = curr_time.weekday()
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
        curr_time = datetime.datetime.now()
        for alarm in alarm_list:
            if alarm_should_ring(curr_time, alarm):
                alarms_queue.put(alarm)


def execute_alarm():
    while True:
        if alarms_queue.qsize() > 0:
            alarm = alarms_queue.get()

if __name__ == "__main__":
    alarm_list = []
    alarms_queue = queue.Queue()
    alarm_time_checker = threading.Thread(
        target=nearly_active_alarm_checker)
    alarm_time_checker.start()
