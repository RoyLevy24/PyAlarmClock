import sys

sys.path.append("./src/")


from datetime import datetime

from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.picker import MDTimePicker

from gui_strings import alarm_string, screen_helper
from screens.AlarmActiveScreen import *
from screens.AlarmFormScreen import *
from screens.DismissSpeechScreen import *
from screens.MainScreen import *

from backend.Logic.LogicManager import *

Window.size = (360, 740)
# Create a screen manager


sm = ScreenManager()
sm.add_widget(MainScreen(name="main"))
sm.add_widget(AlarmFormScreen(name="alarm_form"))
sm.add_widget(AlarmActiveScreen(name="alarm_active"))
sm.add_widget(DismissSpeechScreen(name="dismiss_speech"))

class AlarmApp(MDApp):
    """
    This class is the entry-point of the application.
    It is responsible for initialization, and displaying the Main Screen.
    """

    def build(self):
        # sets color theme
        self.theme_cls.primary_palette = 'Purple'
        # create the main screen Widget
        screen_manager = Builder.load_string(screen_helper)
        main_screen = screen_manager.screens[0]
        logic_manger = LogicManager()
        main_screen.set_logic_manager(logic_manger)
        return screen_manager

AlarmApp().run()
