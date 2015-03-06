from query import Query


OPERATORS = ['NOT', 'AND', 'OR']
PRECEDENCE = {
    ')' : 4,
    '(' : 4,
    'NOT': 3,
    'AND': 2,
    'OR': 1
}


is_operator = lambda t: t in OPERATORS
is_brace = lambda t: t in ['(', ')']
is_operand = lambda t: not(is_operator(t) or is_brace(t))


def compare(op1, op2):
    if PRECEDENCE[op1] == PRECEDENCE[op2]:
        return 0
    elif PRECEDENCE[op1] > PRECEDENCE[op2]:
        return 1
    return -1


def to_polish_notation(query):
    query = query.rstrip('\n').replace('(', ' ( ').replace(')', ' ) ')
    tokens = filter(lambda x: x is not '', [t for t in query.split(' ')][::-1])

    output = []
    stack = []
    for token in tokens:
        if is_operand(token):
            output.append(token)
        elif is_operator(token):
            while (len(stack) and not is_brace(stack[-1])):
                if compare(token, stack[-1]) <= 0:
                    output.append(stack.pop())
                else:
                    break
            stack.append(token)
        elif token == '(':
            while (len(stack) and stack[-1] != ')'):
                output.append(stack.pop())
            stack.pop()
        elif token == ')':
            stack.append(token)

    while(len(stack)):
        output.append(stack.pop())

    return output[::-1]


def process_query(polish_list):
    stack = []
    if(len(polish_list)) == 1:
        return Query(tuple(polish_list))

    while(len(polish_list) != 1 or len(stack)):
        token = polish_list.pop()
        if is_operand(token):
            stack.append(token)
        else:
            if token == 'NOT':
                q = Query((token, stack.pop()))
            else:
                q = Query((token, stack.pop(), stack.pop()))
            polish_list.append(q)
    return polish_list[0]

