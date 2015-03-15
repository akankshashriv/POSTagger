__author__ = 'akanksha'

import os
from brillsTagset import BrillsTagset
from combineData import CombineAll
from splitData import SplitData
from calcWordCatAllData import CalcWordCatAllData
from calcFreq import CalculateEachFrequency
from calProb import CalculateProb
from classifyTestDataBigram import ClassifyTestDataBigram
from classifyTestDataTrigram import ClassifyTestDataTrigram

tagset = BrillsTagset().getTagset()

# if os.path.isfile("orderedtags.csv"):
#     os.remove("orderedtags.csv")
# if os.path.isfile("errorlog.txt"):
#     os.remove("errorlog.txt")
#
fileAllData = "orderedtags.csv"
#
# c = 0
# count = 0
# for root, dirs, files in os.walk("../WSJ-2-12/02"):
#     for f in files:
#         filepath = os.path.join(root, f)
#         combine = CombineAll(filepath, fileAllData)
#         count += combine.getsentcount()
#         c += 1
#     print c
# print count

# Split Data from orderedtags.csv
# split = SplitData(fileAllData, "Datasets", count)

# Calculate Frequencies of words in different categories in 100% of data
wordCatFreqAll = CalcWordCatAllData(fileAllData, "Datasets", tagset)

for n in xrange(0, 10):
    # Calculate Frequencies for each dataset
    freq = CalculateEachFrequency("Datasets", n)

    # Calculate Probabilities for each dataset
    prob = CalculateProb("Datasets", n)

    # Classify Data in each set
    # classify = ClassifyTestDataBigram("Datasets", n, "p_cat1_cat2.pkl", "p_word_cat.pkl", "WordFreq.pkl", "accuracy" + str(n) + ".txt")
    # classify = ClassifyTestDataBigram("Datasets", n, "p_cat1_cat2.pkl", "p_word_cat_all.pkl", "WordFreq.pkl", "accuracy" + str(n) + "_all.txt")
    classify = ClassifyTestDataTrigram("Datasets", n, "p_cat1_cat2_cat3.pkl", "p_word_cat.pkl", "WordFreq.pkl", "accuracy" + str(n) + "_alltrigram.txt")

avg = 0.0
avg_all = 0.0
avg_tri = 0.0
for root, dirs, files in os.walk("Accuracy/"):
   for f in files:
       filepath = os.path.join(root, f)
       pointer = open(filepath, "r")
       c = map(float, pointer)
       print c
       if "all" in f:
           avg_all += float(c[0])
       elif "tri" in f:
           avg_tri += float(c[0])
       else:
           avg += float(c[0])

print avg/10, avg_all/10