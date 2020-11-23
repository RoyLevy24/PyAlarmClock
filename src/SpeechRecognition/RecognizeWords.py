from difflib import SequenceMatcher

import speech_recognition as sr


class RecognizeWords():

    # TODO: Need to be singleton

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.match_ratio = 0.65

    def recognize_word(self, actual_word):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            try:
                said_word = self.recognizer.recognize_google(audio)
                return self.are_similar_words(actual_word, said_word)
            except Exception as e:
                print(str(e))

    def are_similar_words(self, actual_word, said_word):
        print("here")
        ratio = SequenceMatcher(None, actual_word, said_word).ratio()
        print(ratio)
        return ratio >= self.match_ratio


rw = RecognizeWords()
sim = rw.recognize_word("cat")
print(sim)
