import definitions
import copy

automaton = definitions.automaton
state = definitions.state
transition = definitions.transition
convertSymbol = definitions.convertSymbol
regexTree = definitions.regexTree

# (
# )
# *
# .
# \symbol
# |

global count
count = 0

#Remove last step of non determinism, empty back transitions
def removeEmpty(automaton) -> automaton:
    emptyTransitions = automaton.symbolTransitions("empty")

    #Group transitions by target
    transitionsGroups = {}

    #For group operation
    firstWord = {}

    for t in emptyTransitions:
        if t.target.name not in transitionsGroups:
            transitionsGroups[t.target.name] = [t]

        if t not in transitionsGroups[t.target.name] : 
            transitionsGroups[t.target.name].append(t)    
    
    for t in emptyTransitions:
        automaton.transitionsList.remove(t)
        currentGroup = transitionsGroups[t.target.name]

        loopStart = t.target
        loopFinish = t.origin

        del(loopFinish.transitions["empty"])

        #Find out which word is built in
        loopWord = automaton.findPath(loopStart, loopFinish, loopStart)
        iterationWord = automaton.findFakePath(loopStart, loopFinish) #Path including symbols from other loops
    
        symbolCount = 0

        #If possible, the back transition would need to have the same symbol as the start of the loop
        transitionSymbol = loopWord[symbolCount]
        
        #Just first symbol from fakePath
        if loopWord != iterationWord : loopStart = loopStart.transitions[iterationWord[0]].target
        
        loopStart = loopStart.transitions[transitionSymbol].target

        while loopFinish.hasTransition(transitionSymbol):
            #If this state has an transition with the symbol equal to transition symbol, we need to advance one state and try again
            loopFinish = loopFinish.transitions[transitionSymbol].target

            #Same for the transitionSymbol
            symbolCount += 1
            if symbolCount == len(loopWord): symbolCount = 0
            transitionSymbol = loopWord[symbolCount]

            #Loop start will advance aswell
            loopStart = loopStart.transitions[loopWord[symbolCount]].target

        newTransition = transition(loopStart, transitionSymbol, loopFinish)
        loopFinish.transitions[transitionSymbol] = newTransition
        firstWord[loopFinish] = transitionSymbol
        # loopFinish.final = True
        automaton.transitionsList.append(newTransition)
    
    #Handle * union from transitionGroups
    for i in transitionsGroups:
        for a in transitionsGroups[i]:
            aOrigin = a.origin
            for b in transitionsGroups[i]:
                if b != a:
                    bFinish = b.origin
                    bStart = b.target
                    
                    loopWord = automaton.findPath(bStart, bFinish, bStart)
                    iterationWord = automaton.findFakePath(bStart, bFinish)

                    symbolCount = 0

                    #If possible, the back transition would need to have the same symbol as the start of the loop
                    transitionSymbol = loopWord[symbolCount]
                    
                    #Just first symbol from fakePath
                    if loopWord != iterationWord : bStart  = bStart.transitions[iterationWord[0]].target
                    
                    bStart = bStart.transitions[transitionSymbol].target
                    
                    if transitionSymbol in aOrigin.transitions:
                        if aOrigin.transitions[transitionSymbol].target == bStart:
                            break

                    while aOrigin.hasTransition(transitionSymbol):
                        #If this state has an transition with the symbol equal to transition symbol, we need to advance one state and try again
                        aOrigin = aOrigin.transitions[transitionSymbol].target

                        #Same for the transitionSymbol
                        symbolCount += 1
                        if symbolCount == len(loopWord): symbolCount = 0
                        transitionSymbol = loopWord[symbolCount]

                        #Loop start will advance aswell
                        bStart = bStart.transitions[loopWord[symbolCount]].target
                    
                    newTransition = transition(bStart, transitionSymbol, aOrigin)
                    aOrigin.transitions[transitionSymbol] = newTransition
                    firstWord[loopFinish] = transitionSymbol
                    automaton.transitionsList.append(newTransition)

    return automaton

def minimizeUnion(union):
    initState = union.initialState

    for i in union.states:
        if i != initState:
            union.states.remove(i)
    
    newState = state(True, {})

    for t in union.transitionsList:
        if t.symbol == "empty":
            t.origin = newState
        else:
            t.target = newState

    
    union.states.append(newState)
    
    return union

