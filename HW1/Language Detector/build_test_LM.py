#!/usr/bin/python
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from pprint import pprint
from itertools import groupby
import nltk
import re
import sys
import getopt


def build_ngram(n, line):
    """strip out the name of the language, build ngram from a given
    string input line. Includes left and right paddings
    """

    lang, line = line[:line.find(' ')], line[line.find(' ') + 1:]
    return (lang, ngrams(line, n, pad_left=True, pad_right=True))


def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and an URL separated by a tab(\t)
    """
    print 'building language models...'

    languages = {}
    with open(in_file) as f:
        lines = f.readlines()
        four_grams = groupby((build_ngram(4, l) for l in lines), lambda x: x[0])
        languages = dict((key, list(group)[0][1]) for key, group in four_grams)
        pprint(languages)

def test_LM(in_file, out_file, LM):
    """
    test the language models on new URLs
    each line of in_file contains an URL
    you should print the most probable label for each URL into out_file
    """
    print "testing language models..."
    # This is an empty method
    # Pls implement your code in below

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
