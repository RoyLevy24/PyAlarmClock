import datetime
import queue
import threading
import time
import json

from backend.AlarmClock.Alarm import *
from backend.AlarmClock.OpenEyesAlarm import *
from backend.AlarmClock.SpeechAlarm import *


class LogicManager():
    """
    This class represents main logic bridge between the GUI and domain components.
    """
    
    def __init__(self, args, main_screen):
        """
        Creates a new LogicManager

        Args:
            args: command line arguments.
        """
        self.args = args
        self.main_screen = main_screen
        self.data_file_path = "data.json"
        self.alarm_list = self.get_alarm_list_from_file()
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
        self.write_alarms_to_file()

    def delete_alarm(self, alarm_id):
        """
        Deletes an alarm from the alarm list.

        Args:
            alarm_id (String): unique identifier of the alarm to delete.
        """
        self.alarm_list = list(
            filter(lambda alarm: alarm.alarm_id != alarm_id, self.alarm_list))
        self.write_alarms_to_file()

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
            self.write_alarms_to_file()

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
            time.sleep(0.001)
            curr_time = datetime.datetime.now().replace(second=0, microsecond=0)
            for alarm in self.alarm_list:
                if self.alarm_should_ring(curr_time, alarm):
                    self.alarms_queue.put(alarm)

    def execute_alarm(self):
        """
        Function for alarm executor thread.
        Transition the user to dismiss screen, and sets up details for alarm execution.
        """
        while True:
            time.sleep(0.001)
            # busy wating if alarm is currently executing
            if hasattr(self, 'main_screen') and self.main_screen.is_alarm_active == False:
                alarm = self.alarms_queue.get()
                alarm_details_dict = {
                    "time": alarm.time.strftime("%H:%M"),
                    "description": alarm.description,
                    "dismiss_func": alarm.execute_alarm,
                }
                self.main_screen.load_alarm_active_details(alarm_details_dict)
                self.main_screen.is_alarm_active = True

    def create_serilizable_alarm(self, alarm):
        """
        creates dictionary represanting the alarm object

        Args:
            alarm (Alarm): an alarm clock to create the dictionary from.
        
        Returns: a dictionary represanting the alarm object.

        """
        alarm_dict = alarm.__dict__.copy()
        alarm_dict['time'] = str(alarm_dict['time'])
        del alarm_dict['main_screen']
        return alarm_dict

    def write_alarms_to_file(self):
        """
        saves the alarm list to the json file
        """
        alarm_dict_list = [self.create_serilizable_alarm(alarm) for alarm in self.alarm_list]
        with open(self.data_file_path, 'w', encoding='utf-8') as f:
            f.seek(0)
            json.dump(alarm_dict_list, f, ensure_ascii=False, indent=4)

    def get_alarm_list_from_file(self):
        """
        Read the alarm list from the json file
        
        Returns: a list of Alarm objects

        """
        try:
            with open(self.data_file_path) as f:
                alarm_json_list = json.load(f)
            alarm_list = []
            for alarm in alarm_json_list:
                alarm_list.append(self.create_alarm(alarm["alarm_id"], datetime.datetime.strptime(alarm["time"], '%H:%M:%S').time(), alarm["days"], alarm["description"], alarm.get("staring_time", None), alarm.get("num_words", None)))
            return alarm_list
        except FileNotFoundError:
            return []


