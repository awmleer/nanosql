import interpreter


def execute(command):
    queryData=interpreter.interpret(command)
    return queryData
