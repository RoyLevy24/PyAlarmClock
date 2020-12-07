class Alarm():

    def __init__(self, alarm_id, main_screen, time, days, description):
        self.alarm_id = alarm_id
        self.time = time
        self.main_screen = main_screen
        self.days = days
        self.description = description
        self.rang_today = False

    def back_to_main_screen(self):
        self.main_screen.manager.transition.direction = 'left'
        self.main_screen.manager.current = "main"

    def execute_alarm(self):
        self.back_to_main_screen()

    # def __repr__(self):
    #     alarm_str = f"""
    #     Time: {self.time}
    #     Description: {self.description}
    #     days = {self.days}
    #     """
    #     return alarm_str
