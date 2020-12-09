from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager

class EnterScreen(Screen, FloatLayout):
    """
    This class represant the Enter Screen of the Application.
    """

    def __init__(self, **kwargs):
        super(EnterScreen, self).__init__(**kwargs)