class WordItem():
    """
    This class represants a words that the user needs to speak
    for speech recognition alarm.
    """

    def __init__(self, title, pronounce, pronounce_audio, pos, meaning):
        """
        Creates a new WordItem.

        Args:
            title (String): the word itself represanted as a string.txt
            pronounce (String): a string that tells how to pronounce the word.
            pronounce_audio (String): path to audio file containing pronunciation of the word.
            pos (String): part of speech of the word
            meaning (String): the words meaning.
        """

        self.title = title
        self.pronounce = pronounce
        self.pronounce_audio = pronounce_audio
        self.pos = pos
        self.meaning = meaning

    def __repr__(self):
        word_str = f"""
        title: {self.title}
        pronounce: {self.pronounce}
        pronounce audio: {self.pronounce_audio}
        part of speech: {self.pos}
        meaning: {self.meaning}
        """
        return word_str
