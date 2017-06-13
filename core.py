import interpreter
import bufferManager, catalogManager, recordManager, indexManager

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
    if queryData['operation']=='createTable':
        executeCreateTable(queryData['data'])
        return {
            'status': 'success',
            'payload': 'Table'+queryData['data']['tableName']+' successfully created.'
        }
    return queryData


def executeCreateTable(data):
    fields = data['fields']
    catalogManager.createTable(data['tableName'], data['primaryKey'], fields)
    columnCount=0
    for field in fields:
        if field['unique']:
            catalogManager.createIndex('autoIndex'+data['tableName'],data['tableName'],columnCount)
        columnCount+=1
    recordManager.createTable(data['tableName'])
    columnCount=0
    for field in fields:
        if field['unique']:
            indexManager.createIndex('autoIndex'+data['tableName'],data['tableName'],columnCount)
        columnCount+=1


def quit():
    indexManager.closeIndices()
    catalogManager.closeCatalog()
    bufferManager.saveAll()
    bufferManager.closeAllFiles()
