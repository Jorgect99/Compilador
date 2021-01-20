# ----------------------------------------------------------------------------
# Nombre:       Compilador
# Autor:        Cabral Torres Jorge
# Profesor:     Ana Millan
# Clase:        Lenguaje y automatas 1
# Creado:       13 abril del 2020
# Copyright:    (c) 2020 by Cabral Torres Jorge
# ----------------------------------------------------------------------------

from lexico import Lexico
from sintactico import Sintactico
from assembly import Assembly

lexico = Lexico()
lexico.lexico()
if lexico.errorEncontrado != True:
    print("\n---Analisis lexico terminado---")
    sintaxis = Sintactico(lexico.cabeza)
    if sintaxis.errorEncontrado != True:
        print("\n---Analisis Sintactico terminado---")
        for d in sintaxis.dicTypeofvariable:
            print(d,"-->",sintaxis.dicTypeofvariable[d])
        assembly = Assembly(sintaxis.polishList, sintaxis.dicTypeofvariable)

        

            