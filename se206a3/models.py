class Word(object):
    def __init__(self, word, definition, example, difficulty):
        self.word = word
        self.definition = definition
        self.example = example
        self.difficulty = difficulty

    def __repr__(self):
        return "Word(word={word}, definition={definition}, " \
               "exampe={example}, difficulty={difficulty})".format(
                word=repr(self.word), definition=repr(self.definition),
                example=repr(self.example), difficulty=repr(self.difficulty))
