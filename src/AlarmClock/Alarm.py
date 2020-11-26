import enum

class Alarm():

    def __init__(self, time, days, description, ring):
        self.time = time
        self.days = days
        self.description = description
        self.ring = ring
        self.rang_today = False
        self.dismiss_function = dismiss_alarm

    def execute_alarm(self):
        self.display_alarm_details()
        self.dismiss_function()

    def display_alarm_details(self):
        # need to do default action which is to show alarm details
        print("In base class: Alarm") 

    def dismiss_alarm(self):
        pass

class Days(enum.Enum):
    Mon = 0
    Tue = 1
    Wen = 2
    Thu = 3
    Fri = 4
    Sat = 5
    Sun = 6

    