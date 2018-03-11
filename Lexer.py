from Lexemes import *       

############################################################################################################ LEXICAL ANALYZER

class Lexer(object):

    def __init__(self,text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid Character')    

    def advance(self):
        self.pos+=1
        if(self.pos > len(self.text)-1):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos] 

    def peek(self):
        peek_pos = self.pos+1
        if(peek_pos > len(self.text)-1):
            return None
        else:
            return self.text[peek_pos]              

    def skip_whitespaces(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_newlines(self):
        while self.current_char is not None and (self.current_char=='\n' or self.current_char == '\t'):
            self.advance()        

    def num(self):
        result=''
        while self.current_char is not None and self.current_char.isdigit():
            result+=self.current_char
            self.advance()
        if self.current_char == '.':
            result+=self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result+=self.current_char
                self.advance()
            return Token(NUM,float(result))
        else:
            return Token(NUM,int(result))  

    def _string(self):
        result = ''
        self.advance()
        while self.current_char is not None and self.current_char != '"':
            result+=self.current_char
            self.advance()
        self.advance()    
        return Token(String,result)    


    def _id(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token          

    def get_next_token(self):

        while self.current_char is not None:
            self.skip_whitespaces()
            self.skip_newlines()
            if self.current_char.isdigit():
                #return Token(INTEGER,self.integer())
                return self.num()
            elif self.current_char == '+':
                self.advance()
                return Token(PLUS,'+')
            elif self.current_char == '-':
                self.advance()
                return Token(MINUS,'-') 
            elif self.current_char == '*':
                self.advance()
                return Token(MUL,'*')
            elif self.current_char == '/':
                self.advance()
                return Token(DIV,'/')
            elif self.current_char == '(':
                self.advance()
                return Token(LPAREN,'(')
            elif self.current_char == ')':
                self.advance()
                return Token(RPAREN,')')
            elif self.current_char.isalpha():
                return self._id()
            elif self.current_char == '=':
                self.advance()
                return Token(ASSIGN,'=')    
            elif self.current_char == ';':
                self.advance()
                return Token(SEMI,';')
            elif self.current_char == '{':
                self.advance()
                return Token(LBRACE, '{')
            elif self.current_char == '}':
                self.advance()
                return Token(RBRACE, '}')
            elif self.current_char == ':':
                self.advance()
                return Token(COLON, ':')
            elif self.current_char == '<':
                self.advance()
                return Token(LAB,'<')
            elif self.current_char == '>':
                self.advance()
                return Token(RAB,'>')
            elif self.current_char == '"':
                return self._string()                                  
            self.error()
        
        return Token(EOF,None) 