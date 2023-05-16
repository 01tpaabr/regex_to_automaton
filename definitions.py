#For debug
from treelib import Tree

from automata.fa.nfa import NFA

class state():
    final : bool = False
    transitions : dict = {}
    
    name_counter : int = 0
    name : str = ""

    #for final states
    tokenType : str = ""

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
    
    def __repr__(self) -> str:
        return "Automaton (" + str(self.initialState) +  ")"

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
    

    def findPathAux(self, origin, target, lastSymbol, calledStates, startLoop):
        calledStates.append(origin)
        noLastSymbol = False
        pathWord = ""

        #Other loop
        for i in origin.transitions:
            if origin.transitions[i].target == startLoop or origin.transitions[i].target == origin:
                noLastSymbol = True

        #State Found
        if origin == target:
            return lastSymbol
        
        for t in origin.transitions:
            #Does not take empty transitions, cycles, we just want the path 
            if t != "empty" and origin.transitions[t].target not in calledStates: 
                nextWord = self.findPathAux(origin.transitions[t].target, target, t, calledStates, startLoop)

                if nextWord != "":
                    if not noLastSymbol: pathWord += lastSymbol + nextWord
                    else: pathWord += nextWord
                    break
                
        return pathWord
    
    #Find which transitions should take to go to one state to another
    def findPath(self, origin, target, startLoop):
        return self.findPathAux(origin, target, "", [], startLoop)

    def findFakePathAux(self, origin, target, lastSymbol, calledStates):
        calledStates.append(origin)
        pathWord = ""

        #State Found
        if origin == target:
            return lastSymbol
        
        for t in origin.transitions:
            #Does not take empty transitions, cycles, we just want the path 
            if t != "empty" and origin.transitions[t].target not in calledStates: 
                nextWord = self.findFakePathAux(origin.transitions[t].target, target, t, calledStates)

                if nextWord != "":
                    pathWord += lastSymbol + nextWord
                    break
                
        return pathWord
    
    def findFakePath(self, origin, target):
        return self.findFakePathAux(origin, target, "", [])

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

        nextDepths.sort(reverse=True)

        if len(nextDepths) > 0: depth += nextDepths[0]

        return depth
    
    #Find cycles in 'path' automatons using help of "empty" back transitions
    def findPathCycles(self):
        currState = self.initialState
        cyclesList = []

        chosenTransition = False

        for i in currState.transitions:
            if i != "empty":
                chosenTransition = currState.transitions[i]

        finished = False

        while chosenTransition:
            if "empty" in currState.transitions:
                cyclesList.append([currState.transitions["empty"].target, currState])
                # finished = True
            
            chosenTransition = False

            for i in currState.transitions:
                if i != "empty":
                    chosenTransition = currState.transitions[i]
            
                if chosenTransition: currState = chosenTransition.target
        
        return cyclesList

        
    
    #Function just work before application of 'removeEmpty' function
    def findLastStates(self, currState, finalStatesList):
        hasNextTransition = False

        for t in currState.transitions:
            if t != "empty":
                hasNextTransition = True
                self.findLastStates(currState.transitions[t].target, finalStatesList)
        

        if not hasNextTransition:
            finalStatesList.append(currState)
        
        return finalStatesList          

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

    def finalStates(self):
        finalStates = []
        for i in self.states:
            if i.final: finalStates.append(i)
        return finalStates
        
class regexTree():
    value = None
    children : list = None

    #just for print
    diferentiator = 1

    def __repr__(self) -> str:
        return "Node (" + str(self.value) +  ")"

    def __init__(self, children, value) -> None:
        self.children = children
        self.value = value
    
    def buildTree(self, tree, currNode, calledNodes):
        calledNodes.append(currNode)
        
        for n in currNode.children:
            nextNode = n
            if nextNode.value != []:
                if nextNode not in calledNodes:
                    if nextNode.value == "|": 
                        nextNode.value += str(regexTree.diferentiator)
                        regexTree.diferentiator += 1

                    if nextNode.value == "*": 
                        nextNode.value += str(regexTree.diferentiator)
                        regexTree.diferentiator += 1

                    tree.create_node(str(nextNode.value), str(nextNode.value), parent=str(currNode.value))
                    self.buildTree(tree, nextNode, calledNodes)


    def treePrint(self):
        #Build in treelib structure
        tree = Tree()

        tree.create_node(str(self.value), str(self.value))

        self.buildTree(tree, self, [])

        tree.show()


def convertSymbol(regex, symbolIndex):
    convertedSymbol = regex[symbolIndex]
    return convertedSymbol