from se206a3.models import Line

def parse_tldr(f):
    """
    Generative TLDR file parser.
    """
    for line in f:
        if line[0] == "#": continue
        yield Line(*f.split("|"))
