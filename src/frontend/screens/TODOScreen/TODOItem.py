class TODOItem():

    def __init__(self, id, date, description, done):
        self.id = id
        self.date = date
        self.description = description
        self.done = done

    def mark_done(self):
        self.done = True