class ParseTitle(object):
    def __init__(self, titles):
        self.titles = titles

    def parseTitle(self):
        for i, title in enumerate(self.titles):
            print i, title