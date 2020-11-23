import enum

class Alarm():

    def __init__(self, time, days, description, ring):
        self.time = time
        self.days = days
        self.description = description
        self.ring = ring
        self.rang_today = False
    

class Days(enum.Enum):
    Mon = 0
    Tue = 1
    Wen = 2
    Thu = 3
    Fri = 4
    Sat = 5
    Sun = 6

    