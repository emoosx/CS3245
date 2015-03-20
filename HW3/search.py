from search_index import SearchIndex
import getopt
import sys


def main():
    search = SearchIndex(dictionary_file, postings_file)
    with open(query_file, 'r') as fquery:
        with open(output_file, 'w') as foutput:
            for query in fquery.readlines():
                result = search.search(query)
                print result
                # foutput.write(result + '\n')


def usage():
    print "python search.py -d dictionary-file -p postings-file \
            -q file-of-queries -o output-file-of-results"


query_file = dictionary_file = postings_file = output_file = None

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'q:d:p:o:')
    except getopt.GetoptError, err:
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == '-q':
            query_file = a
        elif o == '-d':
            dictionary_file = a
        elif o == '-p':
            postings_file = a
        elif o == '-o':
            output_file = a
        else:
            assert False, "unhandled option"

    if query_file is None or dictionary_file is None or postings_file is None or output_file is None:
        usage()
        sys.exit(0)

main()
