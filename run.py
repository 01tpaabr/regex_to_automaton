import automaton_generation

#If input is valid, will return token list
def run(tokenAutomatons, priorityList, tokenTypes, input):
    notErrors = [" ", "\n"]

    #["token", "type", "line"]
    tokenList = []

    inputPositions = []
    accepting_automatons = []
    possibleTokens = []
    breakCharList = []
    finishedList = []
    lineCountDict = {}

    lineCount = 1

    for i in tokenAutomatons:
        inputPositions.append(i.initialState)
        possibleTokens.append("")
        breakCharList.append("")
        finishedList.append(False)

    i = 0
    while i < len(input):
        #When all runs has finished we will have a inputPositions list of the form [False, False, False, ...]
        while False in finishedList:
            currChar = input[i]
            if currChar == "\n": lineCount += 1
            
            #One iteration for all automatons
            j = 0
            while j < len(inputPositions):
                
                currState = inputPositions[j]
                if currState:
                    if currChar not in currState.transitions:
                        inputPositions[j] = False
                        finishedList[j] = True

                        if currState.final:
                            
                            accepting_automatons.append(tokenTypes[j])
                            if currChar ==  "\n": lineCountDict[tokenTypes[j]] = lineCount - 1
                            else: lineCountDict[tokenTypes[j]] = lineCount
                        
                        breakCharList[j] = currChar
                    else:
                        possibleTokens[j] += currChar
                        inputPositions[j] = currState.transitions[currChar].target

                j += 1

            #Get next char
            if i + 1 <= len(input): i += 1
            else: break
        
        #In the end of this while Loop, we will have an populated list of accepting_automatons
        #Decide tokenType
        if len(accepting_automatons) > 0:
            if input[i - 1] not in notErrors:
                i += - 1 #Go back if last char is not space
            tokenType = ""
            for token in accepting_automatons:
                if token in priorityList:
                    tokenType = token
                    break

                tokenType = token
            
            tokenList.append([tokenType, possibleTokens[tokenTypes.index(tokenType)], lineCountDict[tokenType]])
        else:
            #No automaton accepted this word
            error = False
            #If any automaton has last char different from " " or "\n" then they read something invalid
            brokenChar = ""

            for char in breakCharList:
                if char not in notErrors:
                    error = True
                    brokenChar = char
                    break

            if error:
                print("Token invalido: `" + str(brokenChar) + "` linha:" + str(lineCount))
                return False
        
        #Reset automatons and aux structures
        for a in range(len(tokenAutomatons)):
            inputPositions[a] = tokenAutomatons[a].initialState
            possibleTokens[a] = ""
            breakCharList[a] = ""
            finishedList[a] = False
                
        accepting_automatons = []
        lineCountDict = {}
    
    return tokenList