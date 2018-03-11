from Lexemes import *

################################################################################################## INTERPRETER

class NodeVisitor(object):
    def visit(self,node):
        method_name = 'visit_'+type(node).__name__   
        visitor = getattr(self,method_name,self.generic_visit)
        return visitor(node)

    def generic_visit(self):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
    def __init__(self,parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {}

    def error(self, error_message):
        raise Exception(error_message)

    def getType(self,n):
        s = str(type(n))
        s = s[8:9].capitalize()+s[9:-2]
        if s == 'Float':
            return 'Double'
        elif s == 'Str':
            return 'String'
        return s          

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self,node):
        pass

    def visit_Assign(self, node):
        var_name = node.left.value
        if var_name not in self.GLOBAL_SCOPE:
            self.error("Kotlin: Unresolved reference: "+var_name)
        if self.GLOBAL_SCOPE[var_name][0] != None and self.GLOBAL_SCOPE[var_name][2]=='val':
            self.error("Kotlin: Val cannot be reassigned")   
        value = self.visit(node.right)   
        if self.GLOBAL_SCOPE[var_name][1] == 'Int':
            if type(value) == int:
                self.GLOBAL_SCOPE[var_name][0] = self.visit(node.right)
            else:
                self.error("Kotlin: The "+self.getType(value)+" literal does not conform to the expected type Int")    
        elif self.GLOBAL_SCOPE[var_name][1] == 'Double':
            if type(value) == float:
                self.GLOBAL_SCOPE[var_name][0] = self.visit(node.right)
            else:
                self.error("Kotlin: The "+self.getType(value)+" literal does not conform to the expected type Double") 
        elif self.GLOBAL_SCOPE[var_name][1] == 'String':
            if type(value) == str:
                self.GLOBAL_SCOPE[var_name][0] = self.visit(node.right)
            else:
                self.error("Kotlin: The "+self.getType(value)+" literal does not conform to the expected type String")    

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)[0]
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def visit_InitializeVariable(self, node):
        VAR_TYPE = node.VAR_TYPE
        var_name = node.left.value
        value = self.visit(node.right)
        if type(value) == int:
            dt = 'Int'
        elif type(value) == float:
            dt = 'Double'    
        self.GLOBAL_SCOPE[var_name] = [self.visit(node.right),dt,VAR_TYPE.type]

    def visit_Declaration(self, node):
        VAR_TYPE = node.VAR_TYPE
        var_name = node.left.value
        dt = node.right.value
        self.GLOBAL_SCOPE[var_name] = [None,dt,VAR_TYPE.type]
    
    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def visit_Str(self, node):
        return node.value    

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_PrintLn(self, node):
        print(self.visit(node.node))
        pass        
            
    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)