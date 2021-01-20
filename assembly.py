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
            "not": "",
            "s-":  ""}

        auxiliaryList = []
        compi_string = ""
        variable_string = "INCLUDE macos.mac\nINCLUDE fp.a\nINCLUDELIB stdlib.lib\nDOSSEG\n.MODEL SMALL\
            \nSTACK 100h\n.DATA\n\t\t\tMAXLEN DB 254\n\t\t\tLEN DB 0\n\t\t\tMSG DB 254 DUP(?)\n\t\t\tMSG_DD DD MSG\
            \n\t\t\tBUFFER		DB 8 DUP('$')\n\t\t\tCADENA_NUM     DB 10 DUP('$')\n\t\t\tBUFFERTEMP   DB 8 DUP('$')\
            \n\t\t\tBLANCO	DB '#'\n\t\t\tBLANCOS DB '$'\n\t\t\tMENOS DB '-$\n\t\t\tCOUNT    DW 0\n\t\t\tNEGATIVO    DB 0\
            \n\t\t\tBUF DW 10\n\t\t\tLISTAPAR	LABEL BYTE\n\t\t\tLONGMAX   DB 254\n\t\t\tTRUE  DW 1\n\t\t\tFALSE DW 0\
            \n\t\t\tINTRODUCIDOS    DB 254 DUP ('$')\n\t\t\tMULT10 DW 1\n\t\t\ts_true  DB 'true$'\n\t\t\ts_false DB 'false$'\n"

        code_string = ".CODE\n.386\nBEGIN:\n\t\t\tMOV   AX, @DATA\n\t\t\tMOV    DS, AX\n CALL COMPI\n\t\t\tMOV AX, 4C00H\n\t\t\tINT 21H\
            \nCOMPI PROC\n"

        for variable in variables:

            variable_string += "\t\t\t" + variable.lexema + " DW 0\n"
            


        for topo in polish:

            if type(topo) is Node:
                if topo.token in [100, 101]:
                    auxiliaryList.append(topo)

                elif topo.lexema in binary_symbols:
                    operator1 = auxiliaryList.pop()
                    operator2 = auxiliaryList.pop()
                    temporary_variable = "t" + str(counter_temporary_variable)
                    ++counter_temporary_variable
                    variable_string += "\t\t\t" + temporary_variable + " DW 0\n"
                    code_string += "\t" + binary_symbols[topo.lexema] + " " + operator2 + "," + operator1 + "," + temporary_variable + "\n"
                    auxiliaryList.append(temporary_variable)
                    
                elif topo.lexema in unary_symbols:
                    operator1 = auxiliaryList.pop()
                    temporary_variable = "t" + str(counter_temporary_variable)
                    ++counter_temporary_variable
                    variable_string += "\t\t\t" + temporary_variable + "  DW 0\n"
                    code_string += "\t" + binary_symbols[topo.lexema] + " " + operator1 + "," + temporary_variable + "\n"
                    auxiliaryList.append(temporary_variable)

                elif topo.lexema in ":=":
                    operator1 = auxiliaryList.pop()
                    operator2 = auxiliaryList.pop()
                    code_string += "\tI_ASIGNAR " + operator2 + "," + operator1 + "\n"

                elif topo.lexema in "write":
                    operator1 = auxiliaryList.pop()
                    code_string += "\tITOA BUFFER, " + operator1 + "\n"
                    code_string += "\tWRITE BUFFERTEMP\n"

                elif topo.lexema in "read":
                    operator1 = auxiliaryList.pop()
                    code_string += "READ\n" + "ASCTODEC " + operator1 + "," + "MSG\n"

            elif "BRF" in topo:
                operator1 = auxiliaryList.pop()
                code_string += "\tJF " + operator1 + "," + topo.split('-')[1] + "\n";
            elif "BRI" in topo:
                code_string +=  "\tJMP "+ topo.split('-')[1] +"\n"
            else: #Afuerzas es A0:
                code_string += "\t" + topo + "\n"
        
        code_string += "\t\tret\nCOMPI  ENDP\nBEGIN"
        file = open("compi.asm","w+")
        file.write(variable_string)
        file.write(code_string)

