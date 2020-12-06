from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from gui_strings import screen_helper, alarm_string

from kivy.core.window import Window
Window.size = (360, 740)


class MainScreen(Screen, FloatLayout):

    def add_alarm(self):
        # TODO: need to implement this screen
        # self.manager.current = "add_alarm"
        alarm_item = Builder.load_string(alarm_string)
        self.ids.list.add_widget(alarm_item)



class AlarmFormScreen(Screen, FloatLayout):
    pass


class AlarmActiveScreen(Screen, FloatLayout):
    pass


class DismissSpeechScreen(Screen, FloatLayout):
    pass


# Create the screen manager
sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
sm.add_widget(AlarmFormScreen(name='alarm_form'))
sm.add_widget(AlarmFormScreen(name='alarm_active'))
sm.add_widget(AlarmFormScreen(name='dismiss_speech'))



class AlarmApp(MDApp):

    def build(self):
        screen = Builder.load_string(screen_helper)
        return screen


AlarmApp().run()