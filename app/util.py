from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

bad_chars = '(;)'.split()

def safer(txt):
    if txt is None: return txt

    tl = strip_tags(txt)
    #cs = tl.translate(None, ''.join(bad_chars))
    return tl



