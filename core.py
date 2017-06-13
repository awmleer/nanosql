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
    if queryData['operation']=='insert':
        executeInsert(queryData['data'])
        return {
            'status': 'success',
            'payload': 'Successfully inserted a record into table '+queryData['data']['tableName']
        }
    if queryData['operation']=='select':
        return {
            'status': 'success',
            'payload': executeSelect(queryData['data'])
        }
    return queryData


def executeCreateTable(data):
    fields = data['fields']
    catalogManager.createTable(data['tableName'], data['primaryKey'], fields)
    columnCount=0
    for field in fields:
        if field['name']==data['primaryKey']:  # auto set primary key to unique
            field['unique']=True
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


def executeInsert(data):
    recordManager.insert(data['tableName'],data['values'])


def executeSelect(data):
    head=[]
    for field in catalogManager.getFieldsList(data['from']):
        head.append(field['name'])
    return {
        'head':head,
        'body':recordManager.select(data['from'],data['fields'],data['where'])
    }




def quit():
    indexManager.closeIndices()
    catalogManager.closeCatalog()
    bufferManager.saveAll()
    bufferManager.closeAllFiles()