#Aux function to find out which last state this transition needs to be handled in (just for union purposes)
def findLastState(lastStatesList, oldReferenceStateDict, originalState):
    lastStateName = ""

    for i in oldReferenceStateDict:
        if originalState in oldReferenceStateDict[i]: lastStateName = i
    
    for i in lastStatesList:
        if i.name == lastStateName: return i


#Given automaton list, unify in one
def unionProcess(automatons : list) -> automaton:
    #Variable representing how much of the 
    union = automaton(None, [], {}, [])

    automatons = sorted(automatons, key = lambda a: a.depth(), reverse=True)


    biggerPath = automatons[0]
    

    #Hold current states being handled by iteration
    pathsList = list(map(lambda a: a.initialState, automatons))
    
    initUnionState = state(False, {})
    union.states.append(initUnionState)
    union.initialState = initUnionState

    for i in pathsList:
        initUnionState.final = initUnionState.final or i.final

    createdStates = []
    createdTransitions = []
    currentTransitionsTargets = {}

    lastStates = []

    #Keep track of all references from createad states to old  (used to handle epsilon transitions)
    allReferences = {}
    
    #Run till bigger path is processed
    for i in range(biggerPath.depth()):
        #Refresh data structures to new iteration
        lastStates = createdStates

        createdStates = []
        createdTransitions

        currentSymbols = []
        currentTransitions = []

        #Keep track which states a symbol lead's to in old automaton's, can be more than one
        oldTransitionsTargets = currentTransitionsTargets
        currentTransitionsTargets = {}

        for p in pathsList: 
            aux = p.nextSymbols()
            aux.append(p.name)

            auxTransitions = []
            for t in p.transitions:
                auxTransitions.append(p.transitions[t])

            currentSymbols.append(aux)
            currentTransitions.append(auxTransitions)

        chosenSymbols = {}

        #Bad way of separating first and other iterations, improve later
        if i == 0:
            chosenSymbols["init"] = []
        else:
            for j in lastStates:
                chosenSymbols[j.name] = []

        for j in range(len(currentSymbols)):
            for s in range(len(currentSymbols[j])):

                originalStateNameForCurrentSymbol = currentSymbols[j][len(currentSymbols[j]) - 1]
                
                for k in pathsList:
                    if k.name == originalStateNameForCurrentSymbol: originalStateForCurrentSymbol = k
                

                #Last place holds state that originated the transitions (not an symbol to be iterated)
                if not s == len(currentSymbols[j]) - 1:
                    currentSymbol = currentSymbols[j][s]
                    currentTransition = currentTransitions[j][s]
                    
                    #First iteration
                    if i == 0:
                        if currentSymbol == "empty":
                            emptyTransitionTarget = allReferences[currentTransition.target.name]
                            newTransition = transition(emptyTransitionTarget, "empty", initUnionState)
                            initUnionState.transitions["empty"] = newTransition
                            if newTransition not in union.transitionsList: 
                                union.transitionsList.append(newTransition)
                        else:
                            if(currentSymbol not in chosenSymbols["init"]):
                                chosenSymbols["init"].append(currentSymbol)

                                newState = state(False, {})
                                newTransition = transition(newState, currentSymbol, initUnionState)

                                createdStates.append(newState)
                                createdTransitions.append(newTransition)
                                if newTransition not in union.transitionsList: 
                                    union.transitionsList.append(newTransition)
                                
                                initUnionState.transitions[currentSymbol] = newTransition
                               
                                #Target state of this symbol in old automaton
                                oldReferencedState = currentTransition.target
                                newState.final = newState.final or oldReferencedState.final

                                currentTransitionsTargets[newState.name] = [oldReferencedState.name]

                                allReferences[oldReferencedState.name] = newState    
                            else: 
                                #If symbol has already been chosen, it already has an state for it in the new automaton
                                #In this case we just need to keep track the old target state of this transition
                                chosenState = union.initialState.transitions[currentSymbol].target
                                oldReferencedState = currentTransition.target
                                currentTransitionsTargets[chosenState.name].append(oldReferencedState.name)
                                allReferences[oldReferencedState.name] = chosenState
                                chosenState.final = chosenState.final or oldReferencedState.final

                            allReferences[originalStateNameForCurrentSymbol] = initUnionState
                    else: #Rest of 
                        transitionParentState = findLastState(lastStates, oldTransitionsTargets, originalStateNameForCurrentSymbol)
                        if currentSymbol == "empty":
                            emptyTransitionTarget = allReferences[currentTransition.target.name]
                            newTransition = transition(emptyTransitionTarget, "empty", transitionParentState)
                            transitionParentState.transitions["empty"] = newTransition
                            if newTransition not in union.transitionsList: 
                                union.transitionsList.append(newTransition)
                        else: #Same logic as first iteration (remove separation later)
                            if(currentSymbol not in chosenSymbols[transitionParentState.name]):
                                chosenSymbols[transitionParentState.name].append(currentSymbol)

                                newState = state(False, {})
                                newTransition = transition(newState, currentSymbol, transitionParentState)
                                
                                createdStates.append(newState)
                                createdTransitions.append(newTransition)
                                if newTransition not in union.transitionsList: 
                                    union.transitionsList.append(newTransition)

                                transitionParentState.transitions[currentSymbol] = newTransition

                                oldReferencedState = currentTransition.target

                                newState.final = newState.final or oldReferencedState.final

                                currentTransitionsTargets[newState.name] = [oldReferencedState.name]
                                allReferences[oldReferencedState.name] = newState
                            else:
                                oldReferencedState = currentTransition.target

                                for p in createdStates:
                                    if currentSymbol in p.transitions:
                                        chosenState = p

                                currentTransitionsTargets[newState.name].append(oldReferencedState.name)
                                allReferences[oldReferencedState.name] = chosenState
                                chosenState.final = chosenState.final or oldReferencedState.final


        #Go to next level
        pathsList = list(map(lambda s: s.goLower(), pathsList))
        pathsList = [val for sublist in pathsList for val in sublist] #Remove nesting

        for s in createdStates:
            if s not in union.states:
                union.states.append(s)
        
        for t in createdTransitions:
            if newTransition not in union.transitionsList: 
                union.transitionsList.append(t)
    
    return union


