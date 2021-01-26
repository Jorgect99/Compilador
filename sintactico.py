class Sintactico:

    contadorIf = 0
    contadorWhile = 0
    dicTypeofvariable = {}
    nameofProgram = ''
    infixList = []
    polishList = []
    polishListTypes = []
    auxiliaryList = []
    typeindex = {"integer": 0,"real": 1,"string": 2,"bool": 3}
    operatorPriority = {":=":0, "or":1,"and":2, "not:":3, "<":4, ">":4, "<=":4, ">=":4, "=":4, "<>":4,
                        "+":5, "-":5, "*":6, "div":6, "s+":7, "s-":7, "(":-1, ")":-1}
    suma = [
        ['integer','real',  'string','error'],
        ['real',   'real',  'string','error'],
        ['string', 'string','string','error'],
        ['error',  'error', 'error', 'error'],
    ]
    subtraction = [
        ['integer','real', 'error','error'],
        ['real',   'real', 'error','error'],
        ['error',  'error','error','error'],
        ['error',  'error','error','error'],
    ]
    multiply = [
        ['integer','real', 'error','error'],
        ['real',   'real', 'error','error'],
        ['error',  'error','error','error'],
        ['error',  'error','error','error'],
    ]
    division = [
        ['real', 'real', 'error','error'],
        ['real', 'real', 'error','error'],
        ['error','error','error','error'],
        ['error','error','error','error'],
    ]
    assignment = [
        ['ok',   'ok',   'error','error'],
        ['ok',   'ok',   'error','error'],
        ['error','error','ok',   'error'],
        ['error','error','error','error'],
    ]
    greaterThan = [
        ['bool','bool',  'error','error'],
        ['bool','bool',  'error','error'],
        ['error','error','error','error'],
        ['error','error','error','error'],
    ]
    smallerThan = [
        ['bool','bool',  'error','error'],
        ['bool','bool',  'error','error'],
        ['error','error','error','error'],
        ['error','error','error','error'],
    ]
    greaterEqualTo = [
        ['bool','bool',  'error','error'],
        ['bool','bool',  'error','error'],
        ['error','error','error','error'],
        ['error','error','error','error'],
    ]
    smallerEqualTo = [
        ['bool', 'bool', 'error','error'],
        ['bool', 'bool', 'error','error'],
        ['error','error','error','error'],
        ['error','error','error','error'],
    ]
    equalTo = [
        ['bool', 'bool', 'error','error'],
        ['bool', 'bool', 'error','error'],
        ['error','error','bool','error'],
        ['error','error','error','bool'],
    ]

    different = [
        ['bool', 'bool', 'error','error'],
        ['bool', 'bool', 'error','error'],
        ['error','error','bool', 'error'],
        ['error','error','error','bool'],
    ]
    andMatrix = [
        ['error', 'error', 'error', 'error'],
        ['error', 'error', 'error', 'error'],
        ['error', 'error', 'error', 'error'],
        ['error', 'error', 'error', 'bool'],
    ]
    orMatrix = [
        ['error', 'error', 'error', 'error'],
        ['error', 'error', 'error', 'error'],
        ['error', 'error', 'error', 'error'],
        ['error', 'error', 'error', 'bool'],
    ]
    notMatrix = ['error','error','error','bool']

    plusUnitary = ['integer','real','error','error']

    lessUnitary = ['integer','real','error','error']
    
    erroresSintacticos= [
              #            0                                      1  
                [ "Se esperaba 'program'"                  ,   "504"], #0 
                [ "Se esperaba identificador"              ,   "505"], #1 
                [ "Se esperaba ';'"                        ,   "506"], #3
                [ "Se esperaba '.'"                        ,   "507"], #4
                [ "Se esperaba 'begin'"                    ,   "508"], #5
                [ "Se esperaba ':'"                        ,   "509"], #6
                [ "Se esperaba algun tipo de variable"     ,   "510"], #7
                [ "Se esperaba 'end'"                      ,   "511"], #8
                [ "Se esperaba ':='"                       ,   "512"], #9
                [ "Se esperaba 'read'"                     ,   "513"], #10
                [ "Se esperaba '('"                        ,   "514"], #11
                [ "Se esperaba ')'"                        ,   "515"], #12
                [ "Se esperaba 'write'"                    ,   "516"], #13
                [ "Se esperaba 'if'"                       ,   "517"], #14
                [ "Se esperaba 'then'"                     ,   "518"], #15
                [ "Se esperaba 'while'"                    ,   "519"], #16
                [ "Se esperaba 'do'"                       ,   "520"], #17
                [ "Se esperaba factor"                     ,   "521"], #18
                [ "Variable ya declarada"                  ,   "522"], #19
                [ "Nombre de variable no valida"           ,   "523"], #20          
                [ "Variable no declarada"                  ,   "524"], #21   
                [ "Incompatibilidad de tipos"              ,   "525"], #21   
    ]
    
    def __init__(self, cabeza):
        self.errorEncontrado = False
        self.program(cabeza)
        self.printSemantic(self.infixList, self.polishListTypes, self.polishList)

    def imprimirErrorSintactico(self, errorSintactico, numRenglon):
        for self.error in self.erroresSintacticos:
            if str(errorSintactico) == self.error[1] and not self.errorEncontrado:
                self.errorEncontrado = True
                print(self.error[0], "en el renglon: ", numRenglon)
                exit()
    

    #<program> ::=program <identifier> ; <block> .
    def program(self, nodo):
        if not nodo or nodo.token != 211:# program
            self.imprimirErrorSintactico(504, nodo.renglon)
            return
        nodo = nodo.sig
        if not nodo or nodo.token != 100:#identifier
            self.imprimirErrorSintactico(505, nodo.renglon)
            return
        self.nameofProgram = nodo.lexema
        nodo = nodo.sig
        if not nodo or nodo.token != 114:#;
            self.imprimirErrorSintactico(506, nodo.renglon)
            return
        nodo = nodo.sig
        nodo = self.block(nodo)#block
        if not nodo or nodo.token != 112:
            self.imprimirErrorSintactico(507, nodo.renglon)
            return
        return

    #<block> ::= <variable declaration part><statement part>
    def block(self, nodo):
        nodo = self.variable_declaration_part(nodo)
        nodo = self.compound_statement(nodo)
        return nodo

    #<variable declaration part> ::= <empty> | var <variable declaration> ; { <variable declaration> ; }
    def variable_declaration_part(self, nodo):
        if not nodo or nodo.token != 209:
            return nodo
        nodo = nodo.sig
        nodo = self.variable_declaration(nodo)
        while nodo and nodo.token != 205:
            nodo = self.variable_declaration(nodo)
        return nodo
        
    #<variable declaration> ::= <identifier> { , <identifier> } : <type>
    def variable_declaration(self, nodo):
        if not nodo or nodo.token != 100:
            self.imprimirErrorSintactico(508, nodo.renglon)
            nodo = nodo.sig
            return nodo
        if nodo.lexema in self.dicTypeofvariable:
            self.imprimirErrorSintactico(522, nodo.renglon)
            nodo = nodo.sig
            return nodo
        self.dicTypeofvariable[nodo.lexema]=""
        nodo = nodo.sig
        while nodo and nodo.token == 113:
            nodo = nodo.sig
            if not nodo or nodo.token != 100:
                self.imprimirErrorSintactico(505, nodo.renglon)
                return nodo
            if nodo.lexema in self.dicTypeofvariable:
                self.imprimirErrorSintactico(522, nodo.renglon)
                nodo = nodo.sig
                return nodo
            self.dicTypeofvariable[nodo.lexema]=""
            nodo = nodo.sig
        if not nodo or nodo.token != 119:
            self.imprimirErrorSintactico(509, nodo.renglon)
            return nodo
        nodo = nodo.sig
        if not nodo or nodo.token not in [210,218,219,220]:
            self.imprimirErrorSintactico(510, nodo.renglon)
            return nodo
        for d in self.dicTypeofvariable:
            if self.dicTypeofvariable[d] == "":
                self.dicTypeofvariable[d] = nodo.lexema
        nodo = nodo.sig
        if not nodo or nodo.token != 114:
            self.imprimirErrorSintactico(506, nodo.renglon)
            return nodo
        for d in self.dicTypeofvariable:
            if self.nameofProgram == d:
                self.imprimirErrorSintactico(523, nodo.renglon)
        nodo = nodo.sig
        return nodo

    #<compound statement> ::= begin <statement>{ ; <statement>  }end
    def compound_statement(self, nodo):
        if not nodo or nodo.token != 205:
            self.imprimirErrorSintactico(508, nodo.renglon)
            return nodo
        nodo = nodo.sig
        nodo = self.statement(nodo)
        while nodo and nodo.token == 114:
            nodo = nodo.sig
            nodo = self.statement(nodo)
        if not nodo or nodo.token != 206:
            self.imprimirErrorSintactico(511, nodo.renglon)
            return nodo
        nodo = nodo.sig
        return nodo

    #<statement> ::=<simple statement> | <structured statement>
    def statement(self, nodo):
        nodo = self.simple_statement(nodo)
        nodo = self.structured_statement(nodo)
        return nodo

    #<simple statement> ::=<assignment statement> | <read statement> | <write statement>
    def simple_statement(self, nodo):
        if nodo and nodo.token == 100:
            nodo = self.assignment_statement(nodo)
            return nodo
        if nodo and nodo.token == 207:
            nodo = self.read_statement(nodo)
            return nodo
        if nodo and nodo.token == 208:
            nodo = self.write_statement(nodo)
            return nodo
        return nodo

    #<structured statement> ::=<compound statement> | <if statement> | <while statement>
    def structured_statement(self, nodo):
        if nodo and nodo.token == 205:
            nodo = self.compound_statement(nodo)
            return nodo
        if nodo and nodo.token == 200:
            nodo = self.if_statement(nodo)
            return nodo
        if nodo and nodo.token == 203:
            nodo = self.while_statement(nodo)
            return nodo
        return nodo

    #<assignment statement> ::=<variable> := <expression>
    def assignment_statement(self, nodo):
        if not nodo or nodo.token != 100:
            self.imprimirErrorSintactico(505, nodo.renglon)
            return nodo
        
        self.infixList.append(nodo)
        if not nodo.lexema in self.dicTypeofvariable:
            self.imprimirErrorSintactico(524, nodo.renglon)
            return nodo
        nodo = nodo.sig
        if not nodo or nodo.token != 118:
            self.imprimirErrorSintactico(512, nodo.renglon)
            return nodo
        self.infixList.append(nodo)
        nodo = nodo.sig
        nodo = self.expression(nodo)
        #self.printSemantic(nodo, self.infixList, self.polishListTypes, self.polishList)
        self.convertToPostfijo(self.infixList, nodo)
        
        return nodo

    #<read statement> ::= read ( <innodout variable> { , <input variable> } )
    def read_statement(self, nodo):
        if not nodo or nodo.token != 207:
            self.imprimirErrorSintactico(513, nodo.renglon)
            return nodo
        nodo = nodo.sig
        
        if not nodo or nodo.token != 115:
            self.imprimirErrorSintactico(514, nodo.renglon)
            return nodo
        nodo = nodo.sig
        self.infixList.append(nodo)
        if not nodo or nodo.token != 100:
            self.imprimirErrorSintactico(505, nodo.renglon)
            return nodo
        if not nodo.lexema in self.dicTypeofvariable:
            self.imprimirErrorSintactico(524, nodo.renglon)
            return nodo
        nodo = nodo.sig
        self.convertToPostfijo(self.infixList, nodo)
        self.polishList.append("read")# :)
        while nodo and nodo.token == 113:
            nodo = nodo.sig
            if not nodo or nodo.token != 100:
                self.imprimirErrorSintactico(505, nodo.renglon)
                return nodo
            if not nodo.lexema in self.dicTypeofvariable:
                self.imprimirErrorSintactico(524, nodo.renglon)
                return nodo
            nodo = nodo.sig
            self.convertToPostfijo(self.infixList, nodo)
            self.polishList.append("read")# :)
        if not nodo or nodo.token != 116:
            self.imprimirErrorSintactico(515, nodo.renglon)
            return nodo
        nodo = nodo.sig
        return nodo

    #<write statement> ::=write ( <output value> { , <output value> } )
    def write_statement(self, nodo):
        if not nodo or nodo.token != 208:
            self.imprimirErrorSintactico(516, nodo.renglon)
            return 
        nodo = nodo.sig
        if not nodo or nodo.token != 115:
            self.imprimirErrorSintactico(514, nodo.renglon)
            return nodo
        nodo = nodo.sig
        nodo = self.expression(nodo)
        #self.printSemantic(nodo, self.infixList, self.polishListTypes, self.polishList)
        self.convertToPostfijo(self.infixList, nodo)
        self.polishList.append("write")# :)
        
        while nodo and nodo.token == 113:
            nodo = nodo.sig
            nodo = self.expression(nodo)
            #self.printSemantic(nodo, self.infixList, self.polishListTypes, self.polishList)
            self.convertToPostfijo(self.infixList, nodo)
            self.polishList.append("write")# :)
            
        if not nodo or nodo.token != 116:
            self.imprimirErrorSintactico(515, nodo.renglon)
            return nodo
        nodo = nodo.sig
        return nodo

    #<if statement> ::= if <expression> then <statement> | if <expression> then <statement> else <statement>
    def if_statement(self, nodo):
        if not nodo or nodo.token != 200:
            self.imprimirErrorSintactico(517, nodo.renglon)
            return nodo
        nodo = nodo.sig
        nodo = self.expression(nodo)
        #self.printSemantic(nodo, self.infixList, self.polishListTypes, self.polishList)
        self.convertToPostfijo(self.infixList, nodo)
        contIf = self.contadorIf
        self.contadorIf+=1
        self.polishList.append("BRF-A"+ str(contIf))# :)
        if not nodo or nodo.token != 201:
            self.imprimirErrorSintactico(518, nodo.renglon)
            return nodo
        nodo = nodo.sig
        nodo = self.statement(nodo)
        self.polishList.append("BRI-B"+ str(contIf))# :)
        
        #Aqui va el apuntador
        self.polishList.append("A"+ str(contIf) + ":")
        if nodo and nodo.token == 202:
            nodo = nodo.sig
            nodo = self.statement(nodo)
        #Aqui va el apuntador
        self.polishList.append("B"+ str(contIf) + ":")
        return nodo

    #<while statement> ::=while <expression> do <statement>
    def while_statement(self, nodo):
        contWhile = self.contadorWhile
        self.contadorWhile+=1
        if not nodo or nodo.token != 203:
            self.imprimirErrorSintactico(519, nodo.renglon)
            return nodo
        nodo = nodo.sig
        self.polishList.append("D"+ str(contWhile) + ":")
        nodo = self.expression(nodo)
        #self.printSemantic(nodo, self.infixList, self.polishListTypes, self.polishList)
        self.convertToPostfijo(self.infixList, nodo)
        self.polishList.append("BRF-C"+ str(contWhile))# :)
        if not nodo or nodo.token != 204:
            self.imprimirErrorSintactico(520, nodo.renglon)
            return nodo
        nodo = nodo.sig
        
        nodo = self.statement(nodo)
        self.polishList.append("BRI-D"+ str(contWhile))# :)
        self.polishList.append("C"+ str(contWhile) + ":")
        return nodo

    #<expression> ::= <simple expression> | <simple expression> <relational operator> <simple expression>
    #<relational operator> ::= = | <> | < | <= | >= | >
    def expression(self, nodo):
        nodo = self.simple_expression(nodo)
        if nodo and nodo.token in [110, 111, 106, 108, 109, 107]:
            self.infixList.append(nodo)
            nodo = nodo.sig
            nodo = self.simple_expression(nodo)
        return nodo

    #<simple expression> ::= <sign> <term> { <adding operator> <term> }
    def simple_expression(self, nodo):
        if nodo and nodo.token in [103,104]:#Unitario
            nodo.lexema = "s"+ nodo.lexema
            self.infixList.append(nodo)
            nodo = nodo.sig
        nodo = self.term(nodo)
        while nodo and nodo.token in [103,104,215]:
            self.infixList.append(nodo)
            nodo = nodo.sig
            nodo = self.term(nodo)
        return nodo

    #<term> ::= <factor> { <multiplying operator> <factor> }
    def term(self, nodo):
        nodo = self.factor(nodo)
        while nodo and nodo.token in [105, 217, 214]:
            self.infixList.append(nodo)
            nodo = nodo.sig
            nodo = self.factor(nodo)
        return nodo

    #<factor> ::= <variable> | <constant> | ( <expression> ) | not <factor>
    def factor(self, nodo):
        if nodo and nodo.token in [100, 101, 102, 117]:
            if nodo.token == 100 and not nodo.lexema in self.dicTypeofvariable:
                self.imprimirErrorSintactico(524, nodo.renglon)
                return nodo
            self.infixList.append(nodo)
            nodo = nodo.sig
            return nodo
        if nodo and nodo.token == 216:
            self.infixList.append(nodo)
            nodo = nodo.sig
            nodo = self.factor(nodo)
        if nodo and nodo.token == 115:
            self.infixList.append(nodo)
            nodo = nodo.sig
            nodo = self.expression(nodo)
            if not nodo or nodo.token != 116:
                self.imprimirErrorSintactico(515, nodo.renglon)
                return nodo
            self.infixList.append(nodo)
            nodo = nodo.sig
            return nodo
        self.imprimirErrorSintactico(521, nodo.renglon)
        return nodo

    def convertToPostfijo(self, infixList, renglon):
        for nodo in infixList:
            self.compareOperators(nodo)
        for nodo in self.auxiliaryList[::-1]:
            self.polishListTypes.append(nodo)
            self.polishList.append(nodo)
        self.checkType(self.polishListTypes, renglon)
        self.auxiliaryList = []
        self.infixList = []
        

    def checkPriority(self, operatorInfijo):
        return self.operatorPriority[operatorInfijo]

    def compareOperators(self, nodo):
        if nodo.token in [100, 101, 102, 117]:#Operando
            self.polishList.append(nodo.lexema)  
            if nodo.token == 100:
                self.polishListTypes.append(self.dicTypeofvariable[nodo.lexema])
            elif nodo.token == 101:
                self.polishListTypes.append("integer")
            elif nodo.token == 102:
                self.polishListTypes.append("real")     
            elif nodo.token == 117:
                self.polishListTypes.append("string")     
        else:#Operador
            if self.auxiliaryList:
                if nodo.token == 116:
                    for aux in self.auxiliaryList[::-1]:
                        if aux == "(":
                            self.auxiliaryList.pop()
                            break
                        else:
                            self.polishListTypes.append(self.auxiliaryList[len(self.auxiliaryList)-1])
                            self.polishList.append(self.auxiliaryList.pop())
                elif nodo.token == 115 or self.checkPriority(nodo.lexema) > self.checkPriority(self.auxiliaryList[-1]):
                    self.auxiliaryList.append(nodo.lexema) 
                else:
                    self.polishListTypes.append(self.auxiliaryList[len(self.auxiliaryList)-1])
                    self.polishList.append(self.auxiliaryList.pop())
                    self.compareOperators(nodo)
            else:
                self.auxiliaryList.append(nodo.lexema)
                

    def checkType(self, polishListTypes , renglon):
        for nodo in polishListTypes:
            if nodo in ['integer', 'real', 'string']:
                self.auxiliaryList.append(nodo)
            elif nodo in ['s+','s-', 'not']:
                operator = self.auxiliaryList.pop()
                if nodo == "not":
                    result= self.notMatrix[self.typeindex[operator]]
                elif nodo == "s+":
                    result= self.plusUnitary[self.typeindex[operator]]
                elif nodo == "s-":
                    result= self.lessUnitary[self.typeindex[operator]]

                if result == "error":
                    self.imprimirErrorSintactico(525, renglon.renglon - 1)
                    return nodo
                else:
                    self.auxiliaryList.append(result)
            else:
                secondoperator = self.auxiliaryList.pop()
                firstoperator = self.auxiliaryList.pop()
                if nodo == "+":
                    result= self.suma[self.typeindex[firstoperator]][self.typeindex[secondoperator]]
                elif nodo == "-":
                    result = self.subtraction[self.typeindex[firstoperator]][self.typeindex[secondoperator]]
                elif nodo == "*":
                    result = self.multiply[self.typeindex[firstoperator]][self.typeindex[secondoperator]]
                elif nodo == "div":
                    result = self.division[self.typeindex[firstoperator]][self.typeindex[secondoperator]]
                elif nodo == ":=":
                    result = self.assignment[self.typeindex[firstoperator]][self.typeindex[secondoperator]]
                elif nodo == ">":
                    result = self.greaterThan[self.typeindex[firstoperator]][self.typeindex[secondoperator]]
                elif nodo == "<":
                    result = self.smallerThan[self.typeindex[firstoperator]][self.typeindex[secondoperator]]
                elif nodo == ">=":
                    result = self.greaterEqualTo[self.typeindex[firstoperator]][self.typeindex[secondoperator]]
                elif nodo == "<=":
                    result = self.smallerEqualTo[self.typeindex[firstoperator]][self.typeindex[secondoperator]]
                elif nodo == "<=":
                    result = self.equalTo[self.typeindex[firstoperator]][self.typeindex[secondoperator]]
                elif nodo == "<=":
                    result = self.different[self.typeindex[firstoperator]][self.typeindex[secondoperator]]
                elif nodo == "and":
                    result = self.andMatrix[self.typeindex[firstoperator]][self.typeindex[secondoperator]]
                elif nodo == "or":
                    result = self.orMatrix[self.typeindex[firstoperator]][self.typeindex[secondoperator]]

                if result == "error":
                    self.imprimirErrorSintactico(525, renglon.renglon - 1)
                    return nodo
                else:
                    #print(result)
                    self.auxiliaryList.append(result)
        
    
    def printSemantic(self, infixList, polishListTypes, polishList):
        #print("Infijo -->", infixList)
        #print("Tipos -->", polishListTypes)
        print("Polish -->", polishList)
        
        
    

                

    
