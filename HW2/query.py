class Query:

    def __init__(self, qtuple):
        if(len(qtuple) == 3):
            if qtuple[1] > qtuple[2]:
                qtuple = (qtuple[0], qtuple[2], qtuple[1])
            else:
                qtuple = (qtuple[0], qtuple[1], qtuple[2])
        self.operator = qtuple[0]
        self.qtuple = qtuple

    def __str__(self):
        return 'Q%s' % str(self.qtuple)

    def __repr__(self):
        return str(self)
