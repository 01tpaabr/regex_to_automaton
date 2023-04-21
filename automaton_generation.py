import definitions

automaton = definitions.automaton
state = definitions.state
transition = definitions.transition
convertSymbol = definitions.convertSymbol

# (
# )
# *
# .
# \symbol
# |



#Given automaton list, unify in one
def unionProcess(automatons : list) -> automaton:
    #these automatons have only one direction, with back transitions, and "states" in these automatons will be following these directions
    #So we can handle the union process  in this way
    union = automaton(None, [], {})

    #For example if 3 paths(automatons) are given, in each iteration of the for loop "oldStates" will have a reference to 3 states, one from each path
    
    currentOldStates = [None for i in range(len(automatons))]
    currentNewStates = [None for i in range(len(automatons))]

    #newStates will have 3 positions, representing the union of the 3 states in "oldStates"
    #An state can be replicated in more than one position in 'newStates', representing it refers to more than one old state, needing to handle the transitions accordingly

    automatons = sorted(automatons, key = lambda a: len(a.states, reverse=True))
    biggerPath =automatons[0]
    pathsList = list(map(lambda a: a.states, automatons))

    #Run till bigger path is processed
    for i in range(len(biggerPath.states)):
        currentOldStates = list(map(lambda l: l[i], pathsList))
        isFinal = list(map(lambda s: s.final, currentOldStates))
        oldTransitions = list(map(lambda s: s.transitions, currentOldStates))
        oldTransitionsSymbols = list(map(lambda t: t.keys(), oldTransitions))

        

        

    return union

#No | operator in this regex
def path(regex : str) -> automaton:
    operators = ["(", ")", "*", "|"]

    a = automaton(None, [], {})

    initState = state(False, {})
    a.initialState = initState
    a.states.append(initState)
    a.statesDict[initState.name] = initState
    
    lastState = initState

    #Starting groups states, defined by '(' ocorrence
    groupStateStack = []
    
    #Notifies number of '(' operations to be handled (i.e add state to 'groupStateStack' line 136) 
    openGroup = 0
    
    i = 0
    while i < len(regex):
        realSymbol = regex[i]
        symbol = convertSymbol(regex, i)
        
        if realSymbol == "(":
            openGroup += 1


        #Handle Group Closure
        if realSymbol == ")":
            startGroupState = groupStateStack.pop()
            #Not last
            if i < len(regex) - 1:
                if regex[i + 1] == "*":
                    startGroupState.final = True

                    #Add transition to go back to starting group state
                    backTransition = transition(startGroupState, "empty")
                    lastState.transitions["empty"] = backTransition

                    if i + 1 == len(regex) - 1:
                        lastState.final = True

                #"empty" symbol needs to be interpreted in run as using this transition only if there is no other, then it doesn't read any symbol
                
                #Exists other symbols
                if i < len(regex) - 2:
                    # +1 for '*', that we have already handled
                    i += 1

        if realSymbol not in operators:
            #If there is no more characters left, this is an final state
            newState = state(not (i + 1 < len(regex)), {})
            
            newTransition = transition(newState, symbol)
            lastState.transitions[symbol] = newTransition

            #Handle '('
            while openGroup:
                groupStateStack.append(lastState)
                openGroup += -1

            #Add to automaton list of states
            a.states.append(newState)
            a.statesDict[newState.name] = newState

            lastState = newState
        
        i += 1

    return a

test = "a(ad(ab)bc)*"
test2 = "ab((bc)*aa)*ad"
test3 = "abd(acc)*(a)*"

a1 = path(test)
a2 = path(test2)
a3 = path(test3)

print(a1)
print("########################################")
print(a2)
print("########################################")
print(a3)  
        