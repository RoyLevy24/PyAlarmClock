from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager

class EnterScreen(Screen, FloatLayout):
    """
    This class represant the Enter Screen of the Application.
    """

    def __init__(self, **kwargs):
        """Creates a new Enter Screen"""
        super(EnterScreen, self).__init__(**kwargs)

    def navigate_to_alarms(self):
        """Navigates the user to alarms screen"""
        self.manager.transition.direction = 'left'
        self.manager.current = 'main'
    
    def navigate_to_todos(self):
        """Navigates the user to TODO tasks screen"""
        self.manager.transition.direction = 'left'
        self.manager.current = 'todo'
