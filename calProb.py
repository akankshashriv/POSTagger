__author__ = 'akanksha'

import cPickle
from brillsTagset import BrillsTagset


def generateTagset():
    tobj = BrillsTagset()
    return tobj.getTagset()


def loadAllWordCat():
    pkl_file = open('Datasets/AllWordCatFreq.pkl', 'rb')
    wordcat = cPickle.load(pkl_file)
    pkl_file.close()
    return wordcat


def loadDict(fname):
    pkl_file = open(fname, 'rb')
    dictionary = cPickle.load(pkl_file)
    pkl_file.close()
    return dictionary


def dumpDicts(dictionary, fname):
    output = open(fname, 'wb')
    cPickle.dump(dictionary, output)
    output.close()


class CalculateProb:

    wordCatAll = loadAllWordCat()
    tagset = generateTagset()
    delta = 0.1

    def __init__(self, folder, n):
        self.n = n
        self.folder = folder
        self.catf = loadDict(self.folder + "/" + str(self.n) + "/CatFreq.pkl")
        self.bigram = loadDict(self.folder + "/" + str(self.n) + "/Bigram.pkl")
        self.trigram = loadDict(self.folder + "/" + str(self.n) + "/Trigram.pkl")
        self.wordCat = loadDict(self.folder + "/" + str(self.n) + "/WordCatFreq.pkl")
        self.length = len(self.catf)

        self.p_cat1_cat2 = {}
        self.p_cat1_cat2_cat3 = {}
        self.p_word_cat = {}
        self.p_word_cat_all = {}

        for cat1 in CalculateProb.tagset:
            self.p_cat1_cat2[cat1] = {}
            self.p_cat1_cat2_cat3[cat1] = {}
            self.p_cat1_cat2_cat3[cat1]['start'] = {}
            for cat2 in CalculateProb.tagset:
                self.p_cat1_cat2[cat1][cat2] = 0.0
                self.p_cat1_cat2_cat3[cat1][cat2] = {}
                for cat3 in CalculateProb.tagset:
                    self.p_cat1_cat2_cat3[cat1][cat2][cat3] = 0.0
                self.p_cat1_cat2_cat3[cat1][cat2]['start'] = 0.0
            self.p_cat1_cat2[cat1]['start'] = 0.0
            self.p_cat1_cat2_cat3[cat1]['start']['start'] = 0.0

        self.calcProb()
        dumpDicts(self.p_cat1_cat2, self.folder + "/" + str(self.n) + "/p_cat1_cat2.pkl")
        dumpDicts(self.p_cat1_cat2_cat3, self.folder + "/" + str(self.n) + "/p_cat1_cat2_cat3.pkl")
        dumpDicts(self.p_word_cat, self.folder + "/" + str(self.n) + "/p_word_cat.pkl")
        dumpDicts(self.p_word_cat_all, self.folder + "/" + str(self.n) + "/p_word_cat_all.pkl")

    def calcProb(self):
        for cat1 in list(self.bigram.keys()):
            for cat2 in list(self.bigram[cat1].keys()):
                self.p_cat1_cat2[cat1][cat2] = float(self.bigram[cat1][cat2]) / (self.catf[cat2] + CalculateProb.delta*self.length)

        for cat1 in list(self.trigram.keys()):
            for cat2 in list(self.trigram[cat1].keys()):
                for cat3 in list(self.trigram[cat1][cat2].keys()):
                    if cat2 == 'start':
                        c = self.catf[cat1]
                    else:
                        c = self.bigram[cat2][cat3]
                    self.p_cat1_cat2_cat3[cat1][cat2][cat3] = float(self.trigram[cat1][cat2][cat3]) / (c + CalculateProb.delta*self.length)

        for each in list(self.wordCat.keys()):
            if each not in list(self.p_word_cat.keys()):
                self.p_word_cat[each] = {}
                for tag in CalculateProb.tagset:
                    self.p_word_cat[each][tag] = 0.0
            for cat in list(self.wordCat[each].keys()):
                self.p_word_cat[each][cat] = float(self.wordCat[each][cat]) / float(self.catf[cat])

        for each in list(CalculateProb.wordCatAll.keys()):
            if each not in list(self.p_word_cat_all.keys()):
                self.p_word_cat_all[each] = {}
                for tag in CalculateProb.tagset:
                    self.p_word_cat_all[each][tag] = 0.0
            for cat in list(CalculateProb.wordCatAll[each].keys()):
                self.p_word_cat_all[each][cat] = float(CalculateProb.wordCatAll[each][cat]) / float(self.catf[cat])