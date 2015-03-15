__author__ = 'akanksha'

import csv
import cPickle
from brillsTagset import BrillsTagset


def dumpDicts(dictionary, fname):
    output = open(fname, 'wb')
    cPickle.dump(dictionary, output)
    output.close()


def generateTagset():
    tobj = BrillsTagset()
    return tobj.getTagset()


class CalculateEachFrequency:

    tagset = generateTagset()

    def __init__(self, folder, n):
        
        self.folder = folder
        self.n = n
        
        self.catf = {}
        self.bigram = {}
        self.trigram = {}
        self.word = {}
        self.wordcat = {}
        self.newtags = []
        self.c = 0
        
        for each in CalculateEachFrequency.tagset:
            self.catf[each] = 1
            self.bigram[each] = {}
            self.trigram[each] = {}
            self.trigram[each]['start'] = {}
            for every in CalculateEachFrequency.tagset:
                self.bigram[each][every] = 1
                self.trigram[each][every] = {}
                self.trigram[each][every]['start'] = 1
                for one in CalculateEachFrequency.tagset:
                    self.trigram[each][every][one] = 1
            self.bigram[each]['start'] = 1
            self.trigram[each]['start']['start'] = 1
        self.catf['start'] = 1
        
        self.lastCat = ""
        self.seclastcat=""
        
        self.calculateFreq()
        dumpDicts(self.catf, self.folder + "/" + str(self.n) + "/CatFreq.pkl")
        dumpDicts(self.bigram, self.folder + "/" + str(self.n) + "/Bigram.pkl")
        dumpDicts(self.trigram, self.folder + "/" + str(self.n) + "/Trigram.pkl")
        dumpDicts(self.word, self.folder + "/" + str(self.n) + "/WordFreq.pkl")
        dumpDicts(self.wordcat, self.folder + "/" + str(self.n) + "/WordCatFreq.pkl")

    def calculateFreq(self):
        filetrain = self.folder + "/" + str(self.n) + "/train.csv"
        print filetrain
        with open(filetrain, 'r') as csvdataset:
            readtags = csv.reader(csvdataset, delimiter=',', lineterminator="\n")
            for row in readtags:
                if row[0] == "EOS":
                    self.lastCat = ""
                    self.seclastcat=""
                    self.catf['start'] += 1
                else:
                    if row[0] in list(self.word.keys()):
                        self.word[row[0]] += 1
                    else:
                        self.word[row[0]] = 2
                    for eachtag in row[1:]:
                        if eachtag not in CalculateEachFrequency.tagset:
                            t = "\""
                            if eachtag not in self.newtags:
                                self.newtags.append(eachtag)
                        else:
                            t = eachtag
                        if row[0] in list(self.wordcat.keys()):
                            self.wordcat[row[0]][t] += 1
                        else:
                            self.wordcat[row[0]] = {}
                            for tag in CalculateEachFrequency.tagset:
                                self.wordcat[row[0]][tag] = 0
                            self.wordcat[row[0]][t] = 1
    
                        self.catf[t] += 1

                        if not self.lastCat == "":
                            for every in self.lastCat.split("*"):
                                if every not in CalculateEachFrequency.tagset:
                                    e = "\""
                                    if every not in self.newtags:
                                        self.newtags.append(every)
                                else:
                                    e = every
                                self.bigram[t][e] += 1
                                if not self.seclastcat == "":
                                    for one in self.seclastcat.split("*"):
                                        if one not in CalculateEachFrequency.tagset:
                                            e2 = "\""
                                            if one not in self.newtags:
                                                self.newtags.append(one)
                                        else:
                                            e2 = one
                                        self.trigram[t][e][e2] += 1
                                else:
                                    self.trigram[t][e]['start'] += 1
                        else:
                            self.bigram[t]['start'] += 1
                            self.trigram[t]['start']['start'] += 1

                    self.seclastcat = self.lastCat
                    self.lastCat = '*'.join(row[1:])
                    self.c += 1
        print self.newtags, self.c