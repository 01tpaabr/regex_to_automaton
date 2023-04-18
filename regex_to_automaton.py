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
    
    #just for print
    id : str = ""

    def __init__(self, final, transitions) -> None:
        self.final = final
        self.transitions = transitions
        self.id = ''.join(random.choices(string.ascii_lowercase, k=5))
    
    def has_transition(self, symbol):
        return symbol in self.transitions.keys()

    def __str__(self) -> str:
        return "State [ " + str(self.final) + " : { "+ str(self.transitions) + " } ]"
    
    def __repr__(self) -> str:
        return "State [ " + str(self.id) + " : { "+ str(self.final) + " } ]"
    

class transition():
    target : state = None
    symbol : str = ""

    def __init__(self, target, symbol) -> None:
        self.target = target
        self.symbol = symbol

    def __str__(self) -> str:
        return "Transition (" + str(self.target.id) + " , "+ str(self.symbol) +  " )"
    
    def __repr__(self) -> str:
        return "Transition (" + str(self.target.id) + " , "+ str(self.symbol) +  " )"

class automaton():
    states : list = []

    #For other acesses
    statesDict : dict = {}

def convertSymbol(regex, symbolIndex):
    convertedSymbol = regex[symbolIndex]
    return convertedSymbol

def transform(regex : str) -> automaton:
    operators = ["(", ")", "*", "+"]
    repetitors = ["*", "+"]

    a = automaton()

    initState = state(False, {})
    a.states.append(initState)
    a.statesDict[initState.id] = initState
    
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
                if regex[i + 1] in repetitors:
                    # * Accept no ocorrences
                    if regex[i + 1] == "*":
                        startGroupState.final = True

                    #Add transition to go back to starting group state
                    backTransition = transition(startGroupState, "")
                    lastState.transitions[""] = backTransition
                    
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
            a.statesDict[newState.id] = newState

            lastState = newState
        
        i += 1

    return a

test = "a(abc)*"

res = transform(test)
print(res.states)        
        