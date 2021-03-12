import graphviz
import os


def nfa_determinization(nfa: dict) -> dict:
    dfa = {
        'alphabet': nfa['alphabet'].copy(),
        'initial_state': None,
        'states': set(),
        'accepting_states': set(),
        'transitions': dict()
    }

    if len(nfa['initial_states']) > 0:
        dfa['initial_state'] = str(nfa['initial_states'])
        dfa['states'].add(str(nfa['initial_states']))

    sets_states = list()
    sets_queue = list()
    sets_queue.append(nfa['initial_states'])
    sets_states.append(nfa['initial_states'])
    if len(sets_states[0].intersection(nfa['accepting_states'])) > 0:
        dfa['accepting_states'].add(str(sets_states[0]))

    while sets_queue:
        current_set = sets_queue.pop(0)
        for a in dfa['alphabet']:
            next_set = set()
            for state in current_set:
                if (state, a) in nfa['transitions']:
                    for next_state in nfa['transitions'][state, a]:
                        next_set.add(next_state)
            if len(next_set) == 0:
                continue
            if next_set not in sets_states:
                sets_states.append(next_set)
                sets_queue.append(next_set)
                dfa['states'].add(str(next_set))
                if next_set.intersection(nfa['accepting_states']):
                    dfa['accepting_states'].add(str(next_set))

            dfa['transitions'][str(current_set), a] = str(next_set)

    return dfa


def dfa_to_dot(dfa: dict, name: str, path: str = './'):

    g = graphviz.Digraph(format='svg')
    g.node('fake', style='invisible')
    for state in dfa['states']:
        if state == dfa['initial_state']:
            if state in dfa['accepting_states']:
                g.node(str(state), root='true',
                       shape='doublecircle')
            else:
                g.node(str(state), root='true')
        elif state in dfa['accepting_states']:
            g.node(str(state), shape='doublecircle')
        else:
            g.node(str(state))

    g.edge('fake', str(dfa['initial_state']), style='bold')
    for transition in dfa['transitions']:
        g.edge(str(transition[0]),
               str(dfa['transitions'][transition]),
               label=transition[1])

    if not os.path.exists(path):
        os.makedirs(path)

    g.render(filename=os.path.join(path, name + '.dot'))


nfa = {
  "alphabet": {
    "a",
    "b",
  },
  "states": {
    "q0",
    "q1",
    "q2",
    "q3",
  },
  "initial_states": {
    "q0"
  },
  "accepting_states": {
    "q3"
  },
  "transitions": {
    ("q0", "a"): {"q0"},
    ("q0", "a"): {"q1"},
    ("q1", "b"): {"q1"},
    ("q2", "b"): {"q3"},
    ("q1", "a"): {"q2"},
    ("q2", "a"): {"q0"},
    }
}

dfa = nfa_determinization(nfa)
dfa_to_dot(dfa, "dot")


"""
AF=(Q, , , q0, F),
Q = { q0, q1, q2, q3 },
 = { a, b, c}, F = { q3 }.
 (q0, a ) = q0 ,
 (q0, a ) = q1 ,
 (q1, b ) = q1 ,
 (q2, b ) = q3,
 (q1, a ) = q2,
 (q2, a ) = q0.
"""

