class Operator:
    OR = 0
    AND = 1
    NOT = 2
    PARANTHESES = 3

    @staticmethod
    def get(op):
        if op == 'OR':
            return Operator.OR
        elif op == 'AND':
            return Operator.AND
        elif op == 'NOT':
            return Operator.NOT
        else:
            raise 'Invalid operator : ' + op

    @staticmethod
    def str(op):
        if op == Operator.OR:
            return 'OR'
        elif op == Operator.AND:
            return 'AND'
        elif op == Operator.NOT:
            return 'NOT'
        else:
            raise 'Invalid Operator'

