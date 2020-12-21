
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from pygame import mixer


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
        try:
            mixer.init()
            mixer.music.load("frontend/assets/alarm_clock_ringtone.mp3")
            mixer.music.play()
        except Exception:
            pass

    def stop_alarm_ringtone(self):
        """
        Stop playing ringtone in the background.
        """
        mixer.stop()
        mixer.quit()

    def dialog_close(self, *args):
        """
        Closes error dialog.
        """
        self.error_dialog.dismiss(force=True)

    def show_error_dialog(self, error_str):
        """
        Shows an error dialog when an exception is raised for invalid input.

        Args:
            error_str (String): Error to show in teh dialog.
        """
        self.error_dialog = MDDialog(
            text=error_str,
            pos_hint={"center_x": .5, "center_y": .5},
            size_hint_x=.8,
            buttons=[MDRaisedButton(
                text="DISCARD", on_press=self.dialog_close)]
        )
        self.error_dialog.open()
