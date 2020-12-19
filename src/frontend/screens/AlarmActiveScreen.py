from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from pygame import mixer
import sys


class AlarmActiveScreen(Screen, FloatLayout):
    """
    This class represents the alarm active screen
    """


    def __init__(self, **kwargs):
        super(AlarmActiveScreen, self).__init__(**kwargs)

    def play_alarm_ringtone(self):
        """
        Starting playing ringtone in the background.
        """
        mixer.init()
        mixer.music.load("frontend/assets/alarm_clock_ringtone.mp3")
        mixer.music.play()

    def stop_alarm_ringtone(self):
        """
        Stop playing ringtone in the background.
        """
        mixer.stop()
        mixer.quit()
