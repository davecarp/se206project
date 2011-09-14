import re
import json
import urllib2
import sys

HTML_TAG_PATTERN = re.compile(r'<.*?>')
HEX_ESCAPE_PATTERN = re.compile(r'\\x([a-fA-F0-9]{2})')
API_URL = "http://www.google.com/dictionary/json?callback=dict_api.callbacks.id100&q={word}&sl=en&tl=en"

class CollectionM(object):
    """
    Collection-querying monad, to stifle any Nones that may arise.
    """
    def __init__(self, result):
        self.result = result

    def get(self, key):
        """
        Get a key from the underlying collection if possible, otherwise return
        a CollectionM encapsulating None.
        """
        if self.result is None:
            result = None
        else:
            try:
                result = self.result[key]
            except:
                result = None
        return CollectionM(result)

    def __repr__(self):
        return 'CollectionsM({0})'.format(repr(self.result))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("""\
    Usage: {0} DIFFICULTY
    Generate a TLDR file using words from STDIN.
    Uses Google for definitions and example.

    DIFFICULTY argument specifies the difficulty the list is.\
    """.format(sys.argv[0]))
        sys.exit(1)

    for word in sys.stdin:
        word = word.strip() # chomp

        data = urllib2.urlopen(API_URL.format(word=word)).read()
        doc = json.loads(
            HEX_ESCAPE_PATTERN.sub(
                lambda x: chr(int(x.group(1), 16)),
                data[data.index('(')+1:data.rindex(')')] \
                    .rsplit(",", 2)[0]
            )
        )

        entriesm = CollectionM(doc) \
            .get('primaries').get(0) \
            .get('entries').get(1)

        definition = entriesm \
            .get('terms').get(0) \
            .get('text') \
            .result

        example = entriesm \
            .get('entries').get(0) \
            .get('terms').get(0) \
            .get('text') \
            .result

        if definition is None:
            sys.stderr.write("WARNING: No definition for {0}\n".format(word))
            definition = "no definition"

        if example is None:
            sys.stderr.write("WARNING: No example for {0}\n".format(word))
            example = "no example"

        difficulty = sys.argv[1]

        definition = HTML_TAG_PATTERN.sub('', definition.encode("utf-8"))
        example = HTML_TAG_PATTERN.sub('', example.encode("utf-8"))

        print('{0}|{1}|{2}|{3}'.format(word, definition, example, difficulty))
