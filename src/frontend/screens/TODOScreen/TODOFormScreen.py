from datetime import datetime

from frontend.gui_strings import todo_string
from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import ILeftBodyTouch, TwoLineAvatarIconListItem
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.selectioncontrol import MDCheckbox
from service.TODOIdGenerator import *


class TODOFormScreen(Screen, FloatLayout):
    """
    This class responsibility is to give the user option to add a todo task.
    """

    def __init__(self, **kwargs):
        super(TODOFormScreen, self).__init__(**kwargs)
        self.MAX_DESC_SIZE = 25
        self.error_dialog = None
        self.add_dialog = None

    def reset_todo_form(self):
        """
        Loads the current date to the todo form and sets the description to empty string.
        """
        self.load_curr_date()
        self.todo_desc.text = ""
#---------------------------------------toolbar actions-------------------------------------------#

    def back_to_todo_list(self):
        """
        Transition into the TODOScreen
        """
        self.reset_todo_form()
        self.manager.transition.direction = 'right'
        self.manager.current = 'todo'

    def add_todo(self):
        """
        Add todo task in the TODOScreen
        """
        try:
            self.get_todo_details()
        except Exception as e:
            self.show_error_dialog(str(e))
            print(str(e))
#-------------------------------------------------------------------------------------------------#

#---------------------------------------dialogs actions-------------------------------------------#
    def add_dialog_close(self, *args):
        """
        Closes add todo dialog
        """
        self.add_dialog.dismiss(force=True)

    def show_add_dialog(self):
        """
        Shows a dialog when a todo is added successfully.
        """
        if not self.add_dialog:
            self.add_dialog = MDDialog(
                text="TODO Added!",
                pos_hint={"center_x": .5, "center_y": .5},
                size_hint_x=.8,
                buttons=[MDRaisedButton(
                    text="DISCARD", on_press=self.add_dialog_close)]
            )
        self.add_dialog.open()

    def error_dialog_close(self, *args):
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
                text="DISCARD", on_press=self.error_dialog_close)]
        )
        self.error_dialog.open()

#-------------------------------------------------------------------------------------------------#

#-----------------------------------input validation actions--------------------------------------#
    def check_valid_description(self, description):
        """
        Checks if the todo description entered by the user is valid

        Raises:
            Exception: If the description entered by the user is exceeding the max_desc_size or is empty.
        """
        if description == "" or len(description) > self.MAX_DESC_SIZE:
            raise Exception(
                f'Description Length Must be Between 1 to {self.MAX_DESC_SIZE}')

    def check_valid_input(self, todo_dict):
        """
        Checks if the parameters entered by the user for a todo are valid

        Args:
            todo_dict (dict): A dictionary contaning todo details.

        Raises:
            Exception: If the todo details in @todo_dict are not valid.
        """
        self.check_valid_description(todo_dict["todo_desc"])

#-------------------------------------------------------------------------------------------------#

#-----------------------------------------input actions-------------------------------------------#

    def load_curr_date(self):
        """
        Load the current date to the todo form.
        """
        curr_date = datetime.now().date()
        curr_date_str = curr_date.strftime("%Y:%m:%d")
        self.date_picker.text = curr_date_str

    def set_date_text(self, date):
        """
        Sets a String of a date in the todo form date picker.
        """
        self.date_picker.text = date.strftime("%Y:%m:%d")

    def open_date_picker(self):
        """
        Opens up a date picker so the user can choose a date for adding a todo task.
        """
        min_date = datetime.now().date()
        picker_date = datetime.strptime(
            self.date_picker.text, '%Y:%m:%d').date()

        date_dialog = MDDatePicker(
            callback=self.set_date_text,
            year=picker_date.year,
            month=picker_date.month,
            day=picker_date.day,
            min_date=min_date,
        )
        date_dialog.open()

#-------------------------------------------------------------------------------------------------#

#---------------------------------------addition actions------------------------------------------#

    def add_to_todo_list(self, todo_dict):
        """
        Adds todo task in the TODOScreen.

        Args:
            todo_dict (dict): a dictionary contaning todo task details.
        """
        todo_id = todo_dict["todo_id"]
        todo_date = todo_dict["todo_date"]
        todo_desc = todo_dict["todo_desc"]
        todo_item = Builder.load_string(todo_string)

        todo_item.name = todo_id
        todo_item.secondary_text = todo_date.strftime("%Y:%m:%d")
        todo_item.text = todo_desc

        todo_screen = self.manager.screens[5]
        todo_screen.add_todo(todo_id, todo_date, todo_desc, todo_item)

    def get_todo_details(self):
        """
        Gets a todo details from the user and adds it to the todos list.

        Raises:
            Exception: If the details the user entered are not valid.
        """
        todo_id = TODOIdGenerator.getInstance().get_next_id()
        todo_date = datetime.strptime(self.date_picker.text, '%Y:%m:%d').date()
        todo_desc = self.todo_desc.text

        todo_dict = {
            "todo_id": todo_id,
            "todo_date": todo_date,
            "todo_desc": todo_desc
        }

        self.check_valid_input(todo_dict)
        self.add_to_todo_list(todo_dict)
        self.show_add_dialog()

#-------------------------------------------------------------------------------------------------#

#-------------------------------classes for todo item in the screen-------------------------------#

class TODOListItemText(TwoLineAvatarIconListItem):
    pass


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    pass
#-------------------------------------------------------------------------------------------------#
