from boolean_operator import Operator
import re


class QueryTree(object):
    def __init__(self, string = None):
        self.operator = None
        self.left = None
        self.right = None
        self.string = None
        self.estimate = None
        self.processed = False

        while string is not None and self.construct(string) is True:
            pass

    def preprocess(self):
        # optimize by sort of cancelling nested nots
        if self.operator == Operator.NOT and self.right.operator == Operator.NOT:
            self = self.right.right
            self.preprocess()

    def withParen(self, string, pos):
        """ Checks whethers the given pos in the string lies within parentheses """
        fst = string.rfind('(', 0, pos)
        if fst != -1:
            cls = string.rfind(')', fst, pos)
            if cls == -1:
                return True
        return False

    def construct(self, string):
        """ Construct string repr of query tree by scanning for operators and retriving subquery clauses.
            Build the query tree recursively. Tries all OR, AND clauses and continue to
            NOT, () later.
        """
        string.strip()
        for match in re.finditer(r"NOT ", string):
            pos = match.start()
            if string[pos+4:] and not self.withParen(string, pos):
                self.operator = Operator.NOT
                self.right = QueryTree(string[pos+4:])
                return False

        for match in re.finditer(r" OR ", string):
            pos = match.start()
            if string[:pos] and string[pos+4:] and not self.withParen(string, pos):
                self.operator = Operator.OR
                self.left = QueryTree(string[:pos])
                self.right = QueryTree(string[pos+4:])
                return False

        for match in re.finditer(r" AND ", string):
            pos = match.start()
            if string[:pos] and string[pos+5:] and not self.withParen(string, pos):
                self.operator = Operator.AND
                self.left = QueryTree(string[:pos])
                self.right = QueryTree(string[pos+5:])
                return False

        # ()
        regex  = re.compile(r'(.*)\(([^\(\)]+)\)(.*)')
        matcher = regex.match(string)

        if matcher is not None and matcher.groups()[1]:
            g = matcher.groups()
            self.construct(g[1])
            return False

        self.string = string.strip()
        return False
