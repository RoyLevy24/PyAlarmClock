
class AlarmIdGenerator():
    __instance = None
    @staticmethod
    def getInstance():
        if AlarmIdGenerator.__instance == None:
            AlarmIdGenerator()
        return AlarmIdGenerator.__instance

    def __init__(self):
        if AlarmIdGenerator.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            AlarmIdGenerator.__instance = self
            self.gen = self.create_id_generator()

    def create_id_generator(self):
        i = 0
        while True:
            num = i
            i += 1
            yield f'alarm_id_{num}'

    def get_next_id(self):
        return next(self.gen)