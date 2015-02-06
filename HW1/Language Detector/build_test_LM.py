#!/usr/bin/python
from collections import defaultdict
from itertools import groupby, chain
from math import log
import sys
import getopt

model = {}
all_ngrams = set()


def get_ngrams(line, n, pad_left=True, pad_right=True, word_based=False):
    """ Lazily build ngram from a given
    string input line. Includes left and right paddings by default
    padding_character = None
    """

    if(word_based):
        line = line.split(' ')

    line = iter(line)
    if pad_left:
        line = chain((None,) * (n-1), line)
    if pad_right:
        line = chain(line, (None,) * (n-1))

    result = [next(line) for i in range(n-1)]
    for gram in line:
        result.append(gram)
        yield tuple(result)
        del result[0]


def build_ngrams(line, n, need_splitting=True):
    if need_splitting:
        lang, line = line[:line.find(' ')], line[line.find(' ') + 1:]
        return (lang, get_ngrams(line, 4))
    else:
        return get_ngrams(line, 4)


def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and an URL separated by a tab(\t)
    """
    print 'building language models...'

    # do this cos question explicity states the given urls are in these
    # three languages only
    languages = ['malaysian', 'indonesian', 'tamil']
    for l in languages:
        model[l] = defaultdict(lambda: 1)   # takes cares of one-smoothing

    with open(in_file) as f:
        four_grams = groupby((build_ngrams(l, 4) for l in f.readlines()),
                             lambda x: x[0])
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

    for ng in ngrams:
        if ng not in lm_dict:
            rouge_ngrams += 1
            continue
        else:
            prob = lm_dict.get(ng)/float(len(lm_dict))
            total_prob += log(prob)

    # if there are a lot of rouge ngrams,
    # chances are that it's in  a language we don't know
    if(float(rouge_ngrams) / len(ngrams)) > 0.5:
        total_prob = None

    return (lm, total_prob)


def test_LM(in_file, out_file, LM):
    """
    test the language models on new URLs
    each line of in_file contains an URL
    you should print the most probable label
    for each URL into out_file
    """
    print "testing language models..."
    output = open(out_file, "wb")
    with open(in_file) as f:
        lines = f.readlines()
        for line in lines:
            ngrams = list(build_ngrams(line, 4, False))
            prediction = max((calculate_probability(lm, ngrams)
                              for lm in model), key=lambda x: x[1])
            output.write('%s %s' % (prediction[0] if prediction[1] is not None
                                    else 'other', line))
    output.close()


def usage():
    print "usage: " + sys.argv[0] + " -b input-file-for-building-LM -t \
    input-file-for-testing-LM -o output-file"

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
if input_file_b is None or input_file_t is None or output_file is None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
