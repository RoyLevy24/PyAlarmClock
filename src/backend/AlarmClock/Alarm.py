import enum


class Alarm():

    def __init__(self, alarm_id, time, days, description):
        self.alarm_id = alarm_id
        self.time = time
        self.days = days
        self.description = description
        self.rang_today = False
        self.dismiss_function = self.dismiss_alarm

    def execute_alarm(self):
        self.display_alarm_details()
        self.dismiss_function()

    def display_alarm_details(self):
        # need to do default action which is to show alarm details
        print(self)

    def dismiss_alarm(self):
        print("in dismiss base")
        pass

    def __repr__(self):
        alarm_str = f"""
        Time: {self.time}
        Description: {self.description}
        days = {self.days}
        """
        return alarm_str

class Days(enum.Enum):
    Mon = (0, "Monday")
    Tue = (1, "Tuesday")
    Wen = (2, "Wednesday")
    Thu = (3, "Thursday")
    Fri = (4, "Friday")
    Sat = (5, "Saturday")
    Sun = (6, "Sunday")

    def __str__(self):
        return self.value[1]
