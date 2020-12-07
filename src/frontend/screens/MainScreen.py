import sys

sys.path.append("./src/")

from kivymd.uix.picker import MDTimePicker
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty, ObjectProperty
from kivy.lang.builder import Builder
from kivy.core.window import Window
from gui_strings import screen_helper
from datetime import datetime


class MainScreen(Screen, FloatLayout):
    """
    This class represant the Main Screen of the Application.
    """

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.alarm_list = []

    def find_alarm_by_id(self, alarm_list, alarm_id):
        """
        Finds an alarm in list by a given alarm_id

        Args:
            alarm_list (list(dict)): List of alarms presented as a dictionary.
            alarm_id (String): The alarm_id of the alarm to be returned.

        Returns:
            The alarm with id of @alarm_id, None if it doesn't exists.
        """
        for alarm in alarm_list:
            if alarm["alarm_id"] == alarm_id:
                return alarm
        return None

    def create_alarm(self):
        """
        Creates alarm and adds it to the main screen
        """
        # get the alarm_form screen
        alarm_form_screen = self.manager.screens[1]
        alarm_form_screen.form_toolbar.title = "Add Alarm"
        alarm_form_screen.check_true_curr_weekday()

        # transition to alarm_form screen
        self.manager.transition.direction = 'left'
        self.manager.current = 'alarm_form'

    def edit_alarm(self, alarm_id):
        """
        Edits an alarm with a given alarm_id and present it in the main screen.
        """
        alarm_to_edit = self.find_alarm_by_id(self.alarm_list, alarm_id)

        # get the alarm_form screen
        alarm_form_screen = self.manager.screens[1]
        alarm_form_screen.form_toolbar.title = "Edit Alarm"
        # set alarm_to_edit in the alarm_form
        alarm_form_screen.alarm_to_edit = alarm_to_edit
        # loading alarm to edit details in the alarm_form
        alarm_form_screen.load_alarm_to_edit_details()

        # transition to alarm_form screen
        self.manager.transition.direction = 'left'
        self.manager.current = 'alarm_form'

    def delete_alarm(self, alarm_id):
        """
        Deletes an alarm with a given alarm_id from the main screen
        """

        # removes the alarm from the screen's alarm_list
        self.alarm_list = list(
            filter(
                lambda alarm: alarm["alarm_id"] != alarm_id,
                self.alarm_list
            )
        )
        # removes the alarm from the screen's view
        self.ids.list.remove_widget(self.ids[alarm_id])
