import automaton_generation
import definitions
import simplifyRegex
import run

regexTree = definitions.regexTree

#Scanner mini C
#tokens: ['<=', 'if', '<', '{', '-', ')', '(', 'identifier', 'for', ',', 'float', '*', 
# '+', '!=', '>=', '=', 'int', 'number', '}', '>', ';', 'while', 'else', '/', '==']

tokenAutomatonList = []
priorityList = []
tokenType = []

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
    if i != ",": # usar virgula da problema com a biblioteca para printar
        a.showVisualDFA("./automaton_images/token" + str(count) + ".png")
    
    tokenAutomatonList.append(a)
    if i[0] == "\\": i = i[1:]
    tokenType.append(i)
    priorityList.append(i)

    count += 1


#Others : ['(', ')', 'identifier', 'float', 'number', '*']

#identifier: ([a-z]|[A-Z])(([a-z]|[A-Z]|[0-9])*)
#number: ([0-9][0-9]*)
#float: ([0-9][0-9]*)(.)([0-9][0-9]*) 

otherTokenList = []

number = simplifyRegex.simplify("([0-9]([0-9]*)( ))")
otherTokenList.append(number)
tokenType.append("number")

identifier = simplifyRegex.simplify("(([a-z]|[A-Z])(([a-z]|[A-Z]|[0-9])*))")
otherTokenList.append(identifier)
tokenType.append("identifier")

float = simplifyRegex.simplify("([0-9]([0-9]*)(.)([0-9]*)( ))")
otherTokenList.append(float)
tokenType.append("float")


for i in otherTokenList:
    newRegexTree = regexTree([], [])
    automaton_generation.buildRegexTree(i, newRegexTree)
    newRegexTree.value = i

    a = automaton_generation.genFinalAutomaton(newRegexTree)
    automaton_generation.removeEmpty(a)
    a.showVisualDFA("./automaton_images/token" + str(count) + ".png")
    
    tokenAutomatonList.append(a)

    count += 1



inputFile = './ex_minic'

with open(inputFile, 'r') as txt:
    input = txt.read()

result = run.run(tokenAutomatonList, priorityList, tokenType, input)
print(result)


