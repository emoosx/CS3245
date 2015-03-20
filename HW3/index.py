from nltk.stem.porter import PorterStemmer
from collections import Counter
from nltk import sent_tokenize, word_tokenize
from search_index import SearchIndex
# from pprint import pprint
import cPickle as pickle
import getopt
import sys
import os


dictionary = {}
postings = []

pointer = 0
stemmer = PorterStemmer()


def get_each_file_term_frequency(content, docId):
    """ Generate tokens, do case-folding and stemming, create a dictionary
    and index each term.
    """
    words = map(word_tokenize, sent_tokenize(content))
    words = map(lambda x: [stemmer.stem(y.lower()) for y in x], words)
    words = [x for word in words for x in word]
    term_freq = dict(Counter(words))     # term frequencies for each document
    return term_freq


def index_content(term_freq, docId):
    """ Create postings lists by populating the global poinstgs list with
    terms and adding respective term frequencies. """
    global pointer
    for word, freq in term_freq.iteritems():
        if word not in dictionary:
            dictionary[word] = pointer
            postings.insert(pointer, [[docId, freq]])
            pointer += 1
        else:
            postings[dictionary[word]].append([docId, freq])


def main():
    """
    This is the point of entry. Does initialization, retrieve files' content,
    do indexing, generation diction and postings_files.

    Make another pass to calculate doc weights (tf * 1)
    """

    data = sorted(os.listdir(dir_to_index), key=int)
    for d in data:
        filepath = os.path.join(dir_to_index, d)
        with open(filepath, 'r') as f:
            content = " ".join(map(lambda x: x.strip(), f.readlines()))
            term_freq = get_each_file_term_frequency(content, d)
            index_content(term_freq, d)

    # make another pass to calculate weights
    for word, pointer in dictionary.iteritems():
        for doc in postings[pointer]:
            doc.append(SearchIndex.cal_log_tfs(doc[1]))

    # pprint(postings)
    create_files(len(data))


def create_files(file_count):
    """ Write dictionary and postings to file."""
    with open(postings_file, 'w+b') as fpostings:
        for key, value in dictionary.iteritems():
            dictionary[key] = (value, fpostings.tell(), len(postings[value]))
            pickle.dump(postings[value], fpostings, pickle.HIGHEST_PROTOCOL)

    with open(dict_file, 'wb') as fdict:
        pickle.dump(dictionary, fdict, pickle.HIGHEST_PROTOCOL)

    with open('FILE_COUNT', 'wb') as fcount:
        fcount.write(str(file_count))


def usage():
    print "python index.py -i directory-of-documents \
        -d dictionary-file -p postings-file"

dir_to_index = None
dict_file = None
postings_file = None

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
    except getopt.GetoptError, err:
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == '-i':
            dir_to_index = a
        elif o == '-d':
            dict_file = a
        elif o == '-p':
            postings_file = a
        else:
            assert False, "unhandled option"

    if dir_to_index is None or dict_file is None or postings_file is None:
        usage()
        sys.exit(0)

    main()
