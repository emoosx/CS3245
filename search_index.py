from nltk.stem.porter import PorterStemmer
from querytree import QueryTree
from boolean_operator import Operator
from postings_list import PostingsList
import cPickle as pickle


class SearchIndex:
    def __init__(self, dictionary_file, postings_file):
        with open(dictionary_file, 'rb') as dfile:
            self.dictionary = pickle.load(dfile)
        self.postings = open(postings_file, 'rb')
        self.stemmer = PorterStemmer()
        self.UNIVERSAL = None
        self.initialize()

    def initialize(self):
        self.search("UNIVERSAL")

    def get_results(self, operator, *lists):
        """ Execute intermediate sub query clauses"""
        if len(lists) is 0:
            raise "Two at least one list to execute"
        elif len(lists) is 1:
            return lists[0]
        else:
            lists = list(lists)
            lists.sort(key=len)
            return reduce(lambda x, y: self.execute(x, y, operator),
                          lists[1:], lists[0])

    def execute(self, left, right, op):
        if op is Operator.NOT:
            return self.execute_not(left, right)
        elif op is Operator.OR:
            return self.execute_or(left, right)
        elif op is Operator.AND:
            return self.execute_and(left, right)

    def execute_not(self, left, right):
        left = set(self.search("UNIVERSAL").get_list())
        right = set(right.get_list())
        return PostingsList(sorted(list(left-right), key=lambda x: int))

    def execute_or(self, left, right):
        sorted_list = sorted(dict.fromkeys(left.get_list() + right.get_list()).keys(), key=lambda x: int)
        result = PostingsList(sorted_list)
        result.generate_skips()
        return result

    def execute_and(self, left, right):
        result = PostingsList()
        left_node = left.root
        right_node = right.root

        while left_node is not None and right_node is not None:
            if left_node.val < right_node.val:
                if left_node.pointers is not None:
                    jump = False
                    for target in left_node.pointers:
                        if target.val <= right_node.val:
                            left_node = target
                            jump = True
                    if not jump:
                        left_node = left_node.next
                else:
                    left_node = left_node.next
            elif left_node.val > right_node.val:
                if right_node.pointers is not None:
                    jump = False
                    for target in right_node.pointers:
                        if target.val <= left_node.val:
                            right_node = target
                            jump = True
                    if not jump:
                        right_node = right_node.next
                else:
                    right_node = right_node.next
            else:
                result.append(left_node.val)
                left_node = left_node.next
                right_node = right_node.next
        result.generate_skips()
        return result

    def build_querytree(self, query_string):
        query_tree = QueryTree(query_string)
        self.guess_results(query_tree)
        return query_tree

    def process(self, query):
        if query is not None and query.estimate == 0:
            return PostingsList()

        # query subclause
        if query is not None and query.operator is not None:
            if query.operator == Operator.AND or query.operator == Operator.OR:
                return self.get_results(query.operator,
                                        self.process(query.left),
                                        self.process(query.right))
            elif query.operator == Operator.NOT:
                return self.get_results(query.operator, PostingsList(),
                                        self.process(query.right))

        # a regular term
        elif query.string is not None:
            return self.search(query.string)

    def guess_results(self, query_tree):
        """ For optimization purpose, try to "guess" the result's length of max result """
        if query_tree.estimate is None:
            if query_tree.operator is not None:

                if query_tree.operator == Operator.NOT:
                    self.guess_results(query_tree.right)
                    full_length = len(self.UNIVERSAL)
                    query_tree.estimate = full_length - \
                        query_tree.right.estimate
                    return

                # AND, OR
                self.guess_results(query_tree.left)
                self.guess_results(query_tree.right)
                if query_tree.operator == Operator.OR:
                    query_tree.estimate = min(len(self.UNIVERSAL), query_tree.left.estimate + query_tree.right.estimate)
                elif query_tree.operator == Operator.AND:
                    query_tree.estimate = min(query_tree.left.estimate, query_tree.right.estimate)
            else:
                s = self.stemmer.stem(query_tree.string.lower())
                if s in self.dictionary:
                    query_tree.estimate = self.dictionary[s][2]
                else:
                    query_tree.estimate = 0

    def search(self, term):
        if self.UNIVERSAL is not None:
            return self.UNIVERSAL
        elif term != 'UNIVERSAL':
            term = self.stemmer.stem(term.lower())

        if term in self.dictionary:
            index = self.dictionary[term][1]
            self.postings.seek(index)
            results = pickle.load(self.postings)
            if term == "UNIVERSAL":
                results = PostingsList(results.split())
                self.UNIVERSAL = results
            return results
        else:
            return PostingsList()
