from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty, ObjectProperty
from kivymd.uix.picker import MDTimePicker
from kivy.core.window import Window
from datetime import datetime
from service.MessageReducer import *

class AlarmFormScreen(Screen, FloatLayout):
    time_picker = ObjectProperty(None)
    # check_face = ObjectProperty(None)
    check_days = ListProperty([])

    def back_to_alarm_list(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'main'
    
    def add_alarm(self):
        self.get_new_alarm_details()
        self.manager.transition.direction = 'up'
        self.manager.current = 'main'

    def select_alarm(self, hint_text="", disabled=True):
        self.tf_alarm_param.disabled = disabled
        self.tf_alarm_param.text = ""
        self.tf_alarm_param.hint_text = hint_text

    def select_face_alarm(self):
        self.select_alarm("Enter Staring Time (Seconds)", disabled=False)

    def select_speech_alarm(self):
        self.select_alarm("Enter Num of Words", disabled=False)

    def select_none_alarm(self):
        self.select_alarm()

    def open_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time_picker_time)
        time_dialog.open()

    def get_time_picker_time(self, instance, time):
        self.time_picker.text = time.strftime("%H:%M")
    
    def check_true_curr_weekday(self):
        now = datetime.now()
        weekday = now.weekday()
        self.check_days[weekday].active = True

    def get_alarm_days_indexes(self):
        check_days = self.check_days
        days_idx = []
        for i in range(len(check_days)):
            if check_days[i].active:
                days_idx.append(i)
        # TODO: create error popup
        if len(days_idx) == 0:
            raise Exception("No day selected")
        return days_idx
    
    def get_alarm_type(self):
        check_type = self.check_type
        for type_checkbox in check_type:
            if type_checkbox.active:
                return type_checkbox.name

    def reset_types(self):
        for type_checkbox in self.check_type:
            type_checkbox.active = False
        self.check_type[2].active = True
        self.select_none_alarm()

    def reset_alarm_form(self):
        self.time_picker.text = "12:00"
        for day in self.check_days:
            day.active = False
        self.check_true_curr_weekday()
        self.reset_types()

    # def get_new_alarm_details(self):
    #     time = datetime.strptime(self.time_picker.text, "%H:%M").time()
    #     days_idx = self.get_alarm_days_indexes()
    #     alarm_type = self.get_alarm_type()
    #     tf_alarm_param = self.tf_alarm_param.text

    #     alarm_dict = {
    #         "alarm_id": "ADDDDDDDDDDDD",
    #         "time": time,
    #         "days": days_idx,
    #         alarm_arg: tf_alarm_param,
    #         "description": "ADDDDDDD"
    #     }
    #     message = {"type": ADD_ALARM, "payload": alarm_dict}
    #     MessageReducer.getInstance().add_message(message)
    #     self.reset_alarm_form()