from spellorama.models import Word

class ParserError(Exception):
    """
    Parser exception class.
    """
    def __init__(self, lineno, exc):
        self.lineno = lineno
        self.exc = exc

    def __str__(self):
        return "line {0}: {1}".format(self.lineno, self.exc)

def parse_tldr(f):
    """
    Generative TLDR iterable parser (it works on lists too).

    >>> for word in parse_tldr([ "test|testing|he tests|easy" ]):
    ...     print word.word
    test
    """
    for i, line in enumerate(f):
        line = line.strip()
        if line[0] == "#": continue
        if not line: continue

        try:
            yield Word.deserialize(line)
        except Exception as e:
            raise ParserError(i + 1, e)

def gen_tldr(words):
    """
    Generate a serialized TLDR iterable from a Words iterable.

    >>> for line in gen_tldr([ Word("test", "testing", "he tests", "easy") ]):
    ...     print line
    test|testing|he tests|easy
    """
    for word in words:
        yield word.serialize() + "\n"

if __name__ == "__main__":
    import doctest
    doctest.testmod()
