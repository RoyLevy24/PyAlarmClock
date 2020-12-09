import sys

sys.path.append("./src/")

from playsound import playsound
from backend.SpeechRecognition.RecognizeWords import *
from backend.AlarmClock.Alarm import *


class SpeechAlarm(Alarm):
    """
    This class represents speech recognition alarm
    """

    def __init__(self, alarm_id, main_screen, time, days, description, num_words):
        # TODO: gets args from the command line
        """
        Creates a new SpeechAlarm.

        Args:
            alarm_id (String): unique identifier for the alarm.
            main_screen (Screen): screen to return to after the alarm is done executing.
            time (datetime.time): time for the alarm to ring.
            days (list(int)): days indexes for the days the alarm should ring.
            description (String): description of the alarm.
            num_words (int): number of words the user to pronounce in order to dismiss the alarm.
        """
        Alarm.__init__(self, alarm_id, main_screen, time, days, description)
        self.num_words = num_words

    def execute_alarm(self):
        """
        Invokes speech detection algorithm.
        Transition the user to the speech recognition screen.
        """
        word_recognizer = RecognizeWords.getInstance()
        # getting words details for the words the user needs to speak 
        word_list = word_recognizer.get_word_list(self.num_words)
        # loads details for first word
        self.load_word_screen(word_list)

    def load_word_screen(self, word_list):
        """
        Setting up the details for each word in the speech recognition screen.

        word_list (list(WordItem)): list containing details of all the words the user needs to speak.
        """
        # getting the screen
        dismiss_speech_screen = self.main_screen.manager.screens[3]
        current_word = word_list[0]
        rest_word_list = word_list[1:]

        # load the next word's details if the rest of the list is not empty,
        # navigate the user to the main screen otherwise.
        def go_to_next_word(): return self.load_word_screen(rest_word_list)
        next_button_on_press = super(SpeechAlarm, self).execute_alarm if len(
            rest_word_list) == 0 else go_to_next_word

        # getting method to execute when the user wish to speak
        mic_on_press = self.get_mic_on_press(
            next_button_on_press, current_word.title, dismiss_speech_screen)

        # getting method to listen to the word's pronunciation
        def pronounce_on_press(): return playsound(current_word.pronounce_audio)

        # setting up details in the screen
        dismiss_speech_screen.dismiss_speech_title.text = "Dismiss Speech"
        dismiss_speech_screen.dismiss_speech_word.text = current_word.title
        dismiss_speech_screen.dismiss_speech_pronounce.text = current_word.pronounce
        dismiss_speech_screen.dismiss_speech_play_word.on_press = pronounce_on_press
        dismiss_speech_screen.dismiss_speech_word_desc.text = current_word.meaning
        dismiss_speech_screen.dismiss_speech_record.on_press = mic_on_press
        dismiss_speech_screen.dismiss_speech_bottom.right_action_items = [
            ["arrow-right-bold", lambda x: next_button_on_press()]]

        # navigating the user to the next screen
        dismiss_speech_screen.manager.transition.direction = 'left'
        dismiss_speech_screen.manager.current = 'dismiss_speech'

    def get_mic_on_press(self, next_button_on_press, word_title, dismiss_speech_screen):
        """
        Returns a method to execute when the user wish to speak a word.

        Args:
            next_button_on_press (function -> None): function to transition the user to the next screen.
            word_title (String): current word the user needs to speak.
            dismiss_speech_screen (Screen): speech recognition screen

        """
        def mic_on_press():
            dismiss_speech_screen.disable_speech_button()
            # TODO: alert the user to start speaking
            # user starts to speak
            is_recognized_word = RecognizeWords.getInstance().recognize_word(word_title)
            dismiss_speech_screen.enable_speech_button()
            if is_recognized_word:
                # moves the user to the next screen
                return next_button_on_press()
            else:
                # shows an error message if the user hasn't spoke the word correctly
                dismiss_speech_screen.show_speech_fail_snackbar()
                return lambda: None

        return mic_on_press
