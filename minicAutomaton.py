import automaton_generation
import definitions
import simplifyRegex

regexTree = definitions.regexTree

#Scanner mini C
#tokens: ['<=', 'if', '<', '{', '-', ')', '(', 'identifier', 'for', ',', 'float', '*', 
# '+', '!=', '>=', '=', 'int', 'number', '}', '>', ';', 'while', 'else', '/', '\\n', '==']

simpleTokenList = [
    '<=', 'if', '<', '{', '-', 'for', ',', '+', '!=', '>=', '=', 'int', '}', '>', ';', 'while', 'else', '/', '=='
]

#Others : ['(', ')', 'identifier', 'float', 'number', '\', '\\n', '*']

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

basicAutomatonsList = []

count = 0
for i in otherTokenList:
    newRegexTree = regexTree([], [])
    automaton_generation.buildRegexTree(i, newRegexTree)
    newRegexTree.value = i

    a = automaton_generation.genFinalAutomaton(newRegexTree)
    a.showVisualDFA("./basic" + str(count) + ".png")
    
    basicAutomatonsList.append(a)

    count += 1

lastUnion = automaton_generation.unionProcess(basicAutomatonsList)
lastUnion.showVisualDFA("./empty.png")
# automaton_generation.removeEmpty(lastUnion)
# lastUnion.showVisualDFA("./minic.png")

