INCLUDE macos.mac
INCLUDE fp.a
INCLUDELIB stdlib.lib
DOSSEG
.MODEL SMALL            
STACK 100h
.DATA
			MAXLEN DB 254
			LEN DB 0
			MSG DB 254 DUP(?)
			MSG_DD DD MSG            
			BUFFER		DB 8 DUP('$')
			CADENA_NUM     DB 10 DUP('$')
			BUFFERTEMP   DB 8 DUP('$')            
			BLANCO	DB '#'
			BLANCOS DB '$'
			MENOS DB '-$
			COUNT    DW 0
			NEGATIVO    DB 0            
			BUF DW 10
			LISTAPAR	LABEL BYTE
			LONGMAX   DB 254
			TRUE  DW 1
			FALSE DW 0            
			INTRODUCIDOS    DB 254 DUP ('$')
			MULT10 DW 1
			s_true  DB 'true$'
			s_false DB 'false$'
.CODE
.386
BEGIN:
			MOV   AX, @DATA
			MOV    DS, AX
 CALL COMPI
			MOV AX, 4C00H
			INT 21H            
COMPI PROC
		ret
COMPI  ENDP
BEGIN