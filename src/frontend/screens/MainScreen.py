from datetime import datetime

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDTimePicker
from frontend.gui_strings import alarm_string
from service.utils import *
import weakref


class MainScreen(Screen, FloatLayout):
    """
    This class represant the Main Screen of the Application.
    """

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.alarm_list = []
        self.is_alarm_active = False

    def go_back_to_enter(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'enter'

    def set_logic_manager(self, logic_manager):
        self.logic_manager = logic_manager
        self.alarm_list = [self.get_alarm_dict(alarm) for alarm in logic_manager.alarm_list]
        self.set_alarm_widget_list()
        

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
        alarm_form_screen = self.manager.screens[2]
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
        alarm_form_screen = self.manager.screens[2]
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
            text="This alarm will no longer be active",
            pos_hint={"center_x": .5, "center_y": .5},
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
        alarm_active_screen = self.manager.screens[3]
        # setting up details
        alarm_active_screen.alarm_active_time.text = alarm_dict["time"]
        alarm_active_screen.alarm_active_desc.text = alarm_dict["description"]
        alarm_active_screen.alarm_active_dismiss.on_press = self.stop_ringtone_dismiss_func(
            alarm_active_screen, alarm_dict["dismiss_func"])

        alarm_active_screen.play_alarm_ringtone()
        # transitioning to the screen
        self.manager.transition.direction = 'left'
        self.manager.current = 'alarm_active'

    def stop_ringtone_dismiss_func(self, alarm_active_screen, dismiss_func):
        def dismiss():
            alarm_active_screen.stop_alarm_ringtone()
            dismiss_func()
        return dismiss

    def set_alarm_item_details(self, alarm_item, alarm_dict, days_str):
        """
        Sets the alarm details from the form in a Widget that later
        displayed on the main screen.

        Args:
            alarm_item (Widget): list item that displayed on the main screen 
        """
        alarm_item.name = alarm_dict["alarm_id"]
        alarm_item.text = alarm_dict["time"].strftime("%H:%M")
        alarm_item.secondary_text = alarm_dict["description"]
        alarm_item.tertiary_text = days_str

    def add_alarm_in_main(self, alarm_dict, add_to_list=False):
        """
        Adds an alarm to the main screen

        Args:
            alarm_dict (dict): dictionary contaning the alarm's details.
        """
        #main_screen = self.manager.screens[1]
        # getting a string represanting alarm days
        days_str = get_days_str(alarm_dict["days"])
        alarm_id = alarm_dict["alarm_id"]

        # Loading an alarm_item Kivy Widget
        alarm_item = Builder.load_string(alarm_string)
        self.set_alarm_item_details(alarm_item, alarm_dict, days_str)

        # adds the alarm to list in the main screen
        if(add_to_list):
            self.alarm_list.append(alarm_dict)
        # adds the alarm to the list view in the main screen
        self.ids.list.add_widget(alarm_item)
        # holding up a reference for the alarm widget for deletion
        self.ids[alarm_id] = weakref.proxy(alarm_item)

    def set_alarm_widget_list(self):
        for alarm in self.alarm_list:
            self.add_alarm_in_main(alarm)

    def get_alarm_type(self, alarm):
        staring_time = alarm.get("staring_time", None)
        num_words = alarm.get("num_words", None)
        if num_words != None:
            return (0, num_words)
        elif staring_time != None:
            return (1, staring_time)
        else:
            return (2, None)
    
    def get_alarm_dict(self, alarm):
        alarm_dict = alarm.__dict__
        alarm_dict["alarm_type"] = self.get_alarm_type(alarm_dict)
        return alarm_dict