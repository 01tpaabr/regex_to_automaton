class state():
    final : bool = False
    transitions : dict = {}
    
    name_counter : int = 0
    name : str = ""

    def __init__(self, final, transitions) -> None:
        self.final = final
        self.transitions = transitions
        self.name = "q" + str(state.name_counter)
        state.name_counter += 1
    
    def has_transition(self, symbol) -> bool:
        return symbol in self.transitions.keys()
    
    #Go one level deeper in path depth
    def goLower(self):
        nextStates = []

        for i in self.transitions:
            #Bad way of verifying if its not a back transition, only works if automaton construction only assigns empty to these transitions
            if i != "empty": nextStates.append(self.transitions[i].target)
        
        return nextStates
    
    def nextSymbols(self):
        symbols = []

        for t in self.transitions:
            symbols.append(t)
        
        return symbols
    
    def show_transitions(self) -> str:
        string = ""

        for i in self.transitions.keys():
            string += str(self.transitions[i]) + "\n"
        
        return string 

    def __str__(self) -> str:
        return "State " + self.name + ", is_final=" + str(self.final)
    
    def __repr__(self) -> str:
        return "State " + self.name + ", is_final=" + str(self.final)
    

class transition():
    target : state = None
    symbol : str = ""

    def __init__(self, target, symbol) -> None:
        self.target = target
        self.symbol = symbol

    def __str__(self) -> str:
        return "Transition (" + str(self.target.name) + " , "+ str(self.symbol) +  " )"
    
    def __repr__(self) -> str:
        return "Transition (" + str(self.target.name) + " , "+ str(self.symbol) +  " )"

class automaton():
    initialState : state = None
    states : list = []
    transitionsList : list = []

    #For other acesses
    statesDict : dict = {}

    def __init__(self, initialState, states, statesDict, transitionsList) -> None:
        self.initialState = initialState
        self.states = states
        self.statesDict = statesDict
        self.transitionsList = transitionsList

    def __str__(self) -> str:
        string = "Start state: " + str(self.initialState.name) + "\n"
        for i in self.states:
            currStateString = "State: " + i.__str__() + "\n"
            for j in i.transitions:
                currStateString += str(i.transitions[j]) + " \n"
            
            string += currStateString + "\n"
        
        return string
    
    def incomingTransitions(self, stateName):
        transitions = []

        for i in self.transitionsList:
            if i.target.name == stateName:
                transitions.append(i)


        return transitions
    

    def depth(self):
        return self.depthAux(self.initialState, [])
    
    def depthAux(self, currentState, calledStates):
        depth = 1

        nextDepths = []
        calledStates.append(currentState)

        for i in currentState.transitions:
            nextState = currentState.transitions[i].target

            if nextState not in calledStates:
                nextDepths.append(self.depthAux(nextState, calledStates))
            
            nextDepths.sort()

        if len(nextDepths) > 0: depth += nextDepths[0]

        return depth


def convertSymbol(regex, symbolIndex):
    convertedSymbol = regex[symbolIndex]
    return convertedSymbol