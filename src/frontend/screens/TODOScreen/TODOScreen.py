import weakref
from datetime import datetime

from frontend.gui_strings import alarm_string
from frontend.screens.TODOScreen.TODOItem import *
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDDatePicker
from service.AlarmIdGenerator import *
from service.utils import *


class TODOScreen(Screen, FloatLayout):
    """
    This class responsibility is display TODO tasks entered by the user.
    """

    def __init__(self, **kwargs):
        super(TODOScreen, self).__init__(**kwargs)
        self.todo_list = []
        self.init_attrs = False

    def init_today_tasks_attributes(self):
        toolbar = self.ids.todo_toolbar
        self.actual_title = toolbar.title
        self.actual_left_actions = toolbar.left_action_items
        self.actual_right_actions = toolbar.right_action_items

        self.today_title = "Tasks For Today"
        self.today_left_actions = []
        self.today_right_actions = [["arrow-right", lambda x: self.go_to_main_screen()]]

        self.list_item_size = None
        self.init_attrs = True

    def go_to_main_screen(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'main'
        self.reset_screen()
        self.manager.screens[1].is_alarm_active = False

    def reset_screen(self):
        toolbar = self.ids.todo_toolbar
        toolbar.title = self.actual_title
        toolbar.left_action_items = self.actual_left_actions
        toolbar.right_action_items = self.actual_right_actions

        for key, value in self.ids.items():
            if key.startswith("todo_id_"):
                value.size = self.list_item_size
                value.opacity = 1
        
        self.list_item_size = None

    def load_today_tasks_screen(self):

        if self.has_tasks_today() == False:
            return False

        if self.init_attrs == False:
            self.init_today_tasks_attributes()

        toolbar = self.ids.todo_toolbar
        toolbar.title = self.today_title
        toolbar.left_action_items = self.today_left_actions
        toolbar.right_action_items = self.today_right_actions

        curr_date_str = datetime.now().date().strftime("%Y:%m:%d")
        for key, value in self.ids.items():
            if key.startswith("todo_id_"):
                if not self.list_item_size:
                    self.list_item_size = (value.size[0], value.size[1])
                if value.secondary_text != curr_date_str:
                    value.size = (0,0)
                    value.opacity = 0

        return True

    def has_tasks_today(self):
        for key in self.ids:
            if key.startswith("todo_id_"):
                return True
        return False

    def go_back_to_enter(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'enter'

    def navigate_todo_form(self):
        """
        navigates the user to todo form for adding a todo task
        """
        # get the todo_form screen
        todo_form_screen = self.manager.screens[6]
        todo_form_screen.load_curr_date()

        # transition to todo_form screen
        self.manager.transition.direction = 'left'
        self.manager.current = 'todo_form'

    def add_todo(self, todo_id, date, description, todo_item):
        todo_list_item = TODOItem(todo_id, date, description, False)
        self.todo_list.append(todo_list_item)

        self.ids.list.add_widget(todo_item)
        self.ids[todo_id] = weakref.proxy(todo_item)

    def delete_todo(self, todo_id):
        """
        Deletes a todo with a given todo_id from TODOScreen
        """

        # removes the todo from the screen's todo_list
        self.todo_list = list(
            filter(
                lambda todo: todo.id != todo_id,
                self.todo_list
            )
        )
        # removes the todo from the screen's view
        self.ids.list.remove_widget(self.ids[todo_id])
        self.ids.pop(todo_id, None)