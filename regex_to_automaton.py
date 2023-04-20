import random
import string

# ()
# *
# +
# .
# \symbol
# ||


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
    
    def show_transitions(self) -> str:
        string = ""

        for i in self.transitions.keys():
            string += str(self.transitions[i]) + "\n"
        
        return string 

    def __str__(self) -> str:
        return "State " + self.name
    
    def __repr__(self) -> str:
        return "State " + self.name
    

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
    states : list = []

    #For other acesses
    statesDict : dict = {}

    def __str__(self) -> str:
        string = ""
        for i in self.states:
            currStateString = "State: " + i.name + "\n"
            for j in i.transitions:
                currStateString += str(i.transitions[j]) + " \n"
            
            string += currStateString + "\n"
        
        return string


def convertSymbol(regex, symbolIndex):
    convertedSymbol = regex[symbolIndex]
    return convertedSymbol

def transform(regex : str) -> automaton:
    operators = ["(", ")", "*", "|"]

    a = automaton()

    initState = state(False, {})
    a.states.append(initState)
    a.statesDict[initState.name] = initState
    
    lastState = initState
    
    i = 0
    while i < len(regex):
        realSymbol = regex[i]
        symbol = convertSymbol(regex, i)

        openGroup = False
        
        if realSymbol == "(":
            openGroup = True

            #Get starting group symbol
            if i < len(regex) - 1:
                i += 1
                realSymbol = regex[i]
                symbol = convertSymbol(regex, i)

        #Handle Group Closure
        if realSymbol == ")":
            #Not last
            if i < len(regex) - 1:
                if regex[i + 1] == "*":
                    startGroupState.final = True

                #Add transition to go back to starting group state
                backTransition = transition(startGroupState, "any")
                lastState.transitions["any"] = backTransition
                
                #Reset groupState variable
                startGroupState = None
                
                #Exists other symbols
                if i < len(regex) - 2:
                    # ) ocorrence + repetitor ocorrence = +2 for next symbol
                    i += 2

        if realSymbol not in operators:
            newState = state(False, {})
            
            newTransition = transition(newState, symbol)
            lastState.transitions[symbol] = newTransition

            #Handle '('
            if openGroup:
                startGroupState = newState
                openGroup = False

            a.states.append(newState)
            a.statesDict[newState.name] = newState

            lastState = newState
        
        i += 1

    return a

test = "a(abc)*"

res = transform(test)
print(res)        
        