#For debug
from treelib import Tree

from automata.fa.nfa import NFA

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
    
    def hasTransition(self, symbol) -> bool:
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
    origin : state = None

    def __init__(self, target, symbol, origin) -> None:
        self.target = target
        self.symbol = symbol
        self.origin = origin

    def __str__(self) -> str:
        return "Transition (" + str(self.origin.name) + ", "+ str(self.symbol) +  ", " + str(self.target.name) + " )"
    
    def __repr__(self) -> str:
        return "Transition (" + str(self.origin.name) + ", "+ str(self.symbol) +  ", " + str(self.target.name) + " )"

class automaton():
    initialState : state = None
    states : list = []
    
    #For other acesses
    statesDict : dict = {}
    transitionsList : list = []

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
    
    #Return list of all transitions
    def symbolTransitions(self, symbol):
        return list(filter(lambda t: t.symbol == symbol, self.transitionsList))
    

    def findPathAux(self, origin, target, lastSymbol, calledStates):
        calledStates.append(origin)
        #State Found
        if origin == target:
            return lastSymbol
        
        pathWord = ""
        for t in origin.transitions:
            #Does not take empty transitions, cycles, we just want the path 
            if t != "empty" and origin.transitions[t].target not in calledStates: 
                nextWord = self.findPathAux(origin.transitions[t].target, target, t, calledStates)

                if nextWord != "":
                    pathWord += lastSymbol + nextWord
                    break
                

        return pathWord
    
    #Find which transitions should take to go to one state to another
    def findPath(self, origin, target):
        return self.findPathAux(origin, target, "", [])

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
    
    #Aux function
    def buildTree(self, tree, currentState, calledStates):
        calledStates.append(currentState)

        for t in currentState.transitions:
            nextState = currentState.transitions[t].target

            if nextState not in calledStates:
                tree.create_node(nextState.name, nextState.name, parent=currentState.name)
                self.buildTree(tree, nextState, calledStates)

    
    def treePrintAutomaton(self): #Does not show cycles
        #Build in treelib structure
        tree = Tree()
        tree.create_node(self.initialState.name, self.initialState.name)

        self.buildTree(tree, self.initialState, [])

        tree.show()

    def buildVisualAutomaton(self, currentState, calledStates, nfa):
        calledStates.append(currentState)
        nfa[0].add(currentState.name)
        
        if currentState.final: nfa[1].add(currentState.name)

        nfa[2][currentState.name] = {}

        for t in currentState.transitions:
            nextState = currentState.transitions[t].target
            nfa[2][currentState.name][currentState.transitions[t].symbol] = {currentState.transitions[t].target.name}

            if nextState not in calledStates:
                self.buildVisualAutomaton(nextState, calledStates, nfa)
        
        
    
    def showVisualDFA(self, path): #only DFA
        results = [set(), set(), dict(), set()]

        for t in self.transitionsList:
            results[3].add(t.symbol)
        
        self.buildVisualAutomaton(self.initialState, [], results)
        
        nfa = NFA(states=results[0], input_symbols=results[3], transitions=results[2], initial_state=self.initialState.name, final_states=results[1])
        nfa.show_diagram(path)
        


def convertSymbol(regex, symbolIndex):
    convertedSymbol = regex[symbolIndex]
    return convertedSymbol