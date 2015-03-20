from collections import Counter
from nltk.stem.porter import PorterStemmer
from nltk import word_tokenize
from math import log10, sqrt
from result_heap import ResultHeap
import cPickle as pickle


class SearchIndex:
    def __init__(self, dictionary_file, postings_file):
        with open(dictionary_file, 'rb') as dfile:
            self.dictionary = pickle.load(dfile)
        self.postings = open(postings_file, 'rb')
        self.stemmer = PorterStemmer()
        with open('FILE_COUNT', 'rb') as fcount:
            self.N = int(fcount.read())

    def get_postings(self, term):
        """ Get postings list for a given term """
        if term in self.dictionary:
            self.postings.seek(self.dictionary[term][1])
            results = pickle.load(self.postings)
            return results
        return []

    def cal_log_tfs(self, freq):
        return 1 + log10(freq) if freq else 0

    def cal_idf(self, term):
        return log10(self.N/self.dictionary[term][2]) \
            if term in self.dictionary else 0

    def tfs_idf(self, term, freq):
        return self.cal_log_tfs(freq) * self.cal_idf(term)

    def normalize_vector(self, terms, weight_function):
        """ Normalize vector, using a given weight_function."""
        factor = 0
        for key, value in terms.iteritems():
            weight = weight_function(key, value)
            terms[key] = weight
            factor += weight ** 2
        return {key: (value/factor)
                for key, value in terms.iteritems()} if factor else {}

    def compute_cosine_scores(self, query_vector):
        scores = {}
        denom = {}
        for term, value in query_vector.iteritems():
            postings = self.get_postings(term)
            for p in postings:
                doc, tf = p[0], p[1]
                # scores[doc] += w(t,d)*w(t,q)
                if doc in scores:
                    scores[doc] += value * self.cal_log_tfs(tf)
                else:
                    scores[doc] = value * self.cal_log_tfs(tf)
        return scores


    def search(self, query):
        """ Entry point of search
        - case-folding and stemming
        - calculate weights for each query term (tf * idf)
        - normalize query vector
        - lnc.ltc
        """
        terms = map(lambda x: self.stemmer.stem(x), word_tokenize(query))
        terms = dict(Counter(terms))
        query_vector = self.normalize_vector(terms, self.tfs_idf)

        if not any(query_vector):
            return []

        cosine_scores = self.compute_cosine_scores(query_vector)
        return cosine_scores

        # scores = {}
        # denom = {}
        # for term, value in query_vector.iteritems():
            # postings = self.get_postings(term)
            # for doc in postings:
                # if doc[0] in scores:
                    # scores[doc[0]] += self.cal_tfs(doc[1]) * value
                    # denom[doc[0]] += self.cal_tfs(doc[1]) ** 2
                # else:
                    # scores[doc[0]] = self.cal_tfs(doc[1]) * value
                    # denom[doc[0]] = self.cal_tfs(doc[1]) ** 2

        # for k, v in scores.iteritems():
            # d = sqrt(denom[k])
            # if d == 0:
                # continue
            # scores[k] = v/sqrt(denom[k])

        # def comparator(x, y):
            # if x[0] > y[0]:
                # return -1
            # elif x[0] < y[0]:
                # return 1
            # else:
                # return -1

        # h = []
        # for docId, score in scores.iteritems():
            # h.append((score, int(docId)))
        # h.sort(comparator)

        # return map(lambda x: x[1], h[:10])
