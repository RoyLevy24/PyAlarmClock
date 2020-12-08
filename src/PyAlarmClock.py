import sys

sys.path.append("./src/")
sys.path.append("./src/frontend/")
sys.path.append("../")




from frontend.frontend import *


class PyAlarmClock():
    """
    This class is the main entry point of the app.
    """
    def __init__(self):
        # creates KivyMD alarm clock app
        self.app = AlarmApp()

    def run(self):
        # running KivyMD alarm clock app
        self.app.run()


if __name__ == '__main__':
    app = PyAlarmClock()
    app.run()
