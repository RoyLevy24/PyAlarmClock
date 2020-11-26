import sys
sys.path.append("./src/")
from SpeechRecognition.RecognizeWords import *
from AlarmClock.Alarm import *

def __init__(self, time, days, description, ring, num_words):
    Alarm.__init__(self, time , days, description, ring)
    self.num_words = num_words
    self.dismiss_function = dismiss_alarm

    def execute_alarm(self):
        super(RecognizeWords, self).execute_alarm()

    def dismiss_alarm(self):
        open_eyes_detector = RecognizeWords.getInstance()
        open_eyes_detector.detect_open_eyes(self.staring_time)