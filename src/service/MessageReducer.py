import sys
import queue
sys.path.append("./src/")
from service.actions.actions import *
from service.actions.actions_types import *

class MessageReducer():

    @staticmethod
    def getInstance():
        if MessageReducer.__instance == None:
            MessageReducer()
        return MessageReducer.__instance

    def __init__(self):
        if MessageReducer.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            MessageReducer.__instance = self
            self.message_queue = queue.Queue()

    def dispatch_message(self):
        action = self.message_queue.get()
        self.dispatch(action)

    def add_message(self, message):
        self.message_queue.put(message)

    def dispatch(self, action):
        action_type = action_type["type"]
        switcher = {
            
        }
        switcher[action_type](action.payload)