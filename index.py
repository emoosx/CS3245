from nltk.stem.porter import PorterStemmer
from postings_list import PostingsList
from nltk import sent_tokenize, word_tokenize
import cPickle as pickle
import getopt
import sys
import os


sys.setrecursionlimit(10000)
dictionary = {}
postings = []

UNIVERSAL = 0
pointer = 1
stemmer = PorterStemmer()


def process_file(contents):
    """ Remove newlines and join them with a single space """
    contents = contents[0]
    return " ".join(map(lambda x: x.strip(), contents))


def index_content(content, docId):
    """ Generate tokens, do case-folding and stemming, create a dictionary
    and index each term.
    """
    words = map(word_tokenize, sent_tokenize(content))
    words = map(lambda x: [stemmer.stem(y.lower()) for y in x], words)
    words = {}.fromkeys([x for y in words for x in y]).keys()
    for word in words:
        index_word(word, docId)


def index_word(word, docId):
    """ Indexes the docId for a particular word, creates the skiplist for new words"""
    global pointer
    if word not in dictionary:
        dictionary[word] = pointer
        plist = PostingsList()
        plist.append(docId)
        postings.insert(pointer, plist)
        pointer += 1
    else:
        postings[dictionary[word]].append(docId)


def init_universal_set():
    dictionary["UNIVERSAL"] = UNIVERSAL
    postings.insert(UNIVERSAL, "")


def main():
    """
    This is the point of entry. Does initialization, retrieve files' content,
    do indexing, generation diction and postings_files.
    """
    init_universal_set()
    data = os.listdir(dir_to_index)
    data.sort(key=lambda x: int(x))
    for d in data:
        filepath = os.path.join(dir_to_index, d)
        with open(filepath, 'r') as f:
            content = " ".join(map(lambda x: x.strip(), f.readlines()))
            index_content(content, d)
            postings[UNIVERSAL] += str(d) + ' '  # also put in universal set
    create_files()


def create_files():
    """ Generate skips, write dicitoinary and postings to file. """
    with open(postings_file, 'w+b') as fpostings:
        for key, value in dictionary.iteritems():
            if key != "UNIVERSAL": # no need to gen skips for universal set
                postings[value].generate_skips()
            dictionary[key] = (value, fpostings.tell(), len(postings[value]))
            pickle.dump(postings[value], fpostings, pickle.HIGHEST_PROTOCOL)

    with open(dict_file, 'wb') as fdict:
        pickle.dump(dictionary, fdict, pickle.HIGHEST_PROTOCOL)


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
