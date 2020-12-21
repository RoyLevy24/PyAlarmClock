class TODOItem():
    """
    This class represents a TODO task. 
    """

    def __init__(self, todo_id, date, description, done):
        """
        Creates a new TODO task.
        
        Args:
            todo_id: task id.
            date: task date.
            description: task description.
            done: indicates if the task is done or not.
        """
        self.id = todo_id
        self.date = date
        self.description = description
        self.done = done

    def mark_done(self):
        self.done = True
