from datetime import datetime

from frontend.gui_strings import screen_helper
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDTimePicker


class MainScreen(Screen, FloatLayout):
    """
    This class represant the Main Screen of the Application.
    """

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.alarm_list = []

    def set_logic_manager(self, logic_manager):
        self.logic_manager = logic_manager
        # TODO: add set_main_screen to LogicManager
        self.logic_manager.set_main_screen(self)

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

    def close_delete_dialog(self, alarm_id, *args, delete=False):
        def close(*args):
            if delete:
                self.delete_alarm(alarm_id)
            self.delete_dialog.dismiss(force=True)
        return close

    def show_delete_alarm_dialog(self, alarm_id):
        """
        Shows a dialog that making sure that the user want to delete an alarm

        Args:
            alarm_id (String): the id of the alarm the user may or may not want to delete.
        """
        self.delete_dialog = MDDialog(
            title="Delete Alarm?",
            text="This alarm we no longer be active",
            pos_hint={"center_x":.5, "center_y":.5},
            size_hint_x=.8,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_press=self.close_delete_dialog(alarm_id, delete=False)
                    
                ),
                MDRaisedButton(
                    text="DELETE",
                    on_press=self.close_delete_dialog(alarm_id, delete=True)
                ),
            ],
        )
        self.delete_dialog.open()

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
        self.logic_manager.delete_alarm(alarm_id)


    def load_alarm_active_details(self, alarm_dict):
        """
        Loads the details of an alarm that needs to be ringed
        into the alarm active scree.

        Args:
            alarm_dict (dict): a dictionary containing the alarm's details.
        """
        # getting the screen
        alarm_active_screen = self.manager.screens[2]
        # setting up details
        alarm_active_screen.alarm_active_time.text = alarm_dict["time"]
        alarm_active_screen.alarm_active_desc.text = alarm_dict["description"]
        alarm_active_screen.alarm_active_dismiss.on_press = alarm_dict["dismiss_func"]
        # transitioning to the screen
        self.manager.transition.direction = 'left'
        self.manager.current = 'alarm_active'
