import datetime
import queue
import threading
import time

from backend.AlarmClock.Alarm import *
from backend.AlarmClock.OpenEyesAlarm import *
from backend.AlarmClock.SpeechAlarm import *


class LogicManager():
    """
    This class represents main logic bridge between the GUI and domain components.
    """

    def __init__(self, args):
        """
        Creates a new LogicManager

        Args:
            args: command line arguments.
        """
        self.args = args
        self.alarm_list = []
        self.alarms_queue = queue.Queue()
        self.init_threads()

    def set_main_screen(self, main_screen):
        self.main_screen = main_screen

    def init_threads(self):
        """
        Creating deamon threads for checking nearly active alarms, and executing them.
        """

        # time checking thread
        self.alarm_time_checker = threading.Thread(
            target=self.nearly_active_alarm_checker, daemon=True)

        # alarm executor thread
        self.alarm_executer = threading.Thread(
            target=self.execute_alarm, daemon=True)

        # starting the threads
        self.alarm_time_checker.start()
        self.alarm_executer.start()

    def create_alarm(self, alarm_id, time, days, description, staring_time=None, num_words=None):
        """
        Creates a new alarm.
        Args:
            alarm_id (String): unique identifier for the alarm.
            time (datetime.time): time for the alarm to ring.
            days (list(int)): days indexes for the days the alarm should ring.
            description (String): description of the alarm.
            staring_time (int): time in seconds the user needs to open his eyes for the alarm to dismiss.
            num_words (int): number of words the user to pronounce in order to dismiss the alarm.

        Returns a newly created alarm based on the parametes given.
        """

        alarm = None
        if staring_time:
            alarm = OpenEyesAlarm(alarm_id, self.main_screen, time, days,
                                  description, staring_time, camera_num=self.args.camera_num, ear=self.args.ear)
        elif num_words:
            alarm = SpeechAlarm(alarm_id, self.main_screen,
                                time, days, description, num_words, mic_num=self.args.microphone_num, sim_thresh=self.args.sim_thresh)

        else:
            alarm = Alarm(alarm_id, self.main_screen, time, days, description)

        return alarm

    def add_alarm(self, alarm_id, time, days, description, staring_time=None, num_words=None):
        """
        Adds a new alarm to the alarms list.

        Args:
            alarm_id (String): unique identifier for the alarm.
            time (datetime.time): time for the alarm to ring.
            days (list(int)): days indexes for the days the alarm should ring.
            description (String): description of the alarm.
            staring_time (int): time in seconds the user needs to open his eyes for the alarm to dismiss.
            num_words (int): number of words the user to pronounce in order to dismiss the alarm.     
        """
        alarm = self.create_alarm(
            alarm_id, time, days, description, staring_time, num_words)
        self.alarm_list.append(alarm)

    def delete_alarm(self, alarm_id):
        """
        Deletes an alarm from the alarm list.

        Args:
            alarm_id (String): unique identifier of the alarm to delete.
        """
        self.alarm_list = list(
            filter(lambda alarm: alarm.alarm_id != alarm_id, self.alarm_list))

    def edit_alarm(self, alarm_id, time, days, description, staring_time=None, num_words=None):
        """
        Edits an existing alarm in the alarm list.

        Args:
            alarm_id (String): unique identifier for the alarm to edit.
            time (datetime.time): time for the alarm to ring.
            days (list(int)): days indexes for the days the alarm should ring.
            description (String): description of the alarm.
            staring_time (int): time in seconds the user needs to open his eyes for the alarm to dismiss.
            num_words (int): number of words the user to pronounce in order to dismiss the alarm.     
        """
        alarm_idx = self.get_alarm_index_by_id(alarm_id)
        if alarm_idx != -1:
            # creates a new alarm instead of the old one with the params given
            self.alarm_list[alarm_idx] = self.create_alarm(
                alarm_id, time, days, description, staring_time, num_words)

    def get_alarm_index_by_id(self, alarm_id):
        """
        Retruns the index of an alarm with @alarm_id in the alarm_list, -1 if not exist.

        Args:
            alarm_id (String): unique identifier for the alarm to return his index.
        """
        for i in range(len(self.alarm_list)):
            if self.alarm_list[i].alarm_id == alarm_id:
                return i
        return -1

    def alarm_should_ring(self, curr_datetime, alarm):
        """
        Checks if an alarm should ring.

        Args:
            curr_datetime (datetime): current system time.
            alarm (Alarm): an alarm clock to check if should ring

        Retruns: True if the alarm should ring, False otherwise.
        """
        # checking if the alarm already rang today
        if alarm.rang_today:
            return False

        # checking if the alarm is for today
        curr_day = curr_datetime.weekday()
        if curr_day not in alarm.days:
            return False

        # checking if the alarm should ring now
        alarm_datetime = datetime.datetime.combine(
            datetime.date.today(), alarm.time)
        time_delta = curr_datetime - alarm_datetime
        if 0 <= time_delta.seconds <= 60:
            alarm.rang_today = True
            return True

    def nearly_active_alarm_checker(self):
        """
        Function to time checker thread.
        Checks if there are alarms that should ring soon.
        """
        while True:
            time.sleep(1)
            curr_time = datetime.datetime.now().replace(second=0, microsecond=0)
            for alarm in self.alarm_list:
                if self.alarm_should_ring(curr_time, alarm):
                    self.alarms_queue.put(alarm)
                    time.sleep(60)

    def execute_alarm(self):
        """
        Function for alarm executor thread.
        Transition the user to dismiss screen, and sets up details for alarm execution.
        """
        while True:
            alarm = self.alarms_queue.get()
            alarm_details_dict = {
                "time": alarm.time.strftime("%H:%M"),
                "description": alarm.description,
                "dismiss_func": alarm.execute_alarm,
            }
            self.main_screen.load_alarm_active_details(alarm_details_dict)
