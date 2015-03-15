__author__ = 'akanksha'

import csv
from brillsTagset import BrillsTagset


def splitsentences(line):
    sent_list = []
    p = line.find('./.')
    if p == -1:
        return [line]
    while p != -1:
        sent_list.append(line[:p + 3])
        line = line[p + 3:]
        p = line.find('./.')
    return sent_list


class CombineAll:

    def __init__(self, filename, filetowrite):

        self.filename = filename
        self.filetowrite = filetowrite

        tobj = BrillsTagset()
        self.tagset = tobj.getTagset()
        self.sent_count = 0

        self.sentence = []
        self.count = 0

        self.getfilecontents()

    # count of sentences read
    def getsentcount(self):
        return self.sent_count

    # the function that reads the files and appends them into a csv
    def getfilecontents(self):
        fread = open(self.filename)
        string = []
        for line in fread:
            string.append(line[:-1])
        string = ' '.join((' '.join(string)).split()).split('=')
        contents = []
        for each in string:
            each = each.strip()
            if each:
                contents.append(each)
        for each in contents:
            l = splitsentences(each)
            self.sentence = self.sentence + l

        csvdataset = open(self.filetowrite, 'a')
        wr = csv.writer(csvdataset, lineterminator="\n")
        errorlog = open('errorlog.txt', 'a')

        for eachword in self.sentence:
            for pair in eachword.split():
                if '\/' in pair:
                    pair = pair.replace('\/', '*slashhere*')
                    errorlog.write("In file " + self.filename + "at sentence " + pair + "\/ exists." + pair + "\n\n")
                s = pair.split("/")
                word_tag = [s[0].lower()]
                for each in s[1:]:
                    if '&' in each:
                        word_tag = word_tag + [each.split('&')[0]]
                    else:
                        word_tag = word_tag + each.split('|')

                # Ignore chunking boundaries
                if '[' not in word_tag and ']' not in word_tag:
                    word_tag[0].replace('*slashhere*', '\/')
                    if len(word_tag) > 2:
                        errorlog.write("In file " + self.filename + "at sentence :" + each + "multiple tags: " + ' '.join(
                            word_tag) + "\n\n")
                    for tag in word_tag[1:]:
                        if tag not in self.tagset:
                            errorlog.write(
                                "In file " + self.filename + "at sentence :" + each + "tag doesn't exist " + " " + tag + "\n\n")
                    wr.writerow(word_tag)
                    self.count += 1
            wr.writerow(["EOS", "EOS"])
            self.sent_count += 1