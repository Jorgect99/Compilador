from nodo import Nodo

class Assembly:

    def __init__(self, polish, dicTypeofvariable):
        self.polish =  polish
        self.variables = dicTypeofvariable

        result = ""
        temporary_variable = ""
        operator1 = ""
        operator2 = ""
        counter_temporary_variable = 0

        binary_symbols = {
            "+":   "SUMAR",
            "-":   "RESTA",
            "*":   "MULTI",
            "div": "DIVIDE",
            "<":   "I_MENOR",
            ">":   "I_MAYOR",
            ">=":  "I_MAYORIGUAL",
            "<=":  "I_MENORIGUAL",
            "=":   "I_IGUAL",
            "and": "I_AND",
            "or":  "I_OR"}

        unary_symbols = {
            "not": "I_NOT",
            "s-":  "SIGNOMENOS"}

        string_macros = {
            "<>": "S_DIFERENTES",
            "=" : "S_IGUAL"
        }

        auxiliaryList = []
        compi_string = ""
        variable_string = "INCLUDE macros.mac\nDOSSEG\n.MODEL SMALL\
            \nSTACK 100h\n.DATA\n\t\t\tMAXLEN DB 254\n\t\t\tLEN DB 0\n\t\t\tMSG DB 254 DUP(?)\n\t\t\tMSG_DD DD MSG\
            \n\t\t\tBUFFER		DB 8 DUP('$')\n\t\t\tCADENA_NUM     DB 10 DUP('$')\n\t\t\tBUFFERTEMP   DB 8 DUP('$')\
            \n\t\t\tBLANCO	DB '#'\n\t\t\tBLANCOS DB '$'\n\t\t\tMENOS DB '-$'\n\t\t\tCOUNT    DW 0\n\t\t\tNEGATIVO    DB 0\
            \n\t\t\tBUF DW 10\n\t\t\tLISTAPAR	LABEL BYTE\n\t\t\tLONGMAX   DB 254\n\t\t\tTRUE  DW 1\n\t\t\tFALSE DW 0\
            \n\t\t\tINTRODUCIDOS    DB 254 DUP ('$')\n\t\t\tMULT10 DW 1\n\t\t\ts_true  DB 'true$'\n\t\t\ts_false DB 'false$'\n"

        code_string = ".CODE\n.386\nBEGIN:\n\t\t\tMOV   AX, @DATA\n\t\t\tMOV    DS, AX\n CALL COMPI\n\t\t\tMOV AX, 4C00H\n\t\t\tINT 21H\
            \nCOMPI PROC\n"

        for variable in self.variables:

            variable_string += "\t\t\t" + variable + " DW 0\n"

        for topo in self.polish:

            if topo in binary_symbols:
                operator1 = auxiliaryList.pop()
                operator2 = auxiliaryList.pop()
                temporary_variable = "t" + str(counter_temporary_variable)
                counter_temporary_variable+=1
                variable_string += "\t\t\t" + temporary_variable + " DW 0\n"
                code_string += "\t" + binary_symbols[topo] + " " + operator2 + "," + operator1 + "," + temporary_variable + "\n"
                auxiliaryList.append(temporary_variable)
                
            elif topo in unary_symbols:
                operator1 = auxiliaryList.pop()
                temporary_variable = "t" + str(counter_temporary_variable)
                counter_temporary_variable+=1
                variable_string += "\t\t\t" + temporary_variable + "  DW 0\n"
                code_string += "\t" + binary_symbols[topo] + " " + operator1 + "," + temporary_variable + "\n"
                auxiliaryList.append(temporary_variable)

            elif topo == ":=":
                operator1 = auxiliaryList.pop()
                operator2 = auxiliaryList.pop()
                code_string += "\tI_ASIGNAR " + operator2 + "," + operator1 + "\n"

            elif topo == "write":
                operator1 = auxiliaryList.pop()
                code_string += "\tITOA BUFFER, " + operator1 + "\n"
                code_string += "\tWRITE BUFFERTEMP\n\tWRITELN\n"

            elif topo == "read":
                operator1 = auxiliaryList.pop()
                code_string += "\tREAD\n" + "ASCTODEC " + operator1 + "," + "MSG\n"

            elif "BRF" in topo:
                operator1 = auxiliaryList.pop()
                code_string += "\tJF " + operator1 + "," + topo.split('-')[1] + "\n";

            elif "BRI" in topo:
                code_string +=  "\tJMP "+ topo.split('-')[1] +"\n"

            elif ":" in topo: #Afuerzas es A0:
                code_string += "\t" + topo + "\n"

            else:
                auxiliaryList.append(topo)
        
        code_string += "\tret\nCOMPI  ENDP\n END BEGIN"
        file = open("compi.asm","w+")
        file.write(variable_string)
        file.write(code_string)

