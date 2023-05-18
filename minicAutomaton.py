import automaton_generation
import definitions
import simplifyRegex

regexTree = definitions.regexTree

#Scanner mini C
#tokens: ['<=', 'if', '<', '{', '-', ')', '(', 'identifier', 'for', ',', 'float', '*', 
# '+', '!=', '>=', '=', 'int', 'number', '}', '>', ';', 'while', 'else', '/', '==']

tokenAutomatonList = []
priorityAutomatonList = []

simpleTokenList = [
    '<=', 'if', '<', '{', '-', 'for', ',', '+', '!=', '>=', '=', 'int', '}', '>', ';', 'while', 'else', '/', '==', '\*', '\(', '\)'
]

count = 0 

for i in simpleTokenList:
    newRegexTree = regexTree([], [])
    automaton_generation.buildRegexTree(i, newRegexTree)
    newRegexTree.value = i

    a = automaton_generation.genFinalAutomaton(newRegexTree)
    automaton_generation.removeEmpty(a)
    if i != ",":
        a.showVisualDFA("./token" + str(count) + ".png")
    
    tokenAutomatonList.append(a)
    priorityAutomatonList.append(a)

    count += 1


#Others : ['(', ')', 'identifier', 'float', 'number', '*']

#identifier: ([a-z]|[A-Z])(([a-z]|[A-Z]|[0-9])*)
#number: ([0-9][0-9]*)
#float: ([0-9][0-9]*)(.)([0-9][0-9]*) 

otherTokenList = []

number = simplifyRegex.simplify("([0-9]([0-9]*)( ))")
otherTokenList.append(number)

identifier = simplifyRegex.simplify("(([a-z]|[A-Z])(([a-z]|[A-Z]|[0-9])*))")
otherTokenList.append(identifier)

float = simplifyRegex.simplify("([0-9]([0-9]*)(.)([0-9]*)( ))")
otherTokenList.append(float)




for i in otherTokenList:
    newRegexTree = regexTree([], [])
    automaton_generation.buildRegexTree(i, newRegexTree)
    newRegexTree.value = i

    a = automaton_generation.genFinalAutomaton(newRegexTree)
    automaton_generation.removeEmpty(a)
    a.showVisualDFA("./token" + str(count) + ".png")
    
    tokenAutomatonList.append(a)

    count += 1


