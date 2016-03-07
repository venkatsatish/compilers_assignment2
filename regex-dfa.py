regex = raw_input()
current = 0

# E -> T + E | T
# T -> F.T | F
# F -> (E) | F* | id


def match(string):
    if string == 'id':
        if regex[current] not in ['*', '+', '(', ')']:
            print(regex[current])
        return regex[current] not in ['*', '+', '(', ')']
    else:
        if regex[current] == string:
            print(regex[current])
        return regex[current] == string

def advance():
    global current
    current += 1
    if current >= len(regex):
        exit(0)

def factor_prime():
    if match('('):
        advance()
        expression()
        if match(')'):
            advance()
            return
        else:
            print('Error: no matching ) in factor')
    if match('id'):
        advance()

def factor():
    factor_prime()
    if match('*'):
        advance()

def term():
    while not match('+') and not match(')'):
        factor()

def expression():
    term()
    if match('+'):
        advance()
        expression()


# import pdb; pdb.set_trace()
expression()
