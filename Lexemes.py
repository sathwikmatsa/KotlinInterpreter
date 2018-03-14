###############################################################Token types

NUM,PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, LBRACE, RBRACE, SEMI, EOF = 'NUM','PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', '{', '}', ';', 'EOF'
ASSIGN, COLON = '=', ':'
ID = 'ID'
Int , Double, String, Boolean = 'Int', 'Double', 'String', 'Boolean' #Supported Data Types
LT = '<'
GT = '>'
QUOTES = '"'
NWLN = '\n'
INC = '++'
DEC = '--'
GTE = '>='
LTE = '<='
EQ = '=='
NE = '!='


class Token(object):

    def __init__(self,type,value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type},{value})'.format(type = self.type,value = self.value)

    def __repr__(self):
        return self.__str__()

RESERVED_KEYWORDS = {
    'val': Token('val','val'),
    'var': Token('var','var'),
    'fun': Token('fun','fun'),
    'main': Token('main','main'),
    'args': Token('args','args'),
    'Array': Token('Array','Array'),
    'println': Token('println','println'),
    'true': Token('true','true'),
    'false': Token('false','false'),
}        
