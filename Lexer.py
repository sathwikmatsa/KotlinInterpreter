from Lexemes import *       

########################################################## LEXICAL ANALYZER #############################################################

class Lexer(object):

    def __init__(self,text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.prev_token = Token(None,None)
        self.eof = 0

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
        while self.current_char is not None and self.current_char == ' ':
            self.advance()

    def skip_tabs(self):
        while self.current_char is not None and (self.current_char == '\t'):
            self.advance()        

    def skip_empty(self):
        while self.current_char is not None and self.current_char.isspace():
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
            self.skip_tabs()
            self.last_token = self.prev_token
            if self.current_char.isdigit():
                #return Token(INTEGER,self.integer())
                self.prev_token = self.num()
                return self.prev_token
            elif self.current_char == '/' and self.peek() == '/':
                while self.current_char != '\n':
                    self.advance()    
                self.skip_empty()
                self.prev_token = Token(NWLN, '\n')
                return self.prev_token 
            elif self.current_char == '/' and self.peek() == '*':
                while self.current_char != '*' or self.peek() != '/':
                    self.advance()
                self.advance()
                self.advance() 
                self.skip_empty()
                self.prev_token = Token(NWLN, '\n')
                return self.prev_token           
            elif self.current_char == '+' and self.peek() == '+':
                self.advance()
                self.advance()
                self.prev_token = Token(INC,'++')
                return self.prev_token
            elif self.current_char == '-' and self.peek() == '-':
                self.advance()
                self.advance()
                self.prev_token = Token(DEC,'--')
                return self.prev_token
            elif self.current_char == '+' and self.peek() == '=':
                self.advance()
                self.advance()
                self.text = self.text[:self.pos]+self.prev_token.value+' + '+self.text[self.pos:]
                self.current_char = self.text[self.pos]
                return Token(ASSIGN,'=')
            elif self.current_char == '-' and self.peek() == '=':
                self.advance()
                self.advance()
                self.text = self.text[:self.pos]+self.prev_token.value+' - '+self.text[self.pos:]
                self.current_char = self.text[self.pos]
                return Token(ASSIGN,'=')
            elif self.current_char == '%' and self.peek() == '=':
                self.advance()
                self.advance()
                self.text = self.text[:self.pos]+self.prev_token.value+' % '+self.text[self.pos:]
                self.current_char = self.text[self.pos]
                return Token(ASSIGN,'=')    
            elif self.current_char == '*' and self.peek() == '=':
                self.advance()
                self.advance()
                self.text = self.text[:self.pos]+self.prev_token.value+' * '+self.text[self.pos:]
                self.current_char = self.text[self.pos]
                return Token(ASSIGN,'=')
            elif self.current_char == '/' and self.peek() == '=':
                self.advance()
                self.advance()
                self.text = self.text[:self.pos]+self.prev_token.value+' / '+self.text[self.pos:]
                self.current_char = self.text[self.pos]
                return Token(ASSIGN,'=')
            elif self.current_char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                self.prev_token = Token(GTE,'>=')
                return self.prev_token 
            elif self.current_char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                self.prev_token = Token(LTE,'<=')
                return self.prev_token
            elif self.current_char == '!' and self.peek() == '=':
                self.advance()
                self.advance()
                self.prev_token = Token(NE,'!=')
                return self.prev_token
            elif self.current_char == '!' and self.peek() == '!':
                self.advance()
                self.advance()
                self.prev_token = Token(NS,'!!')
                return self.prev_token    
            elif self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                self.prev_token = Token(EQ,'==')
                return self.prev_token
            elif self.current_char == '(' and self.peek() == ')':
                self.advance()
                self.advance()
                self.prev_token = Token(MC,'()')
                return self.prev_token                                          
            elif self.current_char == '+':
                self.advance()
                self.prev_token = Token(PLUS,'+')
                return self.prev_token
            elif self.current_char == '%':
                self.advance()
                self.prev_token = Token(MOD,'%')
                return self.prev_token    
            elif self.current_char == '-':
                self.advance()
                self.prev_token = Token(MINUS,'-')
                return self.prev_token 
            elif self.current_char == '*':
                self.advance()
                self.prev_token = Token(MUL,'*')
                return self.prev_token
            elif self.current_char == '/':
                self.advance()
                self.prev_token = Token(DIV,'/')
                return self.prev_token
            elif self.current_char == '(':
                self.advance()
                self.prev_token = Token(LPAREN,'(')
                return self.prev_token
            elif self.current_char == ')':
                self.advance()
                self.prev_token = Token(RPAREN,')')
                return self.prev_token
            elif self.current_char.isalpha():
                self.prev_token = self._id()
                return self.prev_token
            elif self.current_char == '=':
                self.advance()
                self.prev_token = Token(ASSIGN,'=')
                return self.prev_token    
            elif self.current_char == ';':
                self.advance()
                self.prev_token = Token(SEMI,';')
                return self.prev_token
            elif self.current_char == '{':
                self.advance()
                self.prev_token = Token(LBRACE, '{')
                return self.prev_token
            elif self.current_char == '}':
                self.advance()
                self.prev_token = Token(RBRACE, '}')
                return self.prev_token
            elif self.current_char == ':':
                self.advance()
                self.prev_token = Token(COLON, ':')
                return self.prev_token
            elif self.current_char == '<':
                self.advance()
                self.prev_token = Token(LT,'<')
                return self.prev_token
            elif self.current_char == '>':
                self.advance()
                self.prev_token = Token(GT,'>')
                return self.prev_token
            elif self.current_char == '"':
                self.prev_token = self._string()
                return self.prev_token
            elif self.current_char == '.':
                self.advance()
                self.prev_token = Token(MOF,'.')
                return self.prev_token
            elif self.current_char == '&' and self.peek() == '&':
                self.advance()
                self.advance()
                self.prev_token = Token(AND,'&&')
                return self.prev_token
            elif self.current_char == '|' and self.peek() == '|':
                self.advance()
                self.advance()
                self.prev_token = Token(OR,'||')
                return self.prev_token                
            elif self.current_char == '\n':
                self.skip_empty()
                return Token(NWLN, '\n') 
            print(self.current_char+' '+self.peek())                                         
            self.error()
        self.eof+=1
        if self.eof==1:
            self.last_token = self.prev_token
        else:
            self.last_token = Token(EOF,None)
        return Token(EOF,None) 
