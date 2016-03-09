import time
import sys

class NFAfromRegex:
    """class for building e-nfa from regular expressions"""

    def __init__(self, regex):
        # initialize NFA
        self.state_counter = 0
        self.alphabet = []
        self.start_state = 0
        self.final_states = []
        self.transition = []

        self.regex = regex + '$'
        self.current = 0
        self.state_counter = 0

        self.alphabet = list(set([char for char in regex if char not in ['*', '+', '(', ')', '$']]))
        self.alphabet.append(':e:')    # Epsilon

        self.nfa_from_regex()
        self.states = set(range(self.state_counter))
        self.alphabet = set(self.alphabet)
        self.final_states = set(self.final_states)

    # E -> T + E | T
    # T -> F.T | F
    # F -> F'* | F'
    # F'-> (E) | id

    def new_state(self):
        self.state_counter += 1
        # Each row in transition table is a list of lists
        self.transition.append([[] for x in xrange(len(self.alphabet))])
        return self.state_counter-1

    def match(self, string):
        if string == 'id':
            if self.regex[self.current] in ['*', '+', '(', ')', '$']:
                print(self.regex[self.current])
            return self.regex[self.current] not in ['*', '+', '(', ')', '$']
        else:
            # if regex[self.current] == string:
            #     print(regex[self.current])
            return self.regex[self.current] == string


    def advance(self):
        self.current += 1
        if self.current >= len(self.regex):
            sys.exit('Termination error: Not a regular expression.')

    def factor_prime(self):
        if self.match('('):
            self.advance()
            start_state, end_state = self.expression()
            if self.match(')'):
                self.advance()
                return start_state, end_state
            else:
                print('Error: no self.matching ) in factor')
        if self.match('id'):
            identifier = self.regex[self.current]
            identifier_index = self.alphabet.index(identifier)
            self.advance()

            state_before_id = self.new_state()
            state_after_id = self.new_state()
            self.transition[state_before_id][identifier_index].append(state_after_id)
            return state_before_id, state_after_id

    def factor(self):
        start_state, end_state = self.factor_prime()
        if self.match('*'):
            state_before_prime, state_after_prime = start_state, end_state
            start_state = self.new_state()
            end_state = self.new_state()
            self.transition[start_state][-1].append(state_before_prime)
            self.transition[state_after_prime][-1].append(end_state)
            self.transition[start_state][-1].append(end_state)
            self.transition[state_after_prime][-1].append(state_before_prime)
            self.advance()
        return start_state, end_state


    def term(self):
        start_state, end_state = self.factor()
        while not self.match('+') and not self.match(')') and not self.match('$'):
            prev_end_state = end_state
            _, end_state = self.factor()
            self.transition[prev_end_state][-1].append(_)
        return start_state, end_state

    def expression(self):
        start_end_states = []
        start_end_states.append(self.term())
        if not self.match('+'):
            return start_end_states[0][0], start_end_states[0][1]

        while self.match('+'):
            self.advance()
            start_end_states.append(self.term())

        state_before_concat = self.new_state()
        state_after_concat = self.new_state()
        for se in start_end_states:
            self.transition[state_before_concat][-1].append(se[0])
            self.transition[se[1]][-1].append(state_after_concat)
        return state_before_concat, state_after_concat

    def nfa_from_regex(self):
        start_state, end_state = self.expression()
        self.final_states.append(end_state)

        transitions = {}
        for i, row in enumerate(self.transition):
            transitions[i] = {}
            for j, column in enumerate(row):
                for state in column:
                    if not state in transitions[i]:
                        transitions[i][state] = []
                    transitions[i][state].append(self.alphabet[j])
            if not transitions[i]:
                transitions.pop(i, None)

        # print('')
        # # for k, v in transitions.iteritems():
        # #     print(str(k) + ' '),
        # #     for l, u in v.iteritems():
        # #         print(str(l) + ':'),
        # #         for i in u:
        # #             print(str(i) + '  '),
        # #     print('')
        self.start_state = start_state
        self.transition = transitions
        self.alphabet.pop()


def main():
    inp = "(a+b)*abb"
    print "Regular Expression: ", inp
    nfa = NFAfromRegex(inp)
    print "\n Minimized DFA"
    DFAtable, DFAstates, DFAstartstate, DFAfinalstates, DFAterminals = DFAfromNFA(nfa.states, nfa.transition, nfa.start_state, nfa.final_states, nfa.alphabet)

    for i in DFAtable:
        print str(i) + '->' + str(DFAtable[i])
    # print "finalstates= " + str(DFAfinalstates)
    DFAminimize(DFAtable,DFAstates,DFAterminals,DFAstartstate,DFAfinalstates)


def epsilonclosure(states,transitions):
    U = set()
    M = set()
    for i in states:
        M.add(i)
        U.add(i)
    # import pdb; pdb.set_trace()
    while len(M)!=0:
        i = M.pop()
        if i in transitions:
            for j in transitions[i]:
                if ':e:' in transitions[i][j]:
                    M.add(j)
                    U.add(j)
    # print "epsilonclosure(" + str(states) + ')=' + str(U)
    return U

def DFAfromNFA(states,transitions,startstate,finalstates,terminals):
    unmarkedstates = []
    markedstates = set()
    U = set()
    S= set()
    q=0
    DFAstates = dict()
    DFAtable = dict()
    DFAfinalstates= set()
    # unmarkedstates.append(startstate)
    state = [startstate]
    DFAstates[q] = epsilonclosure(state,transitions)
    DFAstartstate = 0
    unmarkedstates.append(0)
    q += 1
    # print(DFAstates)
    while len(unmarkedstates)!=0:
        T = unmarkedstates.pop()
        markedstates.add(T)
        for t in terminals:
            for i in DFAstates[T]:
                if i in transitions:
                    for j in transitions[i]:
                        if t in transitions[i][j]:
                            # print j
                            S.add(j)

            # print "move(" + str(T) + "," + t + ")=" + str(S)
            U=epsilonclosure(S,transitions)
            k=0
            for i in DFAstates:
                if U == DFAstates[i]:
                    if T in DFAtable:
                        DFAtable[T][i] = t
                    else:
                        DFAtable[T] = {i : t}
                    k = 1
                    break
            if k == 0:
                DFAstates[q] = U
                unmarkedstates.append(q)
                if T in DFAtable:
                    DFAtable[T][q] = t
                else:
                    DFAtable[T] = {q:t}
                for i in U:
                    if i in finalstates:
                        DFAfinalstates.add(q)
                q += 1
            S = set()
    return DFAtable,markedstates,DFAstartstate,DFAfinalstates,terminals

def DFAminimize(transitions,states,terminals,startstate,finalstates):
    F = set()
    S = set()
    F = finalstates
    S = set()
    # S = set([F],[states-finalstates])
    # while
    return 0


if __name__  ==  '__main__':
    t = time.time()
    try:
        main()
    except BaseException as e:
        print "\nFailure:", e
    print "\nExecution time: ", time.time() - t, "seconds"        