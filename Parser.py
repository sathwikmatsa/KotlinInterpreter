from Lexemes import *

############################################################ PARSER ################################################################        

class AST(object):
    pass

class Num(AST):
    def __init__(self,token):
        self.token = token
        self.value = token.value

class Str(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Bool(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value                   

class BinOp(AST):
    def __init__(self,left,op,right):
        self.left = left
        self.token = self.op = op
        self.right = right  

class UnaryOp(AST):
    def __init__(self,op,expr):
        self.token = self.op = op
        self.expr = expr 

class Post_Unary(AST):
    def __init__(self,op,var):
        self.token = self.op = op
        self.var = var

class Pre_Unary(AST):
    def __init__(self,op,var):
        self.token = self.op = op
        self.var = var

class ReadLine(AST):
    def __init__(self,input_type = str):
        self.input_type = input_type

class TypeCast(AST):
    def __init__(self, var, input_type):
        self.var = var
        self.input_type = input_type                           

class Compound(AST):
    """Represents a '{ ... }' block"""
    def __init__(self):
        self.children = [] 

class ConditionalBlock(AST):
    def __init__(self):
        self.children = [] 

class WhileLoop(AST):
    def __init__(self,cond,token):
        self.cond = cond
        self.token = token               

class InitializeVariable(AST):
    def __init__(self, VAR_TYPE, left, op, right):
        self.VAR_TYPE = VAR_TYPE
        self.left = left
        self.token = self.op = op
        self.right = right

class Declaration(AST):
    def __init__(self, VAR_TYPE, left, op, right):
        self.VAR_TYPE = VAR_TYPE
        self.left = left
        self.token = self.op = op
        self.right = right

class Dec_Init(AST):
    def __init__(self, VAR_TYPE, left, DATA_TYPE, right):
        self.VAR_TYPE = VAR_TYPE
        self.left = left
        self.DATA_TYPE = DATA_TYPE
        self.right = right        

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Var(AST):
    """The Var node is constructed out of ID token."""
    def __init__(self,token):
        self.token = token
        self.value = token.value

class Print(AST):
    def __init__(self,node,nwln):
        self.node = node
        self.nwln = nwln                

class NoOp(AST):
    pass                  

class Parser(object):
    
    def __init__(self,lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self,message = "Invalid Syntax"):
        raise Exception(message)

    def eat(self,token_type):
        if(self.current_token.type == token_type):
            self.current_token = self.lexer.get_next_token()
        else:
            self.error("Error:Kotlin: Expected token: "+str(self.current_token.value))

    def factor(self):
        """factor : (PLUS | MINUS) factor | NUM | LPAREN expr RPAREN | String | pre _var | post _var | readLine() | var.toX()"""
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == NUM:
            self.eat(NUM)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            token = self.current_token
            if token.type == MOF:
                self.eat(MOF)
                if self.current_token.type == 'toInt':
                    t = int
                elif self.current_token.type == 'toString':
                    t = str
                elif self.current_token.type == 'toDouble':
                    t = float
                elif self.current_token.type == 'toBoolean':
                    t = bool
                self.eat(self.current_token.type)
                self.eat(MC)
                return TypeCast(node, t)
            return node
        elif token.type == String:
            self.eat(String)
            return Str(token)
        elif token.type == 'true':
            self.eat('true')
            token.type = Boolean
            token.value = True
            return Bool(token)
        elif token.type == 'false':
            self.eat('false')
            token.type = Boolean
            token.value = False
            return Bool(token)
        elif token.type == INC:
            self.eat(INC)
            node = self.variable()
            return Pre_Unary(token,node)
        elif token.type == DEC:
            self.eat(DEC)
            node = self.variable()
            return Pre_Unary(token,node)
        elif token.type == ID:
            node = self.variable()
            token = self.current_token
            if token.type == INC:
                self.eat(INC)
                return Post_Unary(token,node)
            elif token.type == DEC:
                self.eat(DEC)    
                return Post_Unary(token,node)
            elif token.type == MOF:
                self.eat(MOF)
                if self.current_token.type == 'toInt':
                    t = int
                elif self.current_token.type == 'toString':
                    t = str
                elif self.current_token.type == 'toDouble':
                    t = float
                elif self.current_token.type == 'toBoolean':
                    t = bool
                self.eat(self.current_token.type)
                self.eat(MC)
                return TypeCast(node, t)                                    
            return node
        elif token.type == 'readLine':
            self.eat('readLine')
            self.eat(MC)
            if self.current_token.type == NS:
                self.eat(NS)
                self.eat(MOF)
                if self.current_token.type == 'toString':
                    t = str
                elif self.current_token.type == 'toInt':
                    t = int 
                elif self.current_token.type == 'toDouble':
                    t = float
                elif self.current_token.type == 'toBoolean':
                    t = bool  
                self.eat(self.current_token.type)
                self.eat(MC)
                return ReadLine(t)
            elif self.current_token.type == MOF:
                self.eat(MOF)
                if self.current_token.type == 'toString':
                    self.eat('toString')
                    self.eat(MC)
                    return ReadLine()
                elif self.current_token.type in ('toInt','toBoolean','toDouble'):
                    self.error("Kotlin: Only non-null asserted (!!.) calls are allowed on a nullable receiver of type String?")
                else:
                    self.error()
            else:
                return ReadLine()        

    def term(self):
        node = self.factor()

        while self.current_token.type in (MUL,DIV,MOD):
            token = self.current_token
            self.eat(token.type)    
            node = BinOp(left = node, op = token, right = self.factor())
                    
        return node   

    def expr4(self):
        node = self.term()

        while self.current_token.type in (PLUS,MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)                   
            elif token.type == MINUS:
                self.eat(MINUS)
            node = BinOp(left =node, op = token, right = self.term()) 
               
        return node

    def expr3(self):
        node = self.expr4()

        while self.current_token.type in (LT,GT,GTE,LTE):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left =node, op = token, right = self.expr4()) 
               
        return node

    def expr2(self):
        node = self.expr3()

        while self.current_token.type in (EQ,NE):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left =node, op = token, right = self.expr3()) 
               
        return node

    def expr1(self):
        node = self.expr2()

        while self.current_token.type in (AND):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left =node, op = token, right = self.expr2()) 
               
        return node

    def expr(self):
        node = self.expr1()

        while self.current_token.type in (OR):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left =node, op = token, right = self.expr1()) 
               
        return node              

    def empty(self):
        """An empty production"""
        return NoOp()

    def variable(self):
        """ varibale : ID """
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def assignment_statement(self):
        """assignment_statement : variable ASSIGN expr"""
        left = self.variable()
        token = self.current_token
        if token.type == INC:
            self.eat(INC)
            return Post_Unary(token,left)
        elif token.type == DEC:
            self.eat(DEC)    
            return Post_Unary(token,left)
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right) 
        return node

    def decl_or_init(self):
        VAR_TYPE = self.current_token
        if VAR_TYPE.type == 'val' :
            self.eat('val')
        elif VAR_TYPE.type == 'var':
            self.eat('var')

        left = self.variable()
        op = self.current_token
        if op.type == COLON:
            self.eat(COLON)
            right = self.current_token
            self.eat(ID)
            if self.current_token.type == ASSIGN:
                self.eat(ASSIGN)
                EXP_VALUE = self.expr()
                node = Dec_Init(VAR_TYPE,left,right,EXP_VALUE)
            else:
                node = Declaration(VAR_TYPE,left,op,right)
        elif op.type == ASSIGN:
            self.eat(ASSIGN)
            right = self.expr()
            node = InitializeVariable(VAR_TYPE,left,op,right)   
        return node  

    def print_statement(self):
        try:
            self.eat('println')
            nwln = 1
        except:
            self.eat('print')
            nwln = 0    
        value = self.expr()
        node = Print(value,nwln)
        return node

    def if_block(self):
        self.eat('if')
        condition = self.expr()
        cs = self.compound_statement()
        blocks = ConditionalBlock()
        blocks.children.append([condition,cs])
        if self.current_token.type == NWLN:
            self.eat(NWLN)
        while self.current_token.type == 'else':
            self.eat('else') 
            if self.current_token.type == 'if':
                self.eat('if')
                condition = self.expr()
                cs = self.compound_statement()
                blocks.children.append([condition,cs])
            elif self.current_token.type == LBRACE:
                cs = self.compound_statement()
                token = Token('Boolean',True)
                node = Bool(token)
                blocks.children.append([node,cs])
                return blocks
            else:
                self.error("unexpected token of type: "+str(self.current_token.type)+': '+str(self.current_token.value))
            while self.current_token.type == NWLN:
                self.eat(NWLN)       
        return blocks

    def while_loop(self):
        self.eat('while')
        condition = self.expr()
        cs = self.compound_statement()
        block = WhileLoop(condition,cs)
        return block

    def statement(self):
        """
        statement : compound_statement
                  | assignment_statement
                  | declaration statement
                  | variable initialization
                  | print statement
                  | if block
                  | empty
        """ 

        if self.current_token.type == LBRACE:
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        elif self.current_token.type in ('val','var'):
            node = self.decl_or_init()
        elif self.current_token.type in ('println','print'):
            node = self.print_statement()
        elif self.current_token.type == 'if':
            node = self.if_block()
        elif self.current_token.type == 'while':
            node = self.while_loop()
        elif self.current_token.type == INC:
            token = self.current_token
            self.eat(INC)
            node = self.variable()
            return Pre_Unary(token,node)
        elif self.current_token.type == DEC:
            token = self.current_token
            self.eat(DEC)
            node = self.variable()
            return Pre_Unary(token,node)        
        else:
            node = self.empty()
        return node
    
    def statement_list(self):
        """
        statement_list : statement
                       | statement SEMI statement_list
        """  
        node = self.statement()
        results = [node]

        while self.current_token.type in (SEMI,NWLN) or (self.lexer.last_token.value == '}'and self.current_token.value != '}'):
            if self.current_token.type == SEMI:
                self.eat(SEMI)
                if self.current_token.type == NWLN:
                    self.eat(NWLN)
            elif self.current_token.type == NWLN:
                self.eat(NWLN)
                if self.current_token.type == SEMI:
                    self.eat(SEMI)
                    if self.current_token.type == NWLN:
                        self.eat(NWLN)       
            results.append(self.statement())
        if self.current_token.type == ID:
            print(self.current_token)
            self.error()

        return results   

    def compound_statement(self):
        """
        compound_statement: BEGIN statement_list END
        """   
        self.eat(LBRACE)
        nodes = self.statement_list()
        self.eat(RBRACE)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root 

    def program(self):
        """fun main LPAREN args COLON Array LAB String RAB RPAREN compound_statement"""                                                   

        self.eat('fun')
        self.eat('main')
        self.eat(LPAREN)
        self.eat('args')
        self.eat(COLON)
        self.eat('Array')
        self.eat(LT)
        self.eat(ID)
        self.eat(GT)
        self.eat(RPAREN)

        node = self.compound_statement()
        return node

    def parse(self):
        node = self.program()
        if self.current_token.type !=EOF:
            self.error()

        return node  
