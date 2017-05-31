from clint.textui import colored
from sys import stdin
import interpreter

def run():
    print('Welcome to NanoSQL')
    command=''
    while True:
        print(colored.green('> '), end='', flush=True)
        line = stdin.readline()
        while line[-1]==' ' or line[-1]=='\n':
            line=line[0:-1]
        command+=line
        if line[-1]!=';':
            continue
        if command=='quit;':
            print('Bye')
            return
        result=interpreter.execute(command)
        print(result)
        command=''
