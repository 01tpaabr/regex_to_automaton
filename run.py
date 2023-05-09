import automaton_generation

#If input is valid, will return token list
def run(automaton, input):
    i = 0

    currState = automaton.initialState
    tokenList = []

    while i < len(input):
        currChar = input[i]

        if currChar in currState.transitions:
            currState = currState.transitions[currChar].target
            currToken += currChar
        else:
            #If there is no transitions, token ended
            isValid = currState.final

            if not isValid: return False

            tokenList.append([currState.tokenType, currToken])
            #Reset token
            currToken = ""

        i += 1
