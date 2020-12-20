import weakref
from datetime import datetime

from frontend.screens.TODOScreen.TODOItem import *
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen


class TODOScreen(Screen, FloatLayout):
    """
    This class responsibility is display TODO tasks entered by the user.
    """

    def __init__(self, **kwargs):
        """
        Creates a new TODO Screen.
        """
        super(TODOScreen, self).__init__(**kwargs)
        self.todo_list = []
        self.init_attrs = False

    def init_today_tasks_attributes(self):
        """
        Init attributes for the TODO Screen and Screen that shows TODO task for today.
        """
        # sets TODO Screen attributes
        toolbar = self.ids.todo_toolbar
        self.actual_title = toolbar.title
        self.actual_left_actions = toolbar.left_action_items
        self.actual_right_actions = toolbar.right_action_items

        # sets today TODO tasks Screen attributes
        self.today_title = "Tasks For Today"
        self.today_left_actions = []
        self.today_right_actions = [
            ["arrow-right", lambda x: self.go_to_main_screen()]]

        self.list_item_size = None
        self.init_attrs = True

    def go_to_main_screen(self):
        """
        Navigates the user to the main alarms screen.
        """
        self.manager.transition.direction = 'left'
        self.manager.current = 'main'
        self.reset_screen()
        # indicates that the alarm is not active at the moment
        self.manager.screens[1].is_alarm_active = False

    def reset_screen(self):
        """
        Resets the screen to the default TODO Screen.
        """
        toolbar = self.ids.todo_toolbar
        toolbar.title = self.actual_title
        toolbar.left_action_items = self.actual_left_actions
        toolbar.right_action_items = self.actual_right_actions

        # displaying all the todo tasks
        for key, value in self.ids.items():
            if key.startswith("todo_id_"):
                value.size = self.list_item_size
                value.opacity = 1

        self.list_item_size = None

    def load_today_tasks_screen(self):
        """
        Loads all the TODO tasks for the current day to the screen,
        hiding the rest of the tasks.
        """
        # returning if there are no tasks for today
        if self.has_tasks_today() == False:
            return False

        if self.init_attrs == False:
            self.init_today_tasks_attributes()

        # sets the screen attributes to the today tasks screen
        toolbar = self.ids.todo_toolbar
        toolbar.title = self.today_title
        toolbar.left_action_items = self.today_left_actions
        toolbar.right_action_items = self.today_right_actions

        # hiding all the tasks that are not for today
        curr_date_str = datetime.now().date().strftime("%Y:%m:%d")
        for key, value in self.ids.items():
            if key.startswith("todo_id_"):
                if not self.list_item_size:
                    self.list_item_size = (value.size[0], value.size[1])
                if value.secondary_text != curr_date_str:
                    value.size = (0, 0)
                    value.opacity = 0

        return True

    def has_tasks_today(self):
        """
        Returns True if there are TODO tasks for today.
        """
        for key in self.ids:
            if key.startswith("todo_id_"):
                return True
        return False

    def go_back_to_enter(self):
        """
        Navigates the user to the enter screen.
        """
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
        """
        Adds a TODO task.

        Args:
            todo_id (String): task id.
            date (datetime.date): date for the task.
            description (String): task description.
            todo_item (weakref.proxy(Widget)): element of the task to show in the screen.
        """
        # adding a TODOItem to the list
        todo_list_item = TODOItem(todo_id, date, description, False)
        self.todo_list.append(todo_list_item)

        # adding the task to the screen
        self.ids.list.add_widget(todo_item)
        self.ids[todo_id] = weakref.proxy(todo_item)

    def delete_todo(self, todo_id):
        """
        Deletes a todo with a given todo_id from TODOScreen

        Args:
            todo_id (String): id of the task wished to be deleted.
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
