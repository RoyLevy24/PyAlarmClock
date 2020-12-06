import sys
sys.path.append("./src/")


from screens.AlarmFormScreen import *
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from gui_strings import screen_helper, alarm_string
from kivy.properties import ListProperty, ObjectProperty
from kivymd.uix.picker import MDTimePicker
from kivy.core.window import Window
from datetime import datetime


Window.size = (360, 740)


class MainScreen(Screen, FloatLayout):

    def __init__(self, **kwargs): 
        super(MainScreen, self).__init__(**kwargs)
        self.alarm_list = []

    def delete_alarm(self, alarm_id):
        self.alarm_list = list(
            filter(
                lambda alarm: alarm.alarm_id != alarm_id,
                self.alarm_list
            )
        )

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
        print(self.ids)
        alarm_to_edit = self.find_alarm_by_id(self.alarm_list, alarm_id)
        
        alarm_form_screen = self.manager.screens[1]
        alarm_form_screen.form_toolbar.title = "Edit Alarm"
        alarm_form_screen.alarm_to_edit = alarm_to_edit

        self.manager.transition.direction = 'left'
        self.manager.current = 'alarm_form'

    def check_true_curr_weekday(self, screen):
        now = datetime.now()
        weekday = now.weekday()
        screen.check_days[weekday].active = True


class AlarmActiveScreen(Screen, FloatLayout):
    pass


class DismissSpeechScreen(Screen, FloatLayout):
    pass


class AlarmApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = 'Purple'
        screen = Builder.load_string(screen_helper)
        return screen

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MainScreen(name="main"))
sm.add_widget(AlarmFormScreen(name="alarm_form"))
# sm.add_widget(AlarmFormScreen())
# sm.add_widget(AlarmFormScreen())
AlarmApp().run()