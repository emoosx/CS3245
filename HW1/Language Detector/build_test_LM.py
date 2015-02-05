#!/usr/bin/python
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from pprint import pprint
from collections import defaultdict
from itertools import groupby
from math import log
import nltk
import re
import sys
import getopt

model = {}
all_ngrams = set()

def build_ngram(n, line, build_lm=True):
    """strip out the name of the language, build ngram from a given
    string input line. Includes left and right paddings
    """

    if build_lm:
        lang, line = line[:line.find(' ')], line[line.find(' ') + 1:]
        return (lang, ngrams(line, n, pad_left=True, pad_right=True))
    else:
        return ngrams(line, n, pad_left=True, pad_right=True)


def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and an URL separated by a tab(\t)
    """
    print 'building language models...'

    languages = ['malaysian', 'indonesian', 'tamil']
    for l in languages:
        model[l] = defaultdict(lambda: 1)   # takes cares of one-smoothing

    with open(in_file) as f:
        lines = f.readlines()
        four_grams = groupby((build_ngram(4, l) for l in lines), lambda x: x[0])

        # for key, group in four_grams:
            # for ngs in group:
                # print key, list(ngs[1])

        for key, group in four_grams:
            for ngs in group:
                for ng in ngs[1]:
                    model[key][ng] += 1
                    all_ngrams.add(ng)

        for lm in model:
            for ng in all_ngrams:
                model[lm].setdefault(ng, 1)


def calculate_probability(lm, ngrams):
    """
    calculate probability of an individual sentence
    for individual language model
    """
    rouge_ngrams = 0
    total_prob = 0
    lm_dict = model[lm]

    for ng in list(ngrams):
        if not ng in lm_dict:
            rouge_ngrams += 1
            continue
        else:
            prob = lm_dict.get(ng)/float(len(lm_dict))
            total_prob += log(prob)
    return total_prob

def test_LM(in_file, out_file, LM):
    """
    test the language models on new URLs
    each line of in_file contains an URL
    you should print the most probable label for each URL into out_file
    """
    print "testing language models..."
    # pprint(model)
    # This is an empty method
    # Pls implement your code in below
    output = open(out_file, "wb")
    with open(in_file) as f:
        lines = f.readlines()
        for line in lines:
            ngrams = list(build_ngram(4, line, False))
            for lm in model:
                print "Answer : %s %f" % (lm, calculate_probability(lm, ngrams))
                # print "Answer: ", lm, calculate_probability(model[lm], ngrams)
            print ""
    output.close()


def usage():
    print "usage: " + sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
