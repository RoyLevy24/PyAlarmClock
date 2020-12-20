class AlarmIdGenerator():
    """
    This class represents a generator of ids for alarm clocks.
    """

    __instance = None

    @staticmethod
    def getInstance():
        """
        Creating a new AlarmIdGenerator if not already exists.
        Returns the instance of AlarmIdGenerator.
        """
        if AlarmIdGenerator.__instance == None:
            AlarmIdGenerator()
        return AlarmIdGenerator.__instance

    def __init__(self):
        """
        Creating a new AlarmIdGenerator if not already exists.
        """
        if AlarmIdGenerator.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            AlarmIdGenerator.__instance = self
            # setting up id generator
            self.gen = self.create_id_generator()

    def create_id_generator(self):
        """
        Creates a generator for alarm clocks ids.
        """
        i = 0
        while True:
            num = i
            i += 1
            yield f'alarm_id_{num}'

    def get_next_id(self):
        """
        Returns the next alarm clock id in the generator.
        """
        return next(self.gen)
