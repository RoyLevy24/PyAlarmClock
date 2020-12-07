import sys
import weakref
sys.path.append("./src/")

from service.MessageReducer import *
from service.AlarmIdGenerator import *
from service.utils import *
from kivymd.uix.picker import MDTimePicker
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty, ObjectProperty
from kivy.lang.builder import Builder
from kivy.core.window import Window
from datetime import datetime
from gui_strings import alarm_string
from kivymd.uix.list import IconLeftWidget, IconRightWidget, ThreeLineAvatarIconListItem
from functools import partial
# from screens.MainScreen import edit_alarm, delete_alarm


class AlarmFormScreen(Screen, FloatLayout):
    time_picker = ObjectProperty(None)
    check_days = ListProperty([])

    def __init__(self, **kwargs):
        super(AlarmFormScreen, self).__init__(**kwargs)
        self.alarm_to_edit = None

#----------------------------------------reset actions--------------------------------------------#
    def reset_days(self):
        for day in self.check_days:
            day.active = False

    def check_true_curr_weekday(self):
        now = datetime.now()
        weekday = now.weekday()
        self.check_days[weekday].active = True

    def reset_types(self):
        for type_checkbox in self.check_type:
            type_checkbox.active = False
        self.check_type[2].active = True
        self.select_none_alarm()

    def reset_alarm_form(self):
        self.time_picker.text = "12:00"
        self.alarm_desc.text = ""
        self.reset_days()
        self.check_true_curr_weekday()
        self.reset_types()
        self.alarm_to_edit = None
#-------------------------------------------------------------------------------------------------#

#-------------------------------------transitions actions-----------------------------------------#
    def back_to_alarm_list(self):
        self.reset_alarm_form()
        self.manager.transition.direction = 'right'
        self.manager.current = 'main'

    def add_alarm(self):
        self.get_new_alarm_details()
        self.manager.transition.direction = 'up'
        self.manager.current = 'main'
#-------------------------------------------------------------------------------------------------#

#--------------------------------------input actions----------------------------------------------#

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

    def get_alarm_days_indexes(self):
        check_days = self.check_days
        days_idx = []
        for i in range(len(check_days)):
            if check_days[i].active:
                days_idx.append(i)
        return days_idx

    def get_alarm_type_index(self):
        check_type = self.check_type
        for i in range(len(check_type)):
            if check_type[i].active:
                return i
        return -1

    def check_valid_input(self):
        pass

    
    def load_time(self, time):
        time_str = time.strftime("%H:%M")
        self.time_picker.text = time_str
    
    def load_days(self, days):
        for day in days:
            self.check_days[day].active = True

    def load_description(self, description):
        self.alarm_desc.text = description

    def load_alarm_type(self, alarm_type):
        type_idx = alarm_type[0]
        type_param = alarm_type[1]

        for i in range(len(self.check_type)):
            if i == type_idx:
                self.check_type[i].active = True
            else:
                self.check_type[i].active = False

        self.tf_alarm_param.text = type_param


    def load_alarm_to_edit_details(self):
        print(self.alarm_to_edit)
        to_edit = self.alarm_to_edit
        self.load_time(to_edit["time"])
        self.load_days(to_edit["days"])
        self.load_description(to_edit["description"])
        self.load_alarm_type(to_edit["alarm_type"])

    def get_new_alarm_details(self):
        to_edit = self.alarm_to_edit
        alarm_id = AlarmIdGenerator.getInstance().get_next_id(
        ) if to_edit == None else to_edit["alarm_id"]
        time = datetime.strptime(self.time_picker.text, "%H:%M").time()
        days_idx = self.get_alarm_days_indexes()
        alarm_type_idx = self.get_alarm_type_index()
        tf_alarm_param = self.tf_alarm_param.text
        alarm_desc = self.alarm_desc.text

        alarm_dict = {
            "alarm_id": alarm_id,
            "time": time,
            "days": days_idx,
            "alarm_type": (alarm_type_idx, tf_alarm_param),
            "description": alarm_desc
        }

        if to_edit != None:
            self.update_alarm_in_main(alarm_dict)
        else:
            self.add_alarm_in_main(alarm_dict)
            self.reset_alarm_form()


        # message = {"type": ADD_ALARM, "payload": alarm_dict}
        # MessageReducer.getInstance().add_message(message)
#-------------------------------------------------------------------------------------------------#

    
    def set_alarm_details(self, alarm_item, alarm_dict, days_str):
        alarm_item.name = alarm_dict["alarm_id"]
        alarm_item.text = alarm_dict["time"].strftime("%H:%M")
        alarm_item.secondary_text = alarm_dict["description"]
        alarm_item.tertiary_text = days_str

    def add_alarm_in_main(self, alarm_dict):
        main_screen = self.manager.screens[0]
        days_str = get_days_str(alarm_dict["days"])
        alarm_id = alarm_dict["alarm_id"]

        alarm_item = Builder.load_string(alarm_string)
        self.set_alarm_details(alarm_item, alarm_dict, days_str)

        main_screen.alarm_list.append(alarm_dict)
        main_screen.ids.list.add_widget(alarm_item)
        main_screen.ids[alarm_id] = weakref.proxy(alarm_item)
        
    def update_alarm_in_main(self, alarm_dict):
        main_screen = self.manager.screens[0]
        days_str = get_days_str(alarm_dict["days"])
        alarm_id = alarm_dict["alarm_id"]

        alarm_item = main_screen.ids[alarm_id]
        self.set_alarm_details(alarm_item, alarm_dict, days_str)
        self.update_alarm_list_in_main(main_screen.alarm_list, alarm_dict)
        self.alarm_to_edit = None

    def update_alarm_list_in_main(self, alarm_list, alarm_dict):
        alarm_in_list = self.alarm_to_edit

        alarm_in_list["time"] = alarm_dict["time"]
        alarm_in_list["days"] = alarm_dict["days"]
        alarm_in_list["alarm_type"] = alarm_dict["alarm_type"]
        alarm_in_list["description"] = alarm_dict["description"]




