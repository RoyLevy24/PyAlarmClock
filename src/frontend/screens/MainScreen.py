import sys
sys.path.append("./src/")


from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from gui_strings import screen_helper
from kivy.properties import ListProperty, ObjectProperty
from kivymd.uix.picker import MDTimePicker
from kivy.core.window import Window
from datetime import datetime


class MainScreen(Screen, FloatLayout):

    def __init__(self, **kwargs): 
        super(MainScreen, self).__init__(**kwargs)
        self.alarm_list = []

    def delete_alarm(self, alarm_id):
        self.alarm_list = list(
            filter(
                lambda alarm: alarm["alarm_id"] != alarm_id,
                self.alarm_list
            )
        )
        self.ids.list.remove_widget(self.ids[alarm_id])

    def find_alarm_by_id(self, alarm_list, alarm_id):
        for alarm in alarm_list:
            if alarm["alarm_id"] == alarm_id:
                return alarm
        return None

    def create_alarm(self):
        # TODO: need to implement this screen
        # self.manager.current = "add_alarm"
        # alarm_item = Builder.load_string(alarm_string)
        # self.ids.list.add_widget(alarm_item)
        alarm_form_screen = self.manager.screens[1]
        alarm_form_screen.form_toolbar.title = "Add Alarm"
        self.check_true_curr_weekday(alarm_form_screen)
        self.manager.transition.direction = 'left'
        self.manager.current = 'alarm_form'

    def edit_alarm(self, alarm_id):
        alarm_to_edit = self.find_alarm_by_id(self.alarm_list, alarm_id)
        
        alarm_form_screen = self.manager.screens[1]
        alarm_form_screen.form_toolbar.title = "Edit Alarm"
        alarm_form_screen.alarm_to_edit = alarm_to_edit
        alarm_form_screen.load_alarm_to_edit_details()

        self.manager.transition.direction = 'left'
        self.manager.current = 'alarm_form'

    def check_true_curr_weekday(self, screen):
        now = datetime.now()
        weekday = now.weekday()
        screen.check_days[weekday].active = True
