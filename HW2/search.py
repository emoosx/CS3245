from nltk.stem.porter import PorterStemmer
import cPickle as pickle
import getopt
import sys
import parser


def execute_query(query, dictionary, pfile):
    """Exectue individual query"""
    pass

def search(dictionary_file, postings_file, query_file, output_file):
    """ Entry point to the program """

    stemmer = PorterStemmer()
    with open(dictionary_file, "rb") as dfile:
        dictionary = pickle.loads(dfile.read())

    with open(query_file, "rb") as qfile:
        with open(postings_file, "rb") as pfile:
            for query in qfile:
                print "query: ", query
                prefix = parser.to_polish_notation(query)
                print "prefix: ", prefix
                processed = []
                for token in prefix:
                    if parser.is_operand(token):
                        token = stemmer.stem(token).lower()
                    processed.append(token)

                print "processed: ", processed
                query = parser.process_query(processed)
                print "query: ", query
                result = execute_query(query, dictionary, pfile)

                print result


def usage():
    print "usage: " + sys.argv[0] + " -d dictionary-file -p postings_file " \
        "-q file-of-queries -o output-file-of-results"


def main():
    dictionary_file = postings_file = query_file = output_file = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
    except getopt.GetoptError, err:
        usage()
        sys.exit(2)

    for o, a in opts:
        if o == '-d':
            dictionary_file = a
        elif o == '-p':
            postings_file = a
        elif o == '-q':
            query_file = a
        elif o == '-o':
            output_file = a
        else:
            assert False, 'unhandled option'


    if dictionary_file is None or postings_file is None or query_file is None \
       or output_file is None:
        usage()
        sys.exit(2)

    search(dictionary_file, postings_file, query_file, output_file)

if __name__ == '__main__':
    main()
