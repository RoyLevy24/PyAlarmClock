import weakref
from datetime import datetime

from frontend.gui_strings import alarm_string
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDTimePicker
from service.AlarmIdGenerator import *
from service.utils import *


class AlarmFormScreen(Screen, FloatLayout):
    """
    This class responsible for displaying add/edit form screen for the alarms.
    From this class the user can add/edit an alarm.
    """

    time_picker = ObjectProperty(None)
    check_days = ListProperty([])

    def __init__(self, **kwargs):
        super(AlarmFormScreen, self).__init__(**kwargs)
        self.alarm_to_edit = None
        self.MAX_DESC_SIZE = 25
        self.MAX_NUM_WORDS = 10
        self.MAX_STARE_TIME = 300

        self.SPEECH_TYPE = 0
        self.FACE_TYPE = 1
        self.NONE_TYPE = 2

#----------------------------------------reset actions--------------------------------------------#
    def reset_days(self):
        # unchecking all the checkboxes of the days
        for day in self.check_days:
            day.active = False

    def check_true_curr_weekday(self):
        # checks the checks box represanting the current day
        now = datetime.now()
        weekday = now.weekday()
        self.check_days[weekday].active = True

    def reset_types(self):
        # uncheck all the types checkboxes
        for type_checkbox in self.check_type:
            type_checkbox.active = False
        # checking the default checkbox (type None)
        self.check_type[self.NONE_TYPE].active = True
        # reseting text field of alarm type
        self.select_none_alarm()

    def reset_alarm_form(self):
        """
        Reseting all the details in the alarm form.
        """
        self.time_picker.text = "12:00"
        self.alarm_desc.text = ""
        self.reset_days()
        self.check_true_curr_weekday()
        self.reset_types()
        self.alarm_to_edit = None
#-------------------------------------------------------------------------------------------------#

#-------------------------------------transitions actions-----------------------------------------#
    def back_to_alarm_list(self):
        """
        Transitions into the MainScreen
        """
        self.reset_alarm_form()
        self.manager.transition.direction = 'right'
        self.manager.current = 'main'

    def add_alarm(self):
        """
        Adds/Edits an alarm to the MainScreen and then transition into it.
        """
        try:
            self.get_new_alarm_details()
            self.manager.transition.direction = 'up'
            self.manager.current = 'main'
        except Exception as e:
            # self.reset_alarm_form()
            self.show_error_dialog(str(e))

#-------------------------------------------------------------------------------------------------#

#--------------------------------------input actions----------------------------------------------#

    def select_alarm_type(self, hint_text="", disabled=True):
        """
        Sets up the text field for input regarding alarm type.
        """
        self.tf_alarm_param.disabled = disabled
        self.tf_alarm_param.text = ""
        self.tf_alarm_param.hint_text = hint_text

    def select_face_alarm(self):
        # setting text field for face alarm type
        self.select_alarm_type("Enter Staring Time (Seconds)", disabled=False)

    def select_speech_alarm(self):
        # setting text field for speech alarm type
        self.select_alarm_type("Enter Num of Words", disabled=False)

    def select_none_alarm(self):
        # setting text field for none alarm type
        self.select_alarm_type()

    def open_time_picker(self):
        """
        Opens up time picker dialog for selection of alarm time.
        """
        time_dialog = MDTimePicker()
        # getting the previous time text in the button
        previous_time = datetime.strptime(
            self.time_picker.text, '%H:%M').time()
        # setting the previous time in the dialog
        time_dialog.set_time(previous_time)
        # binds a method that sets the time chosen
        time_dialog.bind(time=self.get_time_picker_time)
        time_dialog.open()

    def get_time_picker_time(self, instance, time):
        """
        Sets the time chosen by the user in the form.
        """
        self.time_picker.text = time.strftime("%H:%M")

    def get_alarm_days_indexes(self):
        """
        Returns all the indexes of the days the use chose for the alarm
        """
        check_days = self.check_days
        days_idx = []
        for i in range(len(check_days)):
            if check_days[i].active:
                days_idx.append(i)
        return days_idx

    def get_alarm_type_index(self):
        """
        Returns the index of the type of alarm the user chose.
        Returns None if the user haven't chose any.
        """
        check_type = self.check_type
        for i in range(len(check_type)):
            if check_type[i].active:
                return i
        return None
