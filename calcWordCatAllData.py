__author__ = 'akanksha'

# This file operates the same way as calcFreq.py and calculates the frequencies of words and words in a given category
# This only runs once, and is run on 100% of words.

import csv
import cPickle

# Function to dump Dictionary into pickle file
def dumpDicts(dictionary, fname):
    output = open(fname, 'wb')
    cPickle.dump(dictionary, output)
    output.close()


class CalcWordCatAllData:

    def __init__(self, filename, folder, tagset):
        # not creating a static instance of tagset as this class will use only one instance.
        self.tagset = tagset
        self.folder = folder
        # Name of the file containing 100% words - orderedtags.csv
        self.filename = filename

        self.word = {}
        self.wordcat = {}
        self.newtags = []
        self.c = 0

        self.lastCat = ""

        self.calculateFreq()
        dumpDicts(self.word, self.folder + "/AllWordFreq.pkl")
        dumpDicts(self.wordcat, self.folder + "/AllWordCatFreq.pkl")

    def calculateFreq(self):
        with open(self.filename, 'r') as csvdataset:
            readtags = csv.reader(csvdataset, delimiter=',', lineterminator="\n")
            for row in readtags:
                if row[0] == "EOS":
                    self.lastCat = ""
                else:
                    if row[0] in list(self.word.keys()):
                        self.word[row[0]] += 1
                    else:
                        self.word[row[0]] = 2
                    for eachtag in row[1:]:
                        if eachtag not in self.tagset:
                            t = "\""
                            if (eachtag) not in self.newtags:
                                self.newtags.append(eachtag)
                        else:
                            t = eachtag
                        if row[0] in list(self.wordcat.keys()):
                            self.wordcat[row[0]][t] += 1
                        else:
                            self.wordcat[row[0]] = {}
                            for tag in self.tagset:
                                self.wordcat[row[0]][tag] = 0
                            self.wordcat[row[0]][t] = 1

                    self.lastCat = '*'.join(row[1:])
                    self.c += 1
                    print self.c
        print self.newtags