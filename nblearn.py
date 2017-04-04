# Open the file for reading.
from collections import defaultdict
import math
import re

with open('train-text.txt', 'r') as file:
    # Read the contents of the file into memory.
    data1 = file.read()
file.close()
# Return a list of the lines, breaking at line boundaries.
my_list = data1.splitlines()

# Open the file for reading.
with open('train-labels.txt', 'r') as file:
    # Read the contents of the file into memory.
    data2 = file.read()
file.close()
# Return a list of the lines, breaking at line boundaries.
labels = data2.splitlines()

# Create a new dictionary :- line_list
line_list = {}
# Each line in the original file is split up into key: ID and value: sentence in the dictionary
for l in my_list:
    review_data = l.split(" ", 1)
    line_list[review_data[0]] = review_data[1]
# Converting all characters of each sentence to lower case
for id, sentence in line_list.items():
    line_list[id] = sentence.lower()

# Create a new dictionary :- vocabulary (to store the words and their count)

vocabulary = defaultdict(int)

for id, sentence in line_list.items():
    words = sentence.split()
    for i in words:
        i = re.sub(r'[^\w\s]', '', i)
        key = i
        if key in vocabulary:
            vocabulary[key] += 1
        else:
            vocabulary[key] = 1

sorted_keys = sorted(vocabulary, key=vocabulary.get, reverse=True)

# for r in sorted_keys:
#     print r, vocabulary[r]

ignorelist = ["the","and","a","i","was","in","of","for","it","at","my","is","that","were","with","this","had","on","they","have","there","you","be"]
# greaterwords = []

for word, count in vocabulary.items():
    if word in ignorelist:
        temp = word
        del vocabulary[word]

# Create a list for deceptive labels
deceptive = []
# Create a list for truthful labels
truthful = []
# Create a list for negative labels
negative = []
# Create a list for positive labels
positive = []

# for each item in each label-sentence segregate into deceptive,positive,truthful,negative
for i in labels:
    items = i.split()
    if items[1] == "deceptive":
        deceptive.append(items[0])
    if items[1] == "truthful":
        truthful.append(items[0])
    if items[2] == "negative":
        negative.append(items[0])
    if items[2] == "positive":
        positive.append(items[0])

# Create a dictionary for each type to count the word occurences in each type
d_wordcount = defaultdict(int)
t_wordcount = defaultdict(int)
n_wordcount = defaultdict(int)
p_wordcount = defaultdict(int)

# Update the word count of each word in each sentence according to appropriate category
for id, sentence in line_list.items():
    words = sentence.split()
    for i in words:
        i = re.sub(r'[^\w\s]', '', i)
        if i not in ignorelist:
            if id in deceptive:
                if i in d_wordcount:
                    d_wordcount[i] += 1
                else:
                    d_wordcount[i] = 1
            if id in truthful:
                if i in t_wordcount:
                    t_wordcount[i] += 1
                else:
                    t_wordcount[i] = 1
            if id in positive:
                if i in p_wordcount:
                    p_wordcount[i] += 1
                else:
                    p_wordcount[i] = 1
            if id in negative:
                if i in n_wordcount:
                    n_wordcount[i] += 1
                else:
                    n_wordcount[i] = 1

# print "positive=",p_wordcount
# print "negative=",n_wordcount
## print "deceptive=",d_wordcount
sorted_keys = sorted(t_wordcount, key=t_wordcount.get, reverse=True)

for r in sorted_keys:
    print r, t_wordcount[r]

print "truthful=",t_wordcount

classes = ["deceptive", "truthful", "positive", "negative"]

conditional_probability = defaultdict(float)

n = float(len(line_list))
for c in classes:
    if c == "deceptive":
        n1 = float(len(deceptive))
        prior_d = float(n1 / n)
        sum = 0
        for k, value in d_wordcount.iteritems():
            sum = sum + d_wordcount[k]
        for token in vocabulary:
            cp = float(float(d_wordcount[token] + 1) / float(sum + len(vocabulary)))
            string = token + " | " + c
            conditional_probability[string] = cp
    if c == "negative":
        n2 = float(len(negative))
        prior_n = float(n2 / n)
        sum = 0
        for k, value in n_wordcount.iteritems():
            sum = sum + n_wordcount[k]
        for token in vocabulary:
            cp = float(float(n_wordcount[token] + 1) / float(sum + len(vocabulary)))
            string = token + " | " + c
            conditional_probability[string] = cp
    if c == "positive":
        n3 = float(len(positive))
        prior_p = float(n3 / n)
        sum = 0
        for k, value in p_wordcount.iteritems():
            sum = sum + p_wordcount[k]
        for token in vocabulary:
            cp = float(float(p_wordcount[token] + 1) / float(sum + len(vocabulary)))
            string = token + " | " + c
            conditional_probability[string] = cp
    if c == "truthful":
        n4 = float(len(truthful))
        prior_t = float(n4 / n)
        sum = 0
        for k, value in t_wordcount.iteritems():
            sum = sum + t_wordcount[k]
        for token in vocabulary:
            cp = float(float(t_wordcount[token] + 1) / float(sum + len(vocabulary)))
            string = token + " | " + c
            conditional_probability[string] = cp

text_file = open("nbmodel.txt", "w")
for i in conditional_probability:
    text_file.write("%s: %f\n" % (i, conditional_probability[i]))
text_file.close()

# ----------------------------------------------------------------------------------------------------------------------
#
# Open the file for reading.
with open('test-text.txt', 'r') as file:
    # Read the contents of the file into memory.
    data3 = file.read()
file.close()
# Return a list of the lines, breaking at line boundaries.
test_list = data3.splitlines()

# Create a new dictionary :- testline_list
testline_dict = {}
# Each line in the original file is split up into key: ID and value: sentence in the dictionary
for l in test_list:
    test_data = l.split(" ", 1)
    testline_dict[test_data[0]] = test_data[1]

# Converting all characters of each sentence to lower case
for id, sentence in testline_dict.items():
    testline_dict[id] = sentence.lower()

answers = []

for id, sentence in testline_dict.items():
    words = sentence.split()
    for i in words:
        i = re.sub(r'[^\w\s]', '', i)
    # Compute scores of each class based on conditional probabilities
    for c in classes:
        if c == "deceptive":
            score1 = math.log(prior_d)
            # print score1
            for t in words:
                s = ""
                s = t + " | " + c
                if s in conditional_probability:
                    score1 += math.log(conditional_probability[s])
                    # print score1
        if c == "negative":
            score2 = math.log(prior_n)
            # print score2
            for t in words:
                s = ""
                s = t + " | " + c
                if s in conditional_probability:
                    score2 += math.log(conditional_probability[s])
                    # print score2
        if c == "positive":
            score3 = math.log(prior_p)
            # print score3
            for t in words:
                s = ""
                s = t + " | " + c
                if s in conditional_probability:
                    score3 += math.log(conditional_probability[s])
                    # print score3
        if c == "truthful":
            score4 = math.log(prior_t)
            # print score4
            for t in words:
                s = ""
                s = t + " | " + c
                if s in conditional_probability:
                    score4 += math.log(conditional_probability[s])
    maximum = max(score2, score3)
    maximum1 = max(score1, score4)
    # print "id is %s\n" % id
    if maximum1 == score1:
        flag1 = "deceptive"
    elif maximum1 == score4:
        flag1 = "truthful"
    if maximum == score2:
        flag2 = "negative"
    elif maximum == score3:
        flag2 = "positive"
    answer = id + " " + flag1 + " " + flag2
    answers.append(answer)

text_file = open("nboutput.txt", "w")
for i in answers:
    text_file.write("%s\n" % i)
text_file.close()

with open('nboutput.txt', 'r') as file:
    # Read the contents of the file into memory.
    data4 = file.read()
file.close()
# Return a list of the lines, breaking at line boundaries.
ans = data4.splitlines()

with open('test-labels.txt', 'r') as file:
    # Read the contents of the file into memory.
    data5 = file.read()
file.close()
# Return a list of the lines, breaking at line boundaries.
lab = data5.splitlines()

pred = 0.0
pret = 0.0
pren = 0.0
prep = 0.0
red = 0.0
ret = 0.0
rep = 0.0
ren = 0.0
f1d = 0.0
f1p = 0.0
f1n = 0.0
f1t = 0.0
tpd = 0.0
tpt = 0.0
tpn = 0.0
tpp = 0.0
fpd = 0.0
fpt = 0.0
fpn = 0.0
fpp = 0.0
fnd = 0.0
fnt = 0.0
fnn = 0.0
fnp = 0.0

zipped = zip(ans, lab)
for i, j in zipped:
    sen1 = i.split()
    sen2 = j.split()
    dt1 = sen1[1]
    pn1 = sen1[2]
    dt2 = sen2[1]
    pn2 = sen2[2]
    if (dt2 == "deceptive"):
        if (dt1 == dt2):
            tpd += 1
        else:
            fnd += 1
            fpt += 1
    if (dt2 == "truthful"):
        if (dt1 == dt2):
            tpt += 1
        else:
            fnt += 1
            fpd += 1
    if (pn2 == "positive"):
        if (pn1 == pn2):
            tpp += 1
        else:
            fnp += 1
            fpn += 1
    if (pn2 == "negative"):
        if (pn1 == pn2):
            tpn += 1
        else:
            fnn += 1
            fpp += 1
print "tpp =%f" % tpp
print "tpn =%f" % tpn
print "tpt =%f" % tpt
print "tpd =%f" % tpd

print "fpp =%f" % fpp
print "fpn =%f" % fpn
print "fpt =%f" % fpt
print "fpd =%f" % fpd

print "fnp =%f" % fnp
print "fnn =%f" % fnn
print "fnt =%f" % fnt
print "fnd =%f" % fnd

pred = float(tpd / (tpd + fpd))
pret = float(tpt / (tpt + fpt))
prep = float(tpp / (tpp + fpp))
pren = float(tpn / (tpn + fpn))
print "pred =%f" % pred
print "pret=%f" % pret
print "prep =%f" % prep
print "pren =%f" % pren

red = float(tpd / (tpd + fnd))
ret = float(tpt / (tpt + fnt))
rep = float(tpp / (tpp + fnp))
ren = float(tpn / (tpn + fnn))
print "red =%f" % red
print "ren =%f" % ren
print "rep =%f" % rep
print "ret =%f" % ret

f1d = float((2 * pred * red) / (pred + red))
f1p = float((2 * prep * rep) / (prep + rep))
f1n = float((2 * pren * ren) / (pren + ren))
f1t = float((2 * pret * ret) / (pret + ret))
print "f1d =%f" % f1d
print "f1p =%f" % f1p
print "f1t =%f" % f1t
print "f1n =%f" % f1n

print (f1d+f1p+f1n+f1t)/4