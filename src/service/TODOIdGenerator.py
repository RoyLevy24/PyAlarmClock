class TODOIdGenerator():
    """
    This class represents a generator of ids for todo tasks.
    """

    __instance = None

    @staticmethod
    def getInstance():
        """
        Creating a new TODOIdGenerator if not already exists.
        Returns the instance of TODOIdGenerator.
        """
        if TODOIdGenerator.__instance == None:
            TODOIdGenerator()
        return TODOIdGenerator.__instance

    def __init__(self):
        """
        Creating a new TODOIdGenerator if not already exists.
        """
        if TODOIdGenerator.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            TODOIdGenerator.__instance = self
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
            yield f'todo_id_{num}'

    def get_next_id(self):
        """
        Returns the next todo task id in the generator.
        """
        return next(self.gen)
