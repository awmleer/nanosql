from clint.textui import colored
from sys import stdin
import core
import logging
import re

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
            core.quit()
            print('Bye')
            return

        if re.match('^execfile ',command):
            execFilePath=re.sub(' *;','',re.sub('^execfile +','',command))
            command=''
            with open(execFilePath,'r') as f:
                line=f.readline()
                while line:
                    if line=='\n':
                        line = f.readline()
                        continue
                    while line[-1] == ' ' or line[-1] == '\n':
                        line = line[0:-1]
                    command += line
                    if line[-1] == ';':
                        try:
                            result = core.execute(command)
                        except Exception as e:
                            logging.exception(e)
                            command = ''
                            continue
                        print(result)
                        command=''
                    line=f.readline()
            continue

        try:
            result=core.execute(command)
        except Exception as e:
            logging.exception(e)
            command = ''
            continue
        print(result)
        command=''



if __name__ == '__main__':
    run()