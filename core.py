import interpreter
import bufferManager

def execute(command):
    queryData=interpreter.interpret(command)
    return queryData


def quit():
    bufferManager.closeAllFiles()
