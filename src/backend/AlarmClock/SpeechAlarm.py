import sys
sys.path.append("./src/")
from backend.SpeechRecognition.RecognizeWords import *
from backend.AlarmClock.Alarm import *

class SpeechAlarm(Alarm):

    def __init__(self, alarm_id, time, days, description, num_words):
        Alarm.__init__(self, alarm_id, time, days, description)
        self.num_words = num_words

    def execute_alarm(self):
        word_recognizer = RecognizeWords.getInstance()
        word_recognizer.recognize_words(self.num_words)