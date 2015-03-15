__author__ = 'akanksha'

import csv
import cPickle
from brillsTagset import BrillsTagset


def loadDict(fname):
    pkl_file = open(fname, 'rb')
    dictionary = cPickle.load(pkl_file)
    pkl_file.close()
    return dictionary


def generateTagset():
    tobj = BrillsTagset()
    return tobj.getTagset()


class ClassifyTestDataBigram:

    tagset = generateTagset()

    def __init__(self, folder, n, pfile1, pfile2, pfile3, fname):
        self.folder = folder
        self.n = n
        self.fname = fname

        self.sentence = []
        self.tagged = {}
        self.classifiedBi = {}
        self.correctcountBi = 0
        self.allcount = 0

        self.p_cat1_cat2 = loadDict(self.folder + "/" + str(self.n) + "/" + pfile1)
        self.p_word_cat = loadDict(self.folder + "/" + str(self.n) + "/" + pfile2)
        self.word = loadDict(self.folder + "/" + str(self.n) + "/" + pfile3)

        self.classify()
        self.accuracy()

    def accuracy(self):
        f = open("Accuracy/" + self.fname, 'wb')
        f.write(str(float(self.correctcountBi * 100)/self.allcount))

    def verify(self):
        fileoutput = self.folder + "/" + str(self.n) + "/taggedoutput.csv"
        csvdataset = open(fileoutput, 'a')
        wr = csv.writer(csvdataset, lineterminator="\n")
        for each in self.sentence:
            if self.classifiedBi[each] in self.tagged[each]:
                self.correctcountBi += 1
            wr.writerow([each, self.classifiedBi[each]])
            self.allcount += 1

    def runViterbi(self):
        scoreBi = {}
        backpointerBi = {}

        for tag in ClassifyTestDataBigram.tagset:
            scoreBi[tag] = {}
            backpointerBi[tag] = {}
            if self.sentence[0] in list(self.word.keys()):
                p1 = self.p_word_cat[self.sentence[0]][tag]
            else:
                p1 = 1
            scoreBi[tag][self.sentence[0]] = p1 * self.p_cat1_cat2[tag]['start']

        backpointerBi['start'] = {}

        c = 1
        prevword = self.sentence[0]
        for each in self.sentence[1:]:
            for tag in ClassifyTestDataBigram.tagset: #v
                maxscoreBi = 0
                for tag2 in ClassifyTestDataBigram.tagset: #u
                    if each in list(self.word.keys()):
                        p1 = self.p_word_cat[each][tag]
                    else:
                        p1 = 1
                    s1 = scoreBi[tag2][prevword] * self.p_cat1_cat2[tag][tag2] * p1
                    if maxscoreBi <= s1:
                        maxscoreBi = s1
                        maxtagBi = tag2
                scoreBi[tag][each] = maxscoreBi
                backpointerBi[tag][each] = maxtagBi
            prevword = each
            c += 1

        maxscoreBi = 0
    
        for each in ClassifyTestDataBigram.tagset:
            if maxscoreBi <= scoreBi[each][self.sentence[-1]]:
                maxscoreBi = scoreBi[each][self.sentence[-1]]
                maxtagBi = each

        self.classifiedBi[self.sentence[-1]] = maxtagBi

        prevtag = maxtagBi
        prevword = self.sentence[-1]
    
        for each in reversed(self.sentence[:-1]):
            self.classifiedBi[each] = backpointerBi[prevtag][prevword]
            if each in [")", "(", ",", ".", "#", "$", ":"]:
                self.classifiedBi[each] = each
            prevword = each
            prevtag = self.classifiedBi[each]

        # for each in self.sentence:
        #     print each + "/" + self.classifiedBi[each] + "//" + self.classifiedTri[each]

    def classify(self):
        filetest = self.folder + "/" + str(self.n) + "/test.csv"
        self.sentence = []
        self.tagged = {}
        with open(filetest, 'r') as csvdataset:
            readtags = csv.reader(csvdataset, delimiter=',', lineterminator="\n")
            for row in readtags:
                if row[0] == "EOS":
                    self.runViterbi()
                    self.verify()
                    self.sentence = []
                    self.tagged = {}
                else:
                    self.sentence.append(row[0].lower())
                    self.tagged[row[0]] = row[1:]