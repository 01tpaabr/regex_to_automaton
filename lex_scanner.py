# .
# ,
# ?-
# :-
# ( 
# )
# termo: a-z(A-z + 0-9)*
# variavel: A-z(A-z + 0-9)*
# numeral: 0-9(0-9)*



#[Conjunto transições, final?]
ponto = {
    "i_ponto": [{".": "e_ponto"}, False],
    "e_ponto": [{}, True]
}

virgula = {
    "i_virgula": [{",": "e_virgula"}, False],
    "e_virgula": [{}, True]
}

interrogacao_traco = {
    "i_interrogacao_traco": [{"?": "0_interrogacao_traco"}, False],
    "0_interrogacao_traco": [{"-": "e_interrogacao_traco"}, False],
    "e_interrogacao_traco": [{}, True]
}

ponto_traco = {
    "i_ponto_traco ": [{":": "0_ponto_traco"}, False],
    "0_ponto_traco ": [{"-": "e_ponto_traco"}, False],
    "e_ponto_traco ": [{}, True]
}

abre = {
    "i_abre": [{"(": "e_abre"}, False],
    "e_abre": [{}, True]
}

fecha = {
    "i_fecha": [{")": "e_fecha"}, False],
    "e_fecha": [{}, True]
}

termo = {
    "i_termo": [{"*": "e_termo"}, False],
    "e_termo": [{"*": "e_termo", "**": "e_termo", "&": "e_termo"}, True],
}

variavel = {
    "i_variavel": [{"**": "e_variavel"}, False],
    "e_variavel": [{"*": "e_variavel", "**": "e_variavel", "&": "e_variavel"}, True],
}

numeral = {
    "i_numeral": [{"&": "e_numeral"}, False],
    "e_numeral": [{"&": "e_numeral"}, True]
}

conj_auto = [ponto, ponto_traco, virgula, interrogacao_traco, abre, fecha, termo, variavel, numeral]

letras = [chr(x) for x in range(97,123)] #representado por *
letrasM = list(map(str.capitalize, letras)) #representado por **
num = [str(i) for i in range(10)] #representado por &

#Automato final
final = {
    "i": [{".": "e_ponto", ",": "e_virgula",
        "?": "0_interrogacao_traco", ":": "0_ponto_traco",
        "(": "e_abre", ")": "e_fecha", "*": "e_termo", "**": "e_variavel", "&": "e_numeral"}, False],
    
    "0_ponto_traco": [{"-": "e_ponto_traco"}, False],
    "0_interrogacao_traco": [{"-": "e_interrogacao_traco"}, False],
    
    "e_ponto_traco": [{}, True],
    "e_interrogacao_traco": [{}, True],
    "e_ponto": [{}, True],
    "e_virgula": [{}, True],
    "e_abre": [{}, True],
    "e_fecha": [{}, True],
    "e_termo": [{"*": "e_termo", "**": "e_termo", "&": "e_termo"}, True],
    "e_variavel": [{"*": "e_variavel", "**": "e_variavel", "&": "e_variavel"}, True],
    "e_numeral": [{"&": "e_numeral", "*": "numeral_lixo", "**": "numeral_lixo"}, True],

    #Estados para facilitar tratamento de espaços necessários
    #se for um número seguido por um outro caracter aceito, sem a separação de espaços
    "numeral_lixo": [{}, False]
}

estadosErro = ["i", "numeral_lixo"]

inputFile = 'prolog.txt'

with open(inputFile, 'r') as txt:
    input = txt.read()

#Run
def run(automato, input, errorStates):
    ignoredChars = [' ', '\n']
    charIndex = 0
    exitRun = False
    tokenList = []
    error = False
    lastChar = ""

    while not exitRun and not error:
        currEstado = "i"
        currToken = ""

        while True:
            realChar = input[charIndex]
            charSymbol = realChar
            
            #Acabou arquivo
            if charIndex == len(input) - 1:
                exitRun = True
                break
            
            if realChar in letras:
                charSymbol = "*"
            
            if realChar in letrasM:
                charSymbol = "**"
            
            if realChar in num:
                charSymbol = "&"
            
            
            availableTransitions = automato[currEstado][0]

            if charSymbol not in availableTransitions.keys():
                #Estado inicial + conjunto de estados usados como lixo
                if currEstado in errorStates:
                    #Token não reconhecido
                    if realChar not in ignoredChars:
                        #Caracter não reconhecido
                        lastChar = realChar
                        error = True
                        break

                    charIndex += 1

                    
                if automato[currEstado][1]:
                    #Final aceito, adicionar em lista de token
                    tokenList.append(currToken)

                #Reiniciar reconhecimento de token
                break
            else:
                #Adicionar caracter ao token, passar para próximo estado
                currToken += realChar
                currEstado = availableTransitions[charSymbol]
            
            charIndex += 1
    
    if error:
        return "Erro, problema perto de: " + lastChar
    
    return tokenList

teste = "Quicksort(X,Y) :-\n?- Left(X)"
testeErro = "1append(X,Y)"

print(run(final, testeErro, estadosErro))
