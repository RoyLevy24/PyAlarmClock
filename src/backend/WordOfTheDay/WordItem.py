class WordItem():

    def __init__(self, title, pronounce, pronounce_audio, pos, meaning):
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
