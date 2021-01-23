INCLUDE macros.mac
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
			MENOS DB '-$'
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
			num DW 0
			anterior DW 0
			actual DW 0
			fibo DW 0
			t0 DW 0
			t1 DW 0
			t2 DW 0
.CODE
.386
BEGIN:
			MOV   AX, @DATA
			MOV    DS, AX
 CALL COMPI
			MOV AX, 4C00H
			INT 21H            
COMPI PROC
	I_ASIGNAR anterior,0
	I_ASIGNAR actual,1
	I_ASIGNAR fibo,0
	READ
ASCTODEC num,MSG
	D0:
	I_MENORIGUAL fibo,num,t0
	JF t0,C0
	SUMAR anterior,actual,t1
	I_ASIGNAR fibo,t1
	I_ASIGNAR anterior,actual
	I_ASIGNAR actual,fibo
	ITOA BUFFER, fibo
	WRITE BUFFERTEMP
	WRITELN
	JMP D0
	C0:
	I_MAYORIGUAL num,10,t2
	JF t2,A0
	ITOA BUFFER, num
	WRITE BUFFERTEMP
	WRITELN
	JMP B0
	A0:
	ITOA BUFFER, num
	WRITE BUFFERTEMP
	WRITELN
	B0:
	ret
COMPI  ENDP
 END BEGIN