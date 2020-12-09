from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.snackbar import Snackbar

class DismissSpeechScreen(Screen, FloatLayout):

    def __init__(self, **kwargs):
        super(DismissSpeechScreen, self).__init__(**kwargs)
        self.primary_light_color = (0.807843137254902, 0.5764705882352941, 0.8470588235294118, 1.0)

    def disable_speech_button(self):
        self.dismiss_speech_record.disabled = True

    def enable_speech_button(self):
        self.dismiss_speech_record.disabled = False

    def is_speech_button_enabled(self):
        return self.dismiss_speech_record.disabled == False

    def show_speech_fail_snackbar(self):
        """
        Shows snackbar that indicates the user failed to speak a word.
        """
        snackbar = Snackbar(text="Try Saying The Word Again")
        snackbar.show()