#-------------------------------------validate input actions--------------------------------------#

    def check_valid_days(self, days):
        """
        Checks if the chosen days by the user is valid.

        Raises: 
            Exception: If the user have not chosen at least one day.
        """
        if len(days) == 0:
            raise Exception("You Must Select At Least One Day!")

    def check_valid_description(self, description):
        """
        Checks if the alarm description entered by the user is valid

        Raises:
            Exception: If the description entered by the user is exceeding the max_desc_size.
        """
        if len(description) > self.MAX_DESC_SIZE:
            raise Exception(f'Max Description Length is {self.MAX_DESC_SIZE}!')

    def check_valid_num_words(self, num_words):
        """
        Checks if the number of words for speech_alarm entered by the user is valid.

        Raises: 
            Exception: if @num_words is not a non-negative integer or exceeds MAX_NUM_WORDS.
        """
        if not is_positive_int(num_words):
            raise Exception("Num Words Must be a positive int!")

        else:
            num_words = int(num_words)
            if num_words > self.MAX_NUM_WORDS:
                raise Exception(f'Max Num of Words is {self.MAX_NUM_WORDS}!')

    def check_valid_stare_time(self, stare_time):
        """
        Checks if the staring time for face_alarm entered by the user is valid.

        Raises: 
            Exception: if @stare_time is not a non-negative integer or exceeds MAX_STARE_TIME.
        """
        if not is_positive_int(stare_time):
            raise Exception("Staring Time Must be a positive int!")

        else:
            stare_time = int(stare_time)
            if stare_time > self.MAX_STARE_TIME:
                raise Exception(f'Max Staring Time is {self.MAX_STARE_TIME}!')

    def check_valid_alarm_type(self, alarm_type):
        """
        Checks if the alarm_type entered by the user is valid.
        """
        alarm_type_idx = alarm_type[0]
        if alarm_type_idx == None:
            raise Exception("You Must Select an Alarm Type!")

        alarm_type_param = alarm_type[1]

        if alarm_type_idx == self.SPEECH_TYPE:
            self.check_valid_num_words(alarm_type_param)
        elif alarm_type_idx == self.FACE_TYPE:
            self.check_valid_stare_time(alarm_type_param)

    def check_valid_input(self, alarm_dict):
        """
        Checks if the parametes entered by the user for an alarm is valid.

        Args:
            alarm_dict (dict): A dictionary containing the alarm details

        Raises:
            Exception: If the alarm details in @alarm_dict are not valid.
        """
        self.check_valid_days(alarm_dict["days"])
        self.check_valid_description(alarm_dict["description"])
        self.check_valid_alarm_type(alarm_dict["alarm_type"])

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

#-------------------------------------------------------------------------------------------------#

