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
            # creates
            self.recognizer = sr.Recognizer()
            # TODO: change the device_index to default!
            self.microphone = sr.Microphone(device_index=1)
            self.match_ratio = 0.65
            RecognizeWords.__instance = self

    def are_similar_words(self, actual_word, said_word):
        """
        Checks if the word said by the user and expected word are similar.

        Args:
            actual_word (String): exprected word.
            said_word (String): the word said by the user.

        Returns: 
            True if the words are similar enough (determined by @self.match_ratio).
            False, otherwise.
        """
        actual_word = actual_word.lower()
        said_word = said_word.lower()
        ratio = SequenceMatcher(None, actual_word, said_word).ratio()
        return ratio >= self.match_ratio

    def recognize_word(self, actual_word):
        """
        Allows the user to speak into the microphone.
        Recognizes the word said by the user.
        """
        with self.microphone as source:
            # setting up microphone for speech
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            try:
                # getting the word from the user
                # TODO: notify the user he can speak
                said_word = self.recognizer.recognize_google(audio)
                return self.are_similar_words(actual_word, said_word)
            except Exception as e:
                # TODO: change exception message
                print(str(e))

    def get_word_list(self, num_words):
        """
        Returns a list of word details. the list contains the words the user needs to speak.

        Args:
            num_words (int): number of words the user needs to speak.
        """
        wod = WordOfTheDay(num_words=num_words)
        words_list = wod.get_words_of_the_day()
        return words_list
