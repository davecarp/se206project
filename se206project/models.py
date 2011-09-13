class Word(object):
    """
    The word model represents a word as specified -- containing a definition,
    example and difficulty level.
    """

    def __init__(self, word, definition, example, difficulty):
        """
        Create a word.
        """
        self.word = word
        self.definition = definition
        self.example = example
        self.difficulty = difficulty

    @classmethod
    def deserialize(cls, form):
        """
        Deserialize a word from its serialized form.

        >>> w = Word.deserialize("test|testing|he tests|easy")
        >>> w.word
        'test'
        >>> w.definition
        'testing'
        >>> w.example
        'he tests'
        >>> w.difficulty
        'easy'
        """
        return cls(*form.split("|"))

    def serialize(self):
        """
        Serialize a word.

        >>> Word("test", "testing", "he tests", "easy").serialize()
        'test|testing|he tests|easy'
        """
        return "{word}|{definition}|{example}|{difficulty}".format(
            **self.__dict__
        )

    def __repr__(self):
        return "Word(word={word}, definition={definition}, " \
               "exampe={example}, difficulty={difficulty})".format(
                word=repr(self.word), definition=repr(self.definition),
                example=repr(self.example), difficulty=repr(self.difficulty))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
