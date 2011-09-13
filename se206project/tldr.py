from se206project.models import Word

def parse_tldr(f):
    """
    Generative TLDR iterable parser (it works on lists too).

    >>> for word in parse_tldr([ "test|testing|he tests|easy" ]):
    ...     print word.word
    test
    """
    for line in f:
        if line[0] == "#": continue
        yield Word.deserialize(line)

def gen_tldr(words):
    """
    Generate a serialized TLDR iterable from a Words iterable.

    >>> for line in gen_tldr([ Word("test", "testing", "he tests", "easy") ]):
    ...     print line
    test|testing|he tests|easy
    """
    for word in words:
        yield word.serialize()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
