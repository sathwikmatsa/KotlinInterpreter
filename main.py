#!python3
from Lexer import *
from Parser import *
from Interpreter import *
import sys

def main():
    if len(sys.argv) == 2:
        file = open(sys.argv[1],'r')
        source = file.read().splitlines()
        source = "".join(source)
        lexer = Lexer(source)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)
    else:
        print("SHELL MODE: still you need to type the whole program in a single line!")
        while True:
            try:
                text = input('>>> ')
            except EOFError:
                break
            if not text:
                continue

            lexer = Lexer(text)
            parser = Parser(lexer)
            interpreter = Interpreter(parser)
            result = interpreter.interpret()
            print(result)


if __name__ == '__main__':
    main()