import nblearn

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

import math
import re

for id, sentence in testline_dict.items():
    words = sentence.split()
    for i in words:
        i = re.sub(r'[^\w\s]', '', i)
    print words
    # Compute scores of each class based on conditional probabilities
    for c in nblearn.classes:
        if c == "deceptive":
            score1 = math.log(nblearn.prior_d)
            print score1
            for t in words:
                s = ""
                s = t + " | " + c
                if s in nblearn.conditional_probability:
                    score1 += math.log(nblearn.conditional_probability[s])
            print score1
        if c == "negative":
            score2 = math.log(nblearn.prior_n)
            print score2
            for t in words:
                s = ""
                s = t + " | " + c
                if s in nblearn.conditional_probability:
                    score2 += math.log(nblearn.conditional_probability[s])
            print score2
        if c == "positive":
            score3 = math.log(nblearn.prior_p)
            print score3
            for t in words:
                s = ""
                s = t + " | " + c
                if s in nblearn.conditional_probability:
                    score3 += math.log(nblearn.conditional_probability[s])
            print score3
        if c == "truthful":
            score4 = math.log(nblearn.prior_t)
            print score4
            for t in words:
                s = ""
                s = t + " | " + c
                if s in nblearn.conditional_probability:
                    score4 += math.log(nblearn.conditional_probability[s])
            print score4
    maximum = max(score2, score3)
    maximum1 = max(score1, score4)
    print "id is %s\n" % id
    if maximum1 == score1:
        flag1 = "deceptive"
        print "deceptive"
    elif maximum1 == score4:
        print "truthful"
        flag1 = "truthful"
    if maximum == score2:
        print "negative"
        flag2 = "negative"
    elif maximum == score3:
        print "positive"
        flag2 = "positive"
    answer = id + " " + flag1 + " " + flag2
    answers.append(answer)

text_file = open("nboutput.txt", "w")
for i in answers:
    text_file.write("%s\n" % i)
text_file.close()



for id, sentence in line_list.items():
    words = sentence.split()
    for i in words:
        #i = re.sub(r'[^\w\s]', '', i)
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