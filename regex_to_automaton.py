import random
import string

# (
# )
# *
# .
# \symbol
# |


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
    states : list = []

    #For other acesses
    statesDict : dict = {}

    def __str__(self) -> str:
        string = ""
        for i in self.states:
            currStateString = "State: " + i.__str__() + "\n"
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

test = "a(ad(ab)bc)*5"

res = transform(test)
print(res)        
        