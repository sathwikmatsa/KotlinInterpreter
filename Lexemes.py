###########################################################Token types##################################################################

NUM, PLUS, MINUS, MUL, DIV = 'NUM','PLUS', 'MINUS', 'MUL', 'DIV'
LPAREN, RPAREN, LBRACE, RBRACE, SEMI, EOF =  '(', ')', '{', '}', ';', 'EOF'
ASSIGN, COLON = '=', ':'
ID = 'ID'
Int , Double, String, Boolean = 'Int', 'Double', 'String', 'Boolean' #Supported Data Types
LT, GT = '<','>'
QUOTES = '"'
NWLN = '\n'
INC, DEC = '++','--'
GTE, LTE, EQ, NE = '>=','<=','==','!='
MC = '()'
MOF = '.'
NS = '!!'
MOD = '%'
AND, OR = '&&','||'

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
    'print': Token('print','print'),
    'true': Token('true','true'),
    'false': Token('false','false'),
    'if': Token('if','if'),
    'else': Token('else','else'),
    'while': Token('while','while'),
    'readLine': Token('readLine','readLine'),
    'toInt': Token('toInt','toInt'),
    'toBoolean': Token('toBoolean','toBoolean'),
    'toDouble': Token('toDouble','toDouble'),
    'toString': Token('toString','toString'),
}        
