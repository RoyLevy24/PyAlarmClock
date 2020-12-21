from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.snackbar import Snackbar

class DismissSpeechScreen(Screen, FloatLayout):

    def __init__(self, **kwargs):
        super(DismissSpeechScreen, self).__init__(**kwargs)
        self.speech_button = True

    def disable_speech_button(self):
        self.speech_button = False

    def enable_speech_button(self):
        self.speech_button = True

    def is_speech_button_enabled(self):
        return self.speech_buttonP

    def show_speech_fail_snackbar(self):
        """
        Shows snackbar that indicates the user failed to speak a word.
        """
        snackbar = Snackbar(text="Try Saying The Word Again")
        snackbar.show()

