import getopt
import sys

def search(dictionary_file, postings_file, query_file, output_file):
    print dictionary_file, postings_file, query_file, output_file

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
