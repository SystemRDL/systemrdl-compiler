grammar SystemRDL;

prog: dummy+;

dummy : expr SEMI ;

//------------------------------------------------------------------------------
// Expressions
//------------------------------------------------------------------------------

expr: op=(PLUS|MINUS|BNOT|NOT|AND|NAND|OR|NOR|XOR|XNOR) expr_primary  #UnaryExpr
    | expr op=EXP expr              #BinaryExpr
    | expr op=(MULT|DIV|MOD) expr   #BinaryExpr
    | expr op=(PLUS|MINUS) expr     #BinaryExpr
    | expr op=(LSHIFT|RSHIFT) expr  #BinaryExpr
    | expr op=(LT|LEQ|GT|GEQ) expr  #BinaryExpr
    | expr op=(EQ|NEQ) expr         #BinaryExpr
    | expr op=AND expr              #BinaryExpr
    | expr op=(XOR|XNOR) expr       #BinaryExpr
    | expr op=OR expr               #BinaryExpr
    | expr op=BAND expr             #BinaryExpr
    | expr op=BOR expr              #BinaryExpr
    | expr '?' expr ':' expr        #TernaryExpr
    | expr_primary                  #NOP
    ;

expr_primary  : literal
              | concatenate
              | replicate
              | paren_expr
              | cast
              | reference
              | struct_literal
              | array_literal
              ;

concatenate   : '{' expr (',' expr)*'}';

replicate     : '{' expr concatenate '}';

paren_expr: '(' expr ')';

cast  : typ=(BOOLEAN_kw|BIT_kw|LONGINT_kw) '\'(' expr ')' #CastType
      | cast_width_expr '\'(' expr ')'               #CastWidth
      ;

cast_width_expr : literal
                | paren_expr
                ;

//------------------------------------------------------------------------------
// Literals
//------------------------------------------------------------------------------

literal : number
        | string_literal
        | boolean_literal
        | accesstype_literal
        | onreadtype_literal
        | onwritetype_literal
        | addressingtype_literal
        | precedencetype_literal
        | enum_literal
        ;

number : INT        #NumberInt
       | HEX_INT    #NumberHex
       | VLOG_INT   #NumberVerilog
       ;

string_literal  : STRING;

boolean_literal : val=(TRUE_kw|FALSE_kw);

array_literal : '\'{' expr (',' expr )* '}';

struct_literal : ID '\'{' struct_kv (',' struct_kv)* '}';
struct_kv : ID ':' expr ;

enum_literal : ID '::' ID;

accesstype_literal : NA_kw|RW_kw|WR_kw|R_kw|W_kw|RW1_kw|W1_kw;
onreadtype_literal : RCLR_kw|RSET_kw|RUSER_kw;
onwritetype_literal : WOSET_kw|WOCLR_kw|WOT_kw|WZS_kw|WZC_kw|WZT_kw|WCLR_kw|WSET_kw|WUSER_kw;
addressingtype_literal : COMPACT_kw|REGALIGN_kw|FULLALIGN_kw;
precedencetype_literal : HW_kw|SW_kw;


//------------------------------------------------------------------------------
// References
//------------------------------------------------------------------------------
reference   : ID
            ;

//==============================================================================
// Lexer
//==============================================================================

SL_COMMENT : ( '//' ~[\r\n]* '\r'? '\n') -> skip;
ML_COMMENT : ( '/*' .*? '*/' ) -> skip;

//------------------------------------------------------------------------------
BOOLEAN_kw          : 'boolean';
BIT_kw              : 'bit';
LONGINT_kw          : 'longint';
UNSIGNED_kw         : 'unsigned';
STRING_kw           : 'string';
ACCESSTYPE_kw       : 'accesstype';
ADDRESSINGTYPE_kw   : 'addressingtype';
ONREADTYPE_kw       : 'onreadtype';
ONWRITETYPE_kw      : 'onwritetype';

//------------------------------------------------------------------------------
// Literals
//------------------------------------------------------------------------------

// Numbers
fragment NUM_BIN : [0-1] [0-1_]* ;
fragment NUM_DEC : [0-9] [0-9_]* ;
fragment NUM_HEX : [0-9a-fA-F] [0-9a-fA-F_]* ;

INT     : NUM_DEC ;
HEX_INT : ('0x'|'0X') NUM_HEX ;
VLOG_INT: [0-9]+ '\'' ( ([bB] NUM_BIN)
                      | ([dD] NUM_DEC)
                      | ([hH] NUM_HEX)
                      )
        ;

fragment ESC : '\\"' | '\\\\' ;
STRING :  '"' (ESC | ~('"'|'\\'))* '"' ;

// Boolean
TRUE_kw : 'true';
FALSE_kw : 'false';

// Special RDL enum-like literals
NA_kw        : 'na';
RW_kw        : 'rw';
WR_kw        : 'wr';
R_kw         : 'r';
W_kw         : 'w';
RW1_kw       : 'rw1';
W1_kw        : 'w1';
RCLR_kw      : 'rclr';
RSET_kw      : 'rset';
RUSER_kw     : 'ruser';
WOSET_kw     : 'woset';
WOCLR_kw     : 'woclr';
WOT_kw       : 'wot';
WZS_kw       : 'wzs';
WZC_kw       : 'wzc';
WZT_kw       : 'wzt';
WCLR_kw      : 'wclr';
WSET_kw      : 'wset';
WUSER_kw     : 'wuser';
COMPACT_kw   : 'compact';
REGALIGN_kw  : 'regalign';
FULLALIGN_kw : 'fullalign';
HW_kw        : 'hw';
SW_kw        : 'sw';

//------------------------------------------------------------------------------
// Operators
//------------------------------------------------------------------------------

PLUS    : '+' ;
MINUS   : '-' ;
BNOT    : '!' ;
NOT     : '~' ;
BAND    : '&&' ;
NAND    : '~&' ;
AND     : '&' ;
OR      : '|' ;
BOR     : '||' ;
NOR     : '~|' ;
XOR     : '^' ;
XNOR    : '~^' | '^~' ;
LSHIFT  : '<<' ;
RSHIFT  : '>>' ;
MULT    : '*' ;
EXP     : '**' ;
DIV     : '/' ;
MOD     : '%' ;
EQ      : '==' ;
NEQ     : '!=' ;
LEQ     : '<=' ;
LT      : '<' ;
GEQ     : '>=' ;
GT      : '>' ;

//------------------------------------------------------------------------------
// Misc symbols
//------------------------------------------------------------------------------

SEMI    : ';';

//------------------------------------------------------------------------------
WS  :   [ \t\r\n]+ -> skip ;
ID  :   ('\\')? [a-zA-Z_] [a-zA-Z0-9_]* ;

