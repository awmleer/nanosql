from clint.textui import colored
from sys import stdin
import core
import logging
import re
import time


def run():
    print('Welcome to NanoSQL')
    command=''
    while True:
        print(colored.green(bold('> ')), end='', flush=True)
        line = stdin.readline()
        if len(line)<=1:  # if get an empty line
            continue
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
            execFromFile(execFilePath)
            command=''
            continue

        timeStart=time.time()
        try:
            result=core.execute(command)
        except Exception as e:
            logging.exception(e)
            command = ''
            continue
        timeElapsed=time.time()-timeStart
        # print(result)  # for DEBUG
        outputResult(result)
        print(bold('Execution done in '+str(round(timeElapsed,5))+' seconds.'))
        command=''



def execFromFile(filePath):
    command = ''
    with open(filePath, 'r') as f:
        line = f.readline()
        while line:
            if line == '\n':
                line = f.readline()
                continue
            while line[-1] == ' ' or line[-1] == '\n':
                line = line[0:-1]
            command += line
            if line[-1] == ';':
                if re.match('^execfile ', command):
                    execFilePath = re.sub(' *;', '', re.sub('^execfile +', '', command))
                    execFilePath = re.sub('/[^/]+$','/',filePath)+execFilePath
                    print(execFilePath)
                    execFromFile(execFilePath)
                    command=''
                    line = f.readline()
                    continue
                try:
                    result = core.execute(command)
                except Exception as e:
                    logging.exception(e)
                    command = ''
                    continue
                if result['status'] == 'error':
                    print(colored.red(result['payload']))
                command = ''
            line = f.readline()



def outputResult(result):
    # print the result based on the status
    if result['status'] == 'success':
        if type(result['payload']) == str:
            print(result['payload'])
        elif type(result['payload']) == dict:
            # calculate the max length of each column
            maxLen=[]
            table=result['payload']
            for col in table['head']:
                maxLen.append(len(str(col)))
            for row in table['body']:
                i=0
                for col in row:
                    if len(str(col))>maxLen[i]:
                        maxLen[i]=len(str(col))
                    i+=1

            printDivider(maxLen)

            print('|',end='',flush=True)
            i=0
            for col in table['head']:
                print(' ', end='', flush=True)
                print(bold(str(col)),end='',flush=True)
                batchPrint(' ',maxLen[i]-len(str(col)))
                print(' ', end='', flush=True)
                print('|',end='',flush=True)
                i+=1
            print('')

            printDivider(maxLen)

            for row in table['body']:
                print('|', end='', flush=True)
                i=0
                for col in row:
                    print(' ', end='', flush=True)
                    print(str(col), end='', flush=True)
                    # print(bold(str(col)), end='', flush=True)
                    batchPrint(' ', maxLen[i] - len(str(col)))
                    print(' ', end='', flush=True)
                    print('|', end='', flush=True)
                    i += 1
                print('')
            if len(table['body'])>0:
                printDivider(maxLen)

            print(colored.green(bold( str(len(table['body']))+' rows, '+str(len(maxLen))+' columns in set.' )))

    elif result['status'] == 'error':
        print(colored.red(result['payload']))
    else:
        print(colored.red('An unknown error occurred when execute the command.'))


def batchPrint(text,count):
    for i in range(0, count):
        print(text,end='',flush=True)

def printDivider(maxLen):
    print('+', end='', flush=True)
    for length in maxLen:
        batchPrint('-', length + 2)
        print('+', end='', flush=True)
    print('')

def bold(text):
    return '\033[1m'+text+'\033[0m'


if __name__ == '__main__':
    run()