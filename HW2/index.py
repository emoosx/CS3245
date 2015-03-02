#!/usr/bin/python
import getopt
import sys

# Apply tokenization and stemming on the document text.
# You should use NLTK tokenizers (nltk.sent_tokenize() and nltk.word_tokenize())
# to tokenize sentences and words, and the NLTK Porter stemmer
# (class nltk.stem.porter ) to do stemming. You need to do case-folding to reduce
# all words to lower case.

# Implement skip pointers in the postings lists.

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
    print opts
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

    print doc_directory, dictionary_file, postings_file


if __name__ == '__main__':
    main()
