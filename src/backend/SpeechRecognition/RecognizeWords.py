from difflib import SequenceMatcher

import speech_recognition as sr
from backend.WordOfTheDay.WordOfTheDay import *


class RecognizeWords():
    """
    This class is responsible of speech recognition of words.
    """

    __instance = None

    @staticmethod
    def getInstance():
        """
        Creates RecognizeWords instance if not already exists.
        Returns RecognizeWords instance.
        """
        if RecognizeWords.__instance == None:
            RecognizeWords()
        return RecognizeWords.__instance

    def __init__(self):
        """
        Creates RecognizeWords instance if not already exists.
        """
        if RecognizeWords.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.recognizer = sr.Recognizer()
            RecognizeWords.__instance = self

    def are_similar_words(self, actual_word, said_word, sim_thresh):
        """
        Checks if the word said by the user and expected word are similar.

        Args:
            actual_word (String): exprected word.
            said_word (String): the word said by the user.
            sim_thresh (float): measurement to determine the minimum similarity for the words.

        Returns:
            True if the words are similar enough (determined by @sim_thresh).
            False, otherwise.
        """
        actual_word = actual_word.lower()
        said_word = said_word.lower()
        ratio = SequenceMatcher(None, actual_word, said_word).ratio()
        return ratio >= sim_thresh

    def recognize_word(self, actual_word, mic_num, sim_thresh):
        """
        Allows the user to speak into the microphone.
        Recognizes the word said by the user.
        """
        with sr.Microphone(device_index=mic_num) as source:
            # setting up microphone for speech
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source)
                # getting the word from the user
                said_word = self.recognizer.recognize_google(audio)
                print(said_word)
                return self.are_similar_words(actual_word, said_word, sim_thresh)
            except Exception as e:
                return False

    def get_word_list(self, num_words):
        """
        Returns a list of word details. the list contains the words the user needs to speak.

        Args:
            num_words (int): number of words the user needs to speak.
        """
        wod = WordOfTheDay(num_words=num_words)
        words_list = wod.get_words_of_the_day()
        return words_list
