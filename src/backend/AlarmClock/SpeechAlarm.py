import sys
sys.path.append("./src/")
from SpeechRecognition.RecognizeWords import *
from AlarmClock.Alarm import *

class SpeechAlarm(Alarm):

    def __init__(self, time, days, description, ring, num_words):
        Alarm.__init__(self, time , days, description, ring)
        self.num_words = num_words
        Alarm.dismiss_function = self.dismiss_alarm

        def execute_alarm(self):
            super(RecognizeWords, self).execute_alarm()

        def dismiss_alarm(self):
            print("in dismiss speech")
            word_recognizer = RecognizeWords.getInstance()
            word_recognizer.recognize_words(self.num_words)