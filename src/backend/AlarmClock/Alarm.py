class Alarm():
    """
    This class represant a regular alarm clock
    """

    def __init__(self, alarm_id, main_screen, time, days, description):
        """
        Creates a new Alarm.

        Args:
            alarm_id (String): unique identifier for the alarm.
            main_screen (Screen): screen to return to after the alarm is done executing.
            time (datetime.time): time for the alarm to ring.
            days (list(int)): days indexes for the days the alarm should ring.
            description (String): description of the alarm.
        """
        self.alarm_id = alarm_id
        self.time = time
        self.main_screen = main_screen
        self.days = days
        self.description = description
        self.rang_today = False

    def back_to_main_screen(self):
        """
        Navigates the user to the main screen.
        """
        self.main_screen.manager.transition.direction = 'left'
        self.main_screen.manager.current = "main"

    def go_to_today_todo_screen(self):
        """
        Navigates the user to the screen with tasks for today.
        If there are not tasks, navigates to the main screen.
        """
        today_todo_screen = self.main_screen.manager.screens[5]
        self.main_screen.manager.transition.direction = 'left'

        if(today_todo_screen.load_today_tasks_screen()):
            self.main_screen.manager.current = "todo"
        else:
            self.main_screen.manager.current = "main"
            self.main_screen.is_alarm_active = False


    def execute_alarm(self):
        """
        dismisses regular alarm.
        """
        self.go_to_today_todo_screen()
