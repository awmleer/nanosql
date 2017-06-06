import interpreter
import bufferManager

def execute(command):
    queryData=interpreter.interpret(command)
    if queryData['operation']=='unknown':
        return {
            'status': 'error',
            'payload': 'Unknown SQL statement'
        }
    """
    DROP TABLE:
        - drop index
        - drop table
    CREATE TABLE:
        - create table
        - create index
    
    """
    return queryData


def quit():
    bufferManager.closeAllFiles()
