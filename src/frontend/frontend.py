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

    def create_alarm(self):
        # TODO: need to implement this screen
        # self.manager.current = "add_alarm"
        # alarm_item = Builder.load_string(alarm_string)
        # self.ids.list.add_widget(alarm_item)
        self.manager.transition.direction = 'left'
        self.manager.current = 'alarm_form'






class AlarmActiveScreen(Screen, FloatLayout):
    pass


class DismissSpeechScreen(Screen, FloatLayout):
    pass


class AlarmApp(MDApp):

    def build(self):
        screen = Builder.load_string(screen_helper)
        return screen

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MainScreen())
sm.add_widget(AlarmFormScreen())
sm.add_widget(AlarmFormScreen())
sm.add_widget(AlarmFormScreen())
AlarmApp().run()