__author__ = 'akanksha'


class BrillsTagset:

    def __init__(self):

        self.tagdesc = {}
        self.tagset = []
        self.count = 0

        tagfile = open("brill_tagset.txt")

        for line in tagfile:
            string = line.split(' ')
            self.tagdesc[' '.join(string[1:])] = string[0]
            self.tagset.append(string[0])

    def getTagset(self):
        return self.tagset

    def getTagDescript(self):
        return self.tagdesc

    def getTagCount(self):
        return self.count