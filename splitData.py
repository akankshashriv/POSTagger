__author__ = 'akanksha'
import csv
import os
import shutil


class SplitData:

    def __init__(self, filename, direc, count):
        self.filename = filename
        self.sent_count = count
        self.direc = direc
        self.split_sent = {}
        self.split()
        self.makedatasets()

    def split(self):
        with open(self.filename, 'r') as csvdataset:
            read_Data = csv.reader(csvdataset, delimiter=',', lineterminator="\n")
            c = 1
            for row in read_Data:
                index = (c*10)/self.sent_count
                if index not in list(self.split_sent.keys()):
                    self.split_sent[index] = []
                self.split_sent[index].append(row)
                if row[0] == 'EOS':
                    c += 1
            print list(self.split_sent.keys())

    def makedatasets(self):
        for x in range(0, 10):
            test = self.split_sent[x]
            train = self.split_sent
            del train[x]
            self.createdatafolders(x, test, train)

    def createdatafolders(self, n, test, train):
        filetest = self.direc + "/" + str(n) + "/test.csv"
        filetrain = self.direc + "/" + str(n) + "/train.csv"
        direc = os.path.dirname(filetest)

        if os.path.exists(direc):
            shutil.rmtree(direc, ignore_errors=True)
        os.makedirs(direc)

        csvdataset = open(filetest, 'w')
        wr = csv.writer(csvdataset, lineterminator="\n")
        for row in test:
            wr.writerow(row)

        csvdataset = open(filetrain, 'w')
        wr = csv.writer(csvdataset, lineterminator="\n")
        for each in train:
            for row in train[each]:
                wr.writerow(row)