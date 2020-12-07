import enum


class Alarm():

    def __init__(self, alarm_id, time, days, description):
        self.alarm_id = alarm_id
        self.time = time
        self.days = days
        self.description = description
        self.rang_today = False

    def execute_alarm(self):
        pass