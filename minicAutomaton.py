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

number = simplifyRegex.simplify("([0-9]([0-9]*))")
otherTokenList.append(number)

identifier = simplifyRegex.simplify("(([a-z]|[A-Z])(([a-z]|[A-Z]|[0-9])*))")
otherTokenList.append(identifier)

float = simplifyRegex.simplify("([0-9]([0-9]*)(.)([0-9]*))")
otherTokenList.append(float)

test = [float]

count = 0
for i in test:
    newRegexTree = regexTree([], [])
    automaton_generation.buildRegexTree(i, newRegexTree)
    newRegexTree.value = i

    a = automaton_generation.genFinalAutomaton(newRegexTree)
    a.showVisualDFA("./empty" + str(count) + ".png")

    automaton_generation.removeEmpty(a)
    
    a.showVisualDFA("./test" + str(count) + ".png")
    count += 1

