#!/usr/bin/python
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer
from skip_list import SkipList
import cPickle as pickle
import os
import getopt
import sys
import itertools

# At the end of the indexing phase, you are to write the dictionary into `dictionary-file`
# and the postings into `posting-file`

# Apply tokenization and stemming on the document text.
# You should use NLTK tokenizers (nltk.sent_tokenize() and nltk.word_tokenize())
# to tokenize sentences and words, and the NLTK Porter stemmer
# (class nltk.stem.porter ) to do stemming. You need to do case-folding to reduce
# all words to lower case.

# Implement skip pointers in the postings lists.
# math.sqrt(len(posting)) skip pointers are evenly placed on the a postings list.
# Although implementing skip pointers takes up extra disk space, it provides a shortcut
# to efficiently merge two postings lists, thus boosting the searching speed.


# Read each file in the training dir

TEMP_DIR = 'temp'
pointer = 0


def process_file(f):
    """Process individual file
        - Decode the string as a unicode string (in case there are unicode characters)
        - Tokenize each sentence
        - For each sentence, tokenize words
        - Flatten the list
        - Apply casefolding and stemming for each word
    """
    stemmer = PorterStemmer()
    invalid_chrs = [',', '-', '.', '..', '&', '(', ')', '"', "'"]
    with open(f, 'rb') as f:
        data = f.read()
        words = (word_tokenize(''.join(w.split('/')))for w in sent_tokenize(data))
        flattened_list = itertools.chain.from_iterable(words)
        stemmed_list = [stemmer.stem(w.lower()) for w in flattened_list if w not in invalid_chrs]
    return stemmed_list


def create_temp_file(terms, doc_id):
    for term in terms:
        filepath = os.path.join(os.getcwd(), TEMP_DIR, term)
        if not os.path.isfile(filepath):
            with open(filepath, 'wb') as f:
                f.write(doc_id)
        else:
            with open(filepath, 'ab') as f:
                f.write("," + doc_id)
        

def build_dictionary(terms, dictionary, doc_id, postings):
    """Build a dictionary and respective postings list from the terms"""
    global pointer
    for term in terms:
        if term not in dictionary:
            skip_list = SkipList()
            skip_list.append(doc_id)
            dictionary[term] = [len(skip_list), pointer]
            postings.insert(pointer, skip_list)
        else:
            pointer = dictionary[term][1]
            postings[dictionary[term][1]].append(doc_id)
            dictionary[term][0] += 1
        pointer += 1


def create_files(dictionary, dict_file, postings, postings_file):
    with open(postings_file, "w+b") as pfile:
        for key, value in dictionary.iteritems():
            postings[value[1]].create_skip_pointers()
            dictionary[key] = (value, len(postings[value[1]]), pfile.tell())
            pickle.dump(postings[value[1]], pfile, pickle.HIGHEST_PROTOCOL)

    with open(dict_file, 'wb') as dfile:
        pickle.dump(dictionary, dfile, pickle.HIGHEST_PROTOCOL)

            
def build_index(docs_directory, dict_file, postings_file):
    dictionary = {}
    postings = []

    training_files = sorted([f for f in os.listdir(docs_directory)], key=lambda x: os.path.basename(x))
    training_files = training_files[:100]  # TODO: omit this

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    for f in training_files:
        terms = process_file(os.path.join(docs_directory, f))
        # create_temp_file(terms, f)
        build_dictionary(terms, dictionary, f, postings)

    create_files(dictionary, dict_file, postings, postings_file)
    

def usage():
    print "usage: " + sys.argv[0] + " -i directory-of-documents " \
        "-d dictionary-file -p postings-file"


def main():
    doc_directory = dictionary_file = postings_file = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
    except getopt.GetoptError, err:
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == '-i':
            doc_directory = a
        elif o == '-d':
            dictionary_file = a
        elif o == '-p':
            postings_file = a
        else:
            assert False, 'unhandled option'

    if doc_directory is None or dictionary_file is None or postings_file is None:
        usage()
        sys.exit(2)

    build_index(doc_directory, dictionary_file, postings_file)


if __name__ == '__main__':
    main()
