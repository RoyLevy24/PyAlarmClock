import sys
sys.path.append("./src/")
from WordOfTheDay.WordOfTheDay import *
from difflib import SequenceMatcher
import speech_recognition as sr


class RecognizeWords():

    # TODO: Need to be singleton

    @staticmethod
    def getInstance():
        if RecognizeWords.__instance == None:
            RecognizeWords()
        return RecognizeWords.__instance

    def __init__(self):
        if RecognizeWords.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.recognizer = sr.Recognizer()
            # TODO: change the device_index to deafault!
            self.microphone = sr.Microphone(device_index=2)
            self.match_ratio = 0.65
            RecognizeWords.__instance = self 

    def are_similar_words(self, actual_word, said_word):
        ratio = SequenceMatcher(None, actual_word, said_word).ratio()
        print(ratio)
        return ratio >= self.match_ratio

    def recognize_word(self, actual_word):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            try:
                said_word = self.recognizer.recognize_google(audio)
                return self.are_similar_words(actual_word, said_word)
            except Exception as e:
                # TODO: change exception message
                print(str(e))

    def recognize_words(self, num_words):
        wod = WordOfTheDay(num_words=num_words)
        words_list = wod.get_words_of_the_day()

        for word_item in words_list:
            recognize_word(word_item.title)