#-----------------------------------update view actions-------------------------------------------#
    def load_time(self, time):
        """
        Loads a time to the form.

        Args:
            time (datetime.time): time to show in the form.
        """
        time_str = time.strftime("%H:%M")
        self.time_picker.text = time_str

    def load_days(self, days):
        """
        Checks all checkboxes of the days in the form based upon a given indexes for the days.
        """
        for i in range(7):
            if i in days:
                self.check_days[i].active = True
            else:
                self.check_days[i].active = False

    def load_description(self, description):
        """
        Loads a description to the form
        """
        self.alarm_desc.text = description

    def load_alarm_type(self, alarm_type):
        """
        Checks a checkbox of a given alarm type and inserting the given param string for the type.
        """
        type_idx = alarm_type[0]
        type_param = alarm_type[1]
        # checking true the alarm type checkbox
        for i in range(len(self.check_type)):
            if i == type_idx:
                self.check_type[i].active = True
                if i != self.NONE_TYPE:
                    self.tf_alarm_param.disabled = False
            else:
                self.check_type[i].active = False
        # setting the param string in the form
        self.tf_alarm_param.text = type_param

    def load_alarm_to_edit_details(self):
        """
        Loads alarm details for alarm ready to be edited.
        """
        to_edit = self.alarm_to_edit
        self.load_time(to_edit["time"])
        self.load_days(to_edit["days"])
        self.load_description(to_edit["description"])
        self.load_alarm_type(to_edit["alarm_type"])

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

    def add_alarm_in_main(self, alarm_dict):
        """
        Adds an alarm to the main screen

        Args:
            alarm_dict (dict): dictionary contaning the alarm's details.
        """
        main_screen = self.manager.screens[1]
        # getting a string represanting alarm days
        days_str = get_days_str(alarm_dict["days"])
        alarm_id = alarm_dict["alarm_id"]

        # Loading an alarm_item Kivy Widget
        alarm_item = Builder.load_string(alarm_string)
        self.set_alarm_item_details(alarm_item, alarm_dict, days_str)

        # adds the alarm to list in the main screen
        main_screen.alarm_list.append(alarm_dict)
        # adds the alarm to the list view in the main screen
        main_screen.ids.list.add_widget(alarm_item)
        # holding up a reference for the alarm widget for deletion
        main_screen.ids[alarm_id] = weakref.proxy(alarm_item)

    def update_alarm_in_main(self, alarm_dict):
        """
        Edits an alarm in the main screen

        Args:
            alarm_dict (dict): dictionary contaning the alarm's details.
        """
        main_screen = self.manager.screens[1]
        days_str = get_days_str(alarm_dict["days"])
        alarm_id = alarm_dict["alarm_id"]

        alarm_item = main_screen.ids[alarm_id]
        self.set_alarm_item_details(alarm_item, alarm_dict, days_str)
        self.update_alarm_list_in_main(alarm_dict)
        # indicates that we finished editing the alarm
        self.alarm_to_edit = None

    def update_alarm_list_in_main(self, alarm_dict):
        """
        Updating an alarm_item Widget in the main screen.

        Args:
            alarm_dict (dict): dictionary contaning the alarm's details.
        """
        alarm_in_list = self.alarm_to_edit

        alarm_in_list["time"] = alarm_dict["time"]
        alarm_in_list["days"] = alarm_dict["days"]
        alarm_in_list["alarm_type"] = alarm_dict["alarm_type"]
        alarm_in_list["description"] = alarm_dict["description"]

#-------------------------------------------------------------------------------------------------#

#----------------------------------form screen main actions---------------------------------------#

    def get_new_alarm_details(self):
        """
        Gets the alarm details the user entered from the form.

        Raises:
            Exception: If the details the user entered are not valid.
        """
        to_edit = self.alarm_to_edit
        alarm_id = AlarmIdGenerator.getInstance().get_next_id(
        ) if to_edit == None else to_edit["alarm_id"]
        time = datetime.strptime(self.time_picker.text, "%H:%M").time()
        days_idx = self.get_alarm_days_indexes()
        alarm_type_idx = self.get_alarm_type_index()
        tf_alarm_param = self.tf_alarm_param.text
        alarm_desc = self.alarm_desc.text

        alarm_dict = {
            "alarm_id": alarm_id,
            "time": time,
            "days": days_idx,
            "alarm_type": (alarm_type_idx, tf_alarm_param),
            "description": alarm_desc
        }

        self.check_valid_input(alarm_dict)
        alarm_params = self.create_alarm_params_for_logic(alarm_dict)
        main_screen = self.manager.screens[1]

        # performing create/edit alarm in the logic
        if to_edit != None:
            self.update_alarm_in_main(alarm_dict)
            main_screen.logic_manager.edit_alarm(*alarm_params)
        else:
            self.add_alarm_in_main(alarm_dict)
            main_screen.logic_manager.add_alarm(*alarm_params)
            self.reset_alarm_form()

    def create_alarm_params_for_logic(self, alarm_dict):
        """
        Transform a dictionary contating alarm details to list of
        parameters suitable to transfer to the LogicManager
        """
        alarm_id = alarm_dict["alarm_id"]
        time = alarm_dict["time"]
        days = alarm_dict["days"]
        description = alarm_dict["description"]
        (staring_time, num_words) = self.extract_alarm_type_params(
            alarm_dict["alarm_type"])

        return [alarm_id, time, days, description, staring_time, num_words]

    def extract_alarm_type_params(self, alarm_type):
        """
        Returns a tuple containing staring time and number of words for an alarm.
        At least one them we bill returned as None.
        """
        type_num = alarm_type[0]
        type_param = alarm_type[1]
        staring_time = None
        num_words = None

        if type_num == self.SPEECH_TYPE:
            num_words = int(type_param)
        elif type_num == self.FACE_TYPE:
            staring_time = int(type_param)

        return (staring_time, num_words)

#-------------------------------------------------------------------------------------------------#
