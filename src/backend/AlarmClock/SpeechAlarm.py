import sys
sys.path.append("./src/")
from backend.SpeechRecognition.RecognizeWords import *
from backend.AlarmClock.Alarm import *
from playsound import playsound

class SpeechAlarm(Alarm):

    def __init__(self, alarm_id, main_screen, time, days, description, num_words):
        Alarm.__init__(self, alarm_id, main_screen, time, days, description)
        self.num_words = num_words

    def execute_alarm(self):
        print("in execute spichiii")
        word_recognizer = RecognizeWords.getInstance()
        word_list = word_recognizer.get_word_list(self.num_words)
        self.load_word_screen(word_list)



    def load_word_screen(self, word_list):
        dismiss_speech_screen = self.main_screen.manager.screens[3]
        current_word = word_list[0]
        rest_word_list = word_list[1:]

        go_to_next_word = lambda: self.load_word_screen(rest_word_list)
        next_button_on_press = super(SpeechAlarm, self).execute_alarm if len(rest_word_list) == 0 else go_to_next_word
        mic_on_press = next_button_on_press if RecognizeWords.getInstance().recognize_word(current_word.title) else lambda: None
        pronounce_on_press = lambda: playsound(current_word.pronounce_audio)

        dismiss_speech_screen.dismiss_speech_title.text = "Dismiss Speech"
        dismiss_speech_screen.dismiss_speech_word.text = current_word.title
        dismiss_speech_screen.dismiss_speech_pronounce.text = current_word.pronounce
        dismiss_speech_screen.dismiss_speech_play_word.on_press = pronounce_on_press
        dismiss_speech_screen.dismiss_speech_word_desc = current_word.meaning
        dismiss_speech_screen.dismiss_speech_record.on_press = mic_on_press
        dismiss_speech_screen.dismiss_speech_bottom.right_action_items = [["arrow-right-bold", lambda x: next_button_on_press()]]

        dismiss_speech_screen.manager.transition.direction = 'left'
        dismiss_speech_screen.manager.current = 'dismiss_speech'