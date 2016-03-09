import sys

# initialize NFA
state_counter = 0
alphabet = []
start_state = 0
final_states = []
transition = []

# regex = raw_input()
regex = '(a+b)*abb'
regex += '$'
current = 0
state_counter = 0

alphabet = list(set([char for char in regex if char not in ['*', '+', '(', ')', '$']]))
alphabet.append(':e:')    # Epsilon


# E -> T + E | T
# T -> F.T | F
# F -> F'* | F'
# F'-> (E) | id

def new_state():
    global state_counter
    state_counter += 1
    # Each row in transition table is a list of lists
    transition.append([[] for x in xrange(len(alphabet))])
    return state_counter-1

def match(string):
    if string == 'id':
        if regex[current] in ['*', '+', '(', ')', '$']:
            print(regex[current])
        return regex[current] not in ['*', '+', '(', ')', '$']
    else:
        # if regex[current] == string:
        #     print(regex[current])
        return regex[current] == string


def advance():
    global current
    current += 1
    if current >= len(regex):
        sys.exit('Termination error: Not a regular expression.')

def factor_prime():
    global state_counter
    if match('('):
        advance()
        start_state, end_state = expression()
        if match(')'):
            advance()
            return start_state, end_state
        else:
            print('Error: no matching ) in factor')
    if match('id'):
        identifier = regex[current]
        identifier_index = alphabet.index(identifier)
        advance()

        state_before_id = new_state()
        state_after_id = new_state()
        transition[state_before_id][identifier_index].append(state_after_id)
        return (state_before_id, state_after_id)

def factor():
    start_state, end_state = factor_prime()
    if match('*'):
        transition[start_state][-1].append(end_state)
        transition[end_state][-1].append(start_state)
        advance()
    return start_state, end_state


def term():
    start_state, end_state = factor()
    while not match('+') and not match(')') and not match('$'):
        prev_end_state = end_state
        _, end_state = factor()
        transition[prev_end_state][-1].append(_)
    return start_state, end_state

def expression():
    start_end_states = []
    start_end_states.append(term())
    if not match('+'):
        return start_end_states[0][0], start_end_states[0][1]

    while match('+'):
        advance()
        start_end_states.append(term())

    state_before_concat = new_state()
    state_after_concat = new_state()
    for se in start_end_states:
        transition[state_before_concat][-1].append(se[0])
        transition[se[1]][-1].append(state_after_concat)
    return state_before_concat, state_after_concat

start_state, end_state = expression()
final_states.append(end_state)

# display transition table
# for i, t in enumerate(transition):
#     print(str(i) + ' ' + str(t))

# import pdb; pdb.set_trace()

transitions = {}

for i, row in enumerate(transition):
    transitions[i] = {}
    for j, column in enumerate(row):
        for state in column:
            if not state in transitions[i]:
                transitions[i][state] = []
            transitions[i][state].append(alphabet[j])

print('')
for k, v in transitions.iteritems():
    print(str(k) + ' '),
    for l, u in v.iteritems():
        print(str(l) + ':'),
        for i in u:
            print(str(i) + '  '),
    print('')
