#!python3
from Lexer import *
from Parser import *
from Interpreter import *
import sys

def main():
    if len(sys.argv) == 2:
        file = open(sys.argv[1],'r')
        source = file.read()
        try:
            lexer = Lexer(source)
            parser = Parser(lexer)
            interpreter = Interpreter(parser)
            result = interpreter.interpret()
            print(result)
        except Exception as e:
           print(e)    
    else:
        print("Usage: ki.py kotlinFilename")
        sys.exit()
        
if __name__ == '__main__':
    main()