def handleRepeatedTransition(t, aOrigin, bTarget, a, b, automatonMap, calledStates):
    symbol = t.symbol
    calledStates.append(aOrigin)
    if symbol not in aOrigin.transitions:
        newTransition = transition(automatonMap[bTarget.name], symbol, aOrigin)
        aOrigin.transitions[symbol] = newTransition
        if newTransition not in a.transitionsList: 
            a.transitionsList.append(newTransition)
    else:
        #Advance each state using this symbol
        if aOrigin not in calledStates:
            aOrigin = aOrigin.transitions[symbol].target

            if len(list(bTarget.transitions)) != 0:
                #Repeat process for new transitions
                for t in bTarget.transitions:
                    currTransition = bTarget.transitions[t]
                    bTarget = automatonMap[currTransition.target.name]
                    handleRepeatedTransition(currTransition, aOrigin, bTarget, a, b, automatonMap, calledStates)


def concat(a, b, finalAStates):
    startBState = b.initialState
    
    mapBToConcat = {} #Keep track of which state from B new states in concat automaton refers to

    for i in finalAStates:
        i.final = i.final and startBState.final
        #First step is to build, b from each finalStateFromA
        
        mapBToConcat[startBState.name] = i
        #Add first state from A aswell
        mapBToConcat[i.name] = i
        repeatedTransitions = []

        #Build from transitionsList
        for t in b.transitionsList:
            oldTransition = t
            currSymbol = oldTransition.symbol
            oldOrigin = oldTransition.origin
            oldTarget = oldTransition.target
            
            #For states we need to create new ones, because of name identifiers
            if oldOrigin.name not in mapBToConcat:
                newState = state(oldOrigin.final, {})
                mapBToConcat[oldOrigin.name] = newState
                mapBToConcat[newState.name] = newState
                a.states.append(newState)
            
            if oldTarget.name not in mapBToConcat:
                newState = state(oldTarget.final, {})
                mapBToConcat[oldTarget.name] = newState
                mapBToConcat[newState.name] = newState
                a.states.append(newState)

            newOrigin = mapBToConcat[oldOrigin.name]
            newTarget = mapBToConcat[oldTarget.name]
            
            
            if currSymbol in newOrigin.transitions: #Handle later
                repeatedTransitions.append(oldTransition)
            else:
                #For transitions we don't need to create new ones
                newTransition = transition(newTarget, currSymbol, newOrigin)
                newOrigin.transitions[currSymbol] = newTransition

                if newTransition not in a.transitionsList: 
                    a.transitionsList.append(newTransition)

        #Now handle repeated transitions
        for i in repeatedTransitions:
            handleRepeatedTransition(i, mapBToConcat[i.origin.name], i.target, a, b, mapBToConcat, [])

    return a

            
#No 'or' operator in this regex
#Ex of input (abcd(a(b)*c)*)
def path(regex : str) -> automaton:
    operators = ["(", ")", "*"]

    a = automaton(None, [], {}, [])

    initState = state(False, {})
    a.initialState = initState
    a.states.append(initState)
    a.statesDict[initState.name] = initState
    
    lastState = initState

    #Starting groups states, defined by '(' ocorrence
    groupStateStack = []
    
    #Notifies number of '(' operations to be handled (i.e add state to 'groupStateStack' line 136) 
    openGroup = 0

    #For other operation
    openParentheses = 0

    cutOperationsList = []
    
    i = 0
    while i < len(regex):
        realSymbol = regex[i]
        # separatePath = False
        
        if realSymbol == "(":
            openGroup += 1
            openParentheses += 1

        #Handle Group Closure
        if realSymbol == ")":
            openParentheses += -1
            startGroupState = groupStateStack.pop()
            #Not last
            if i < len(regex) - 1:
                if regex[i + 1] == "*":
                    #Add transition to go back to starting group state
                    backTransition = transition(startGroupState, "empty", lastState)
                    a.transitionsList.append(backTransition)
                    lastState.transitions["empty"] = backTransition

                    #Reset last state
                    lastState = startGroupState

                    if i + 1 == len(regex) - 1:
                        lastState.final = True
                
                #Exists other symbols
                if i < len(regex) - 2:
                    # +1 for '*', that we have already handled
                    i += 1

        if realSymbol not in operators:
            #If there is no more characters left, this is an final state
            newState = state(not (i + 1 < len(regex)), {})

            #Handle '('
            while openGroup:
                groupStateStack.append(lastState)
                openGroup += -1
            
            #Could happen in case of finished ()*
            if realSymbol in lastState.transitions:
                lastState = lastState.transitions[realSymbol].target
            else:
                newTransition = transition(newState, realSymbol, lastState)
                a.transitionsList.append(newTransition)
                lastState.transitions[realSymbol] = newTransition
                
                #Add to automaton list of states
                a.states.append(newState)
                a.statesDict[newState.name] = newState

                lastState = newState
        
        i += 1
    
    return a

#This function will build an tree informing which operations and in which onder we need to do, to construct the automaton
def buildRegexTree(regex : str, currNode : regexTree):
    if regex[0] != "(":
        currNode.value = regex
    else:
        #Remove parentheses
        regex = regex[1:-1]

        openParentheses = 0

        nextLevel = []

        i = 0

        currentWord = ""

        while i < len(regex):
            currentChar = regex[i]

            if currentChar == "(": openParentheses += 1

            if currentChar == ")": 
                openParentheses += -1
                if openParentheses == 0:
                    currentWord += ")"

                    if i + 1 < len(regex):
                        if regex[i + 1] == "*":
                            currentWord += '*'
                            i += 1

                    nextLevel.append(currentWord)
                    currentWord = ""
                    i += 1
                    continue
            
            currentWord += currentChar

            i += 1

        if currentWord != "": nextLevel.append(currentWord)

        #Pre process for union operation
        nextIsUnion = False

        if len(nextLevel) > 1:
            if nextLevel[1][0] == "|":
                nextIsUnion = True

        newUnionTree = regexTree([], "|")

        if nextIsUnion:
            #Remove '|'
            i = 1
            while i < len(nextLevel):
                nextLevel[i] = nextLevel[i][1:]
                i += 1    
            
            currNode.children.append(newUnionTree)

        for i in nextLevel:
            if len(i) != 0: 
                #We need to check if this * need's to be removed for next level of regex tree (diferentiate these two types of regex)
                #Ex: needs to be removed: ((ghi)*) / doesn't need to be removed (abd(acc)*(a)*)
                #Going to do this by counting parentheses, if parentheses count equals 0 more than one two times
                zeroCounts = 0
                auxParenthesesCount = 0

                for j in range(len(i)):
                    if i[j] == "(": auxParenthesesCount += 1
                    if i[j] == ")": auxParenthesesCount += -1

                    if auxParenthesesCount == 0: zeroCounts += 1

                if i[len(i)-1] == "*":
                    if zeroCounts == 2:
                        #In this case we remove the *
                        #and inform in the tree, by means of adding another node with '*' as value
                        # we need to encapsulate the lower levels of this branch with an ()* operation, when building automaton

                        i = i[0:-1]
                        newTree = regexTree([], "*")
                        currNode.value.append(i)
                        currNode.children.append(newTree)

                        currNode = newTree
                        newTree = regexTree([], [])
                        currNode.children.append(newTree)
                    else:
                        newTree = regexTree([], [])
                        currNode.children.append(newTree)
                else:
                    if nextIsUnion:                        
                        newTree = regexTree([], [])
                        currNode.value.append(i)
                        newUnionTree.children.append(newTree)
                    else:
                        newTree = regexTree([], [])
                        currNode.value.append(i)
                        currNode.children.append(newTree)

                buildRegexTree(i, newTree)


def applyStar(a : automaton) -> automaton:
    finalStates = a.findLastStates(a.initialState, [])    

    #Apply empty transitions from finalStates to initial State
    for i in finalStates:
        if "empty" not in i.transitions.keys():
            newTransition = transition(a.initialState, "empty", i)

            a.transitionsList.append(newTransition)
            i.transitions["empty"] = newTransition

            a.initialState.final = True
        else:
            #We need to add another state before adding empty transition, to keep one transition for which symbol in each state
            firstPathWord = a.findPath(a.initialState, i, a.initialState)[0]
            newState = state(False, {})
            a.states.append(newState)

            newTransition = transition(newState, firstPathWord, i)
            a.transitionsList.append(newTransition)
            newState.transitions[firstPathWord] = newTransition
            a.statesDict[newState.name] = newState

            #Now we add the empty transition to first state + 1
            newTransition = transition(a.initialState.transitions[firstPathWord].target, "empty", newState)

            a.transitionsList.append(newTransition)
            i.transitions["empty"] = newTransition

            a.initialState.final = True
    
    return a

def genFinalAutomaton(regexTree : regexTree) -> automaton:
    #The automaton will be built from botton up, following these rules:
    #Leaves of this tree will contain regex, that need to be given to 'path' function
    #An parent node will be formed by the union of his children, by using their automaton as input to 'unionProcess' function
    #An parent node with '*' value will have only one child and informs that it need's to be applied an ()* operation in his child automaton    
    if len(regexTree.value) > 0:
        if regexTree.value[0] == "*":
            if len(regexTree.children[0].value) > 1:
                child = genFinalAutomaton(regexTree.children[0])

                asteriscResult = applyStar(child)

            else:
                asteriscResult = applyStar(genFinalAutomaton(regexTree.children[0]))
            
            return asteriscResult

    
    
    if len(regexTree.children) > 1 :
        concatList = []

        for i in regexTree.children:
            concatList.append(genFinalAutomaton(i))

        concatResult = concatList[0]
        
        i = 1
        while i < len(concatList):
            concatResult = concat(concatResult, concatList[i], concatList[i-1].finalStates())
            i += 1

        return concatResult
    
    if len(regexTree.children) > 0:
        if regexTree.children[0].value[0] == '|':
            regexTree = regexTree.children[0]
            unionList = []
            
            for i in regexTree.children:
                unionList.append(genFinalAutomaton(i))

            unionResult = unionProcess(unionList)
            #For cases like [a-z], [A-Z], [0-9]
            if unionResult.depth() == 2:
                unionResult = minimizeUnion(unionResult)

            return unionResult
        
        if regexTree.children[0].value[0] == "*":
            #Go down to asterisc level
            regexTree = regexTree.children[0]
            if len(regexTree.children[0].value) > 1:
                child = genFinalAutomaton(regexTree.children[0])

                asteriscResult = applyStar(child)

            else:
                asteriscResult = applyStar(genFinalAutomaton(regexTree.children[0]))
            
            return asteriscResult
        
        #Basic case, found leaf
        return path(regexTree.children[0].value)
        
    
    #Basic case, found leaf
    return path(regexTree.value)

test = "(((a)|(b))(cd))"
old = "(((abd(ac c)*)(ab)*)|((bb((bc)*aa)*)(ad))|(ba)|((x)|(((ghi)|(kkkkkkk))*))|((p)|(z)))"

# testTree = regexTree([], [])
# buildRegexTree(old, testTree)
# testTree.value = old
# testTree.treePrint()

# testAutomaton = genFinalAutomaton(testTree)
# removeEmpty(testAutomaton)

# testAutomaton.showVisualDFA("./test.png")

#Problematico em casos de (()*)* ex: (bb((bc)*aa)*ad), (abd(ac c)*(a)*), por conta da ordem dos ()*, no momento esta tratando (ac c)*|(a)* como (ac c)*(a)*