
from nodo import Nodo

class Lexico:
    cabeza = Nodo()
    cabeza = None
    p = Nodo()
    estado = 0
    columna = 1
    valorMT = 1 
    numRenglon = 1
    caracter = 0
    lexema = ""
    errorEncontrado = False

    archivo = r"D:\Escuela\micompi\Compilador\code.txt"
    
    matriz = [
            #  L     D     +     -     *     =     .     ,     :     ;     <     >     (     )     "    Eb   tab    Nl   Eol   Eof    oc 
            #  0     1     2     3     4     5     6     7     8     9    10    11    12    13    14    15    16    17    18    19    20 
            [  1,    2,  103,  104,  105,  110,  112,  113,    7,  114,    6,    5,    8,  116,   11,    0,    0,    0,    0,    0,  503],#0
            [  1,    1,  100,  100,  100,  100,  100,  100,  100,  100,  100,  100,  100,  100,  100,  100,  100,  100,  100,  100,  100],#1
            [101,    2,  101,  101,  101,  101,    3,  101,  101,  101,  101,  101,  101,  101,  101,  101,  101,  101,  101,  101,  101],#2
            [500,    4,  500,  500,  500,  500,  500,  500,  500,  500,  500,  500,  500,  500,  500,  500,  500,  500,  500,  500,  500],#3
            [102,    4,  102,  102,  102,  102,  102,  102,  102,  102,  102,  102,  102,  102,  102,  102,  102,  102,  102,  102,  102],#4
            [107,  107,  107,  107,  107,  109,  107,  107,  107,  107,  107,  107,  107,  107,  107,  107,  107,  107,  107,  107,  107],#5
            [106,  106,  106,  106,  106,  108,  106,  106,  106,  106,  106,  111,  106,  106,  106,  106,  106,  106,  106,  106,  106],#6
            [119,  119,  119,  119,  119,  118,  119,  119,  119,  119,  119,  119,  119,  119,  119,  119,  119,  119,  119,  119,  119],#7
            [115,  115,  115,  115,    9,  115,  115,  115,  115,  115,  115,  115,  115,  115,  115,  115,  115,  115,  115,  115,  115],#8
            [  9,    9,    9,    9,   10,    9,    9,    9,    9,    9,    9,    9,    9,    9,    9,    9,    9,    9,    9,  501,    9],#9
            [  9,    9,    9,    9,    9,    9,    9,    9,    9,    9,    9,    9,    9,    0,    9,    9,    9,    9,    9,    9,    9],#10
            [ 11,   11,   11,   11,   11,   11,   11,   11,   11,   11,   11,   11,   11,   11,  117,   11,   11,   11,   502,  501,  11] #11    
    ]

    palReservadas = [
              #    0            1  
                [ "if",      "200"], #1 
                [ "then",    "201"], #2
                [ "else",    "202"], #3
                [ "while",   "203"], #4     
                [ "do",      "204"], #5
                [ "begin",   "205"], #6
                [ "end",     "206"], #7 
                [ "read",    "207"], #8 
                [ "write",   "208"], #9
                [ "var",     "209"], #10 
                [ "integer", "210"], #11 
                [ "program", "211"], #12 
                [ "true",    "212"], #13 
                [ "false",   "213"], #14 
                ["and",      "214"], #15 
                [ "or",      "215"], #17
                [ "not",     "216"], #18 
                [ "div",     "217"], #19 
                [ "real",    "218"], #20 
                [ "string",  "219"], #21
                [ "bool",    "220"]  #22
    ]

    errores= [
              #         0                   1  
                [ "Se esperaba digito",   "500"], #0 
                [ "Eof inesperado",       "501"], #2
                [ "Eol inesperado",       "502"], #3    
                [ "Simbolo no valido",    "503"]  #4
    ]

    def lexico(self):
        try:
            file = open(self.archivo, "r", newline ='')
            while self.caracter != "":
                self.caracter = file.read(1)
                if self.caracter.isalpha():
                    self.columna = 0
                elif self.caracter.isdigit():
                    self.columna = 1
                else:
                    if self.caracter == "+":
                        self.columna = 2  
                    elif self.caracter == '-':
                        self.columna = 3   
                    elif self.caracter == '*':
                        self.columna = 4   
                    elif self.caracter == '=':
                        self.columna = 5  
                    elif self.caracter == '.':
                        self.columna = 6   
                    elif self.caracter == ',':
                        self.columna = 7 
                    elif self.caracter == ':':
                        self.columna = 8  
                    elif self.caracter == ';':
                        self.columna = 9      
                    elif self.caracter == '<':
                        self.columna = 10  
                    elif self.caracter == '>':
                        self.columna = 11   
                    elif self.caracter == '(':
                        self.columna = 12 
                    elif self.caracter == ')':
                        self.columna = 13    
                    elif self.caracter == '"':
                        self.columna = 14   
                    elif self.caracter == ' ': #Espacio en blanco
                        self.columna = 15   
                    elif self.caracter == chr(9): # Tabulacion 
                        self.columna = 16      
                    elif self.caracter == chr(10): # Nueva linea
                        self.numRenglon = self.numRenglon + 1   
                        self.columna = 17         
                    elif self.caracter == chr(13): #Eol Retorno de carro
                        self.columna = 18     
                    elif self.caracter == "": #Eof
                        self.columna = 19
                    else:
                        self.columna = 20
                
                self.valorMT = self.matriz[self.estado][self.columna]  

                if self.valorMT < 100:#cambiar de estado
                    self.estado = self.valorMT
                    if self.estado == 0:
                        self.lexema = ""
                    else:
                        self.lexema = self.lexema + self.caracter
                elif self.valorMT >= 100 and self.valorMT < 500:#estado final
                    if self.valorMT == 100:
                        self.validarSiEsPalabraReservada()

                    if (self.valorMT == 100 or self.valorMT == 101 or self.valorMT == 102 or self.valorMT == 106 or 
                        self.valorMT == 107 or self.valorMT == 115 or self.valorMT >= 200):
                        file.seek(file.tell()-1)
                    else:
                        self.lexema = self.lexema + self.caracter
                
                    self.insertarNodo()
                    self.estado = 0
                    self.lexema = ""
                else:
                    self.imprimirMensajeError()
                    break
            self.imprimirNodo()
        except Exception as e:
            print(e)


    def imprimirNodo(self):
        self.p = self.cabeza
        print("{0:20}|{1:7}|{2:7}".format("Lexema","Token","Renglon"))
        print("{0:20}{1:7}{2:7}".format("--------------------","-------","---------"))
        while self.p != None:
            resultado = "{0:20}|{1:7}|{2:7}".format(self.p.lexema, str(self.p.token), str(self.p.renglon))
            print(resultado)
            self.p = self.p.sig

    def validarSiEsPalabraReservada(self):
        for self.palReservada in self.palReservadas:
            if self.lexema == self.palReservada[0]:
                self.valorMT = int(self.palReservada[1])

    def imprimirMensajeError(self):
        for self.error in self.errores:
            if str(self.valorMT) == self.error[1]:
                print("El error encontrado es: " + self.error[0])
        self.errorEncontrado = True

    def insertarNodo(self):
        nodo = Nodo(self.lexema,self.valorMT,self.numRenglon)
        if self.cabeza == None:
            self.cabeza = nodo
            self.p = self.cabeza
        else:
            self.p.sig = nodo
            self.p = nodo
