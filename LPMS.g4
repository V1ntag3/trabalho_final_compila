grammar LPMS;

program : programSection EOF;

programSection : PROGRAM_INIT ID E_CHAVES (declarations | statement)+ D_CHAVES;

declarations : (TYPE ID (VIRGULA ID)* FIM_DE_LINHA) | (TYPE ID ATRIBUICAO_OPERADOR FIM_DE_LINHA) ;

block : E_CHAVES  statement* D_CHAVES ;

statement : assignmentStatement
          | ifStatement
          | whileStatement
          | expressionStatement
          | output
          | input;

assignmentStatement : ID (ATRIBUICAO_OPERADOR (expression | logic_expr) ) FIM_DE_LINHA;

ifStatement : IF_CONDICIONAL E_PARAN logic_expr D_PARAN block (ELSE_CONDICIONAL block)?;

whileStatement : WHILE_CONDICIONAL E_PARAN logic_expr D_PARAN block ;

expressionStatement : expression FIM_DE_LINHA ;

expression : E_PARAN expression D_PARAN
                 | MINUS_OPERADOR expression
                 | expression MODULO_OPERADOR expression
                 | expression MUL_DIV_OPERADOR expression
                 | expression (SOMA_OPERADOR | MINUS_OPERADOR) expression
                 | values_permitidos;

logic_expr : E_PARAN logic_expr D_PARAN
                | values_permitidos (RELACIONAL_OPERADOR) values_permitidos
                | values_permitidos2 (IGUALDADE_OPERADOR) values_permitidos2
                | NEG_OPERADOR logic_expr
                | BOOLEAN;

values_permitidos: INT | FLOAT | ID;

values_permitidos2: INT | FLOAT | ID | BOOLEAN;

input : INPUT_FUNCTION E_PARAN varList D_PARAN FIM_DE_LINHA;

varList : ID (VIRGULA ID)*;

output : PRINT_FUNCTION E_PARAN valueList D_PARAN FIM_DE_LINHA;

valueList : (STRING | expression) (VIRGULA (STRING | expression))*;

// Léxicas (começo com caixa alta)
// PALAVRAS OU CARACTERES RESERVADAS
PROGRAM_INIT: 'Program';
INPUT_FUNCTION: 'input';
PRINT_FUNCTION: 'print';
IF_CONDICIONAL: 'if';
ELSE_CONDICIONAL: 'else';
WHILE_CONDICIONAL: 'while';
E_PARAN: '(';
D_PARAN: ')';
E_CHAVES: '{';
D_CHAVES: '}';
FIM_DE_LINHA: ';';
VIRGULA:',';

TYPE : 'int'
     | 'float'
     | 'str'
     | 'const'
     | 'bool';

BOOLEAN: 'False' | 'True';

ID : [a-zA-Z] [a-zA-Z_0-9]* ;
INT : [0-9]+ ;
FLOAT : [0-9]+ '.' [0-9]+ ;
STRING : '"' ( '\\' (["\\] ) | ~[\r\n"] )* '"';

// OPERADORES
ATRIBUICAO_OPERADOR : '=';

MINUS_OPERADOR: '-' ;
MODULO_OPERADOR: '%' ;
MUL_DIV_OPERADOR: '*'|'/';
SOMA_OPERADOR: '+';

RELACIONAL_OPERADOR: '<'|'>'|'<='|'>=';
IGUALDADE_OPERADOR: '=='|'!=';
NEG_OPERADOR: '!';

// TEXTO IGNORADO
COMMENT : '//' ~[\r\n]* -> skip ;
WS : [ \t\r\n]+ -> skip ;
