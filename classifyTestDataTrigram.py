__author__ = 'akanksha'

import sys
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


class ClassifyTestDataTrigram:

    tagset = generateTagset()

    def __init__(self, folder, n, pfile1, pfile2, pfile3, fname):
        self.folder = folder
        self.n = n
        self.fname = fname

        self.sentence = []
        self.tagged = {}
        self.classifiedBi = {}
        self.classifiedTri = {}
        self.correctcountBi = 0
        self.correctcountTri = 0
        self.allcount = 0

        self.p_cat1_cat2_cat3 = loadDict(self.folder + "/" + str(self.n) + "/" + pfile1)
        self.p_word_cat = loadDict(self.folder + "/" + str(self.n) + "/" + pfile2)
        self.word = loadDict(self.folder + "/" + str(self.n) + "/" + pfile3)

        self.classify()
        self.accuracy()

    # Function that writes accuracy in a txt file
    def accuracy(self):
        f = open("Accuracy/" + self.fname, 'wb')
        f.write(str(float(self.correctcountTri * 100)/self.allcount))

    # Function that verifies the new tags for each word against original tags
    # counted positively if new tag is any of the multiple tags
    def verify(self):
        fileoutput = self.folder + "/" + str(self.n) + "/taggedoutput_trigram.csv"
        csvdataset = open(fileoutput, 'a')
        wr = csv.writer(csvdataset, lineterminator="\n")
        for each in self.sentence:
            if self.classifiedTri[each] in self.tagged[each]:
                self.correctcountTri += 1
            wr.writerow([each, self.classifiedTri[each]])
            self.allcount += 1

    # Function that implements Viterbi for a trigram tagger
    def runViterbi(self):
        scoreTri = {}
        backpointerTri = {}

        for tag in ClassifyTestDataTrigram.tagset:
            scoreTri[tag] = {}
            scoreTri[tag]['start'] = {}
            backpointerTri[tag] = {}
            if self.sentence[0] in list(self.word.keys()):
                p2 = self.p_word_cat[self.sentence[0]][tag]
            else:
                p2 = 1
            scoreTri[tag]['start'][self.sentence[0]] = p2 * self.p_cat1_cat2_cat3[tag]['start']['start']

        backpointerTri['start'] = {}
        backpointerTri['start']['start'] = {}

        for tag in ClassifyTestDataTrigram.tagset:
            for tag2 in ClassifyTestDataTrigram.tagset: #u
                scoreTri[tag][tag2] = {}
                backpointerTri[tag][tag2] = {}
                if self.sentence[1] in list(self.word.keys()):
                    p2 = self.p_word_cat[self.sentence[1]][tag]
                else:
                    p2 = 1
                scoreTri[tag][tag2][self.sentence[1]] = scoreTri[tag2]['start'][self.sentence[0]] * self.p_cat1_cat2_cat3[tag][tag2]['start'] * p2
                backpointerTri[tag][tag2][self.sentence[1]] = 'start'

        c = 1
        prevword = self.sentence[0]
        for each in self.sentence[1:]:
            for tag in ClassifyTestDataTrigram.tagset: #v
                maxscoreTri = 0
                for tag2 in ClassifyTestDataTrigram.tagset: #u
                    if each in list(self.word.keys()):
                        p2 = self.p_word_cat[each][tag]
                    else:
                        p2 = 1
                    if c > 1:
                        for tag3 in ClassifyTestDataTrigram.tagset: #w
                            s2 = scoreTri[tag2][tag3][prevword] * self.p_cat1_cat2_cat3[tag][tag2][tag3] * p2
                            if maxscoreTri <= s2:
                                maxscoreTri = s2
                                maxtagTri = tag3
                        scoreTri[tag][tag2][each] = maxscoreTri
                        backpointerTri[tag][tag2][each] = maxtagTri
            prevword = each
            c += 1

        maxscoreTri = 0
    
        for each in ClassifyTestDataTrigram.tagset:
            for every in ClassifyTestDataTrigram.tagset:
                temp = scoreTri[each][every][self.sentence[-1]] * self.p_cat1_cat2_cat3['.'][every][each]
                if maxscoreTri <= temp:
                    maxscoreTri = temp
                    maxtagTri = [each, every]

        self.classifiedTri[self.sentence[-1]] = maxtagTri[1]
        self.classifiedTri[self.sentence[-2]] = maxtagTri[0]

        prevtag = maxtagTri[0]
        secprevtag = maxtagTri[1]
        prevword = self.sentence[-1]
        c=0
        for each in reversed(self.sentence):
            if c>1:
                self.classifiedTri[each] = backpointerTri[prevtag][secprevtag][prevword]
            if each in [")", "(", ",", ".", "#", "$", ":"]:
                self.classifiedTri[each] = each
            prevword = each
            secprevtag = prevtag
            prevtag = self.classifiedTri[each]
            c += 1

    # Function that reads the test data file - test.csv and forms sentences using the EOS marker
    # It then sends the sentence to be classified, after which it starts reading a new sentence
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