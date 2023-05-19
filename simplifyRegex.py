from string import ascii_lowercase as lowerCase
from string import ascii_uppercase as upperCase

#Add [a-z], [0-9] and [A-Z]

def simplify(regex: str) -> str:
    result = ""

    #Operators only in this simplifier context, has nothing to do with regex operators
    operators = ["\\", "[", "]"]

    i = 0

    while i < len(regex):
        currChar = regex[i]

        if currChar not in operators:
            result += currChar
        
        #If currChar == "\", just ignore, next character will be added as an regex symbol
        #In this case will only work for ([) and (])
        if currChar == "\\":
            i += 1
            result += regex[i]
        
        if currChar == "[":
            nextChar = regex[i+1]
            
            if(nextChar == "a"):
                auxString = "("
                for j in range(len(lowerCase)):
                    if j == len(lowerCase) - 1:
                        auxString += "(" + lowerCase[j] + ")" + ")"
                    else:
                        auxString += "(" + lowerCase[j] + ")" + "|"
                result += auxString
            elif(nextChar == "A"):
                auxString = "("
                for j in range(len(upperCase)):
                    if j == len(upperCase) - 1:
                        auxString += "(" + upperCase[j] + ")" + ")"
                    else:
                        auxString += "(" + upperCase[j] + ")" + "|"
                result += auxString
            elif(nextChar == "0"):
                auxString = "("
                for j in range(10):
                    if j == 10 - 1:
                        auxString += "(" + str(j) + ")" + ")"
                    else:
                        auxString += "(" + str(j) + ")" + "|"
                result += auxString
            else:
                #will only accept [a-z], [0-9] and [A-Z], otherwise, invalid regex
                return False
            #Go to end of sequence
            i += 4
            
        i += 1 

    return result