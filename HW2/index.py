#!/usr/bin/python
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer
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

def process_file(f):
    """Process individual file
    
    """
    
    with open(f, 'r') as f:
        data = f.read().decode('utf8')
        words = [word_tokenize(w) for w in sent_tokenize(data)]
        flattened_list = itertools.chain.from_iterable(words)
        stemmer = PorterStemmer()
        stemmed_list = [stemmer.stem(w.lower()) for w in flattened_list]

    return stemmed_list
        

def build_index(docs_directory, dict_file, postings_file):
    training_files = sorted([f for f in os.listdir(docs_directory)], key=lambda x: os.path.basename(x))
    training_files = training_files[:5]  # TODO: omit this
    for f in training_files:
        contents = process_file(os.path.join(docs_directory, f))
        print contents
    

    
    
        

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
