import interpreter
import bufferManager, catalogManager, recordManager, indexManager

def execute(command):
    queryData=interpreter.interpret(command)
    print(queryData)  # for DEBUG
    if queryData['operation']=='unknown':
        return {
            'status': 'error',
            'payload': 'Unknown SQL statement'
        }

    if 'error' in queryData['data']:
        return {
            'status': 'error',
            'payload': queryData['data']['error']
        }

    if queryData['operation']=='createTable':
        executeCreateTable(queryData['data'])
        return {
            'status': 'success',
            'payload': 'Table '+queryData['data']['tableName']+' was successfully created.'
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
    if queryData['operation']=='delete':
        executeDelete(queryData['data'])
    if queryData['operation']=='createIndex':
        executeCreateIndex(queryData['data'])
        return {
            'status': 'success',
            'payload': 'Index '+queryData['data']['indexName']+' was successfully created.'
        }
    if queryData['operation']=='dropIndex':
        executeDropIndex(queryData['data'])
        return {
            'status': 'success',
            'payload': 'Index ' + queryData['data']['indexName'] + ' was successfully removed.'
        }
    if queryData['operation']=='dropTable':
        executeDropTable(queryData['data'])
        return {
            'status': 'success',
            'payload': 'Table ' + queryData['data']['tableName'] + ' was successfully removed.'
        }
    return queryData  # TODO just for DEBUG



#TODO check the execute return status

def executeCreateTable(data):
    fields = data['fields']
    catalogManager.createTable(data['tableName'], data['primaryKey'], fields)
    columnCount=0
    for field in fields:
        if field['name']==data['primaryKey']:  # auto set primary key to unique
            field['unique']=True
    for field in fields:
        if field['unique']:
            catalogManager.createIndex('auto$'+data['tableName']+'$'+field['name'],data['tableName'],columnCount)
        columnCount+=1
    recordManager.createTable(data['tableName'])
    columnCount=0
    for field in fields:
        if field['unique']:
            indexManager.createIndex('auto$'+data['tableName']+'$'+field['name'],data['tableName'],columnCount)
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



def executeCreateIndex(data):
    fields=catalogManager.getFieldsList(data['tableName'])
    count=0
    for field in fields:
        if field['name']==data['fieldName']:
            break
        count+=1
    catalogManager.createIndex(data['indexName'],data['tableName'],count)
    indexManager.createIndex(data['indexName'],data['tableName'],count)



def executeDropIndex(data):
    indexManager.dropIndex(data['indexName'])
    catalogManager.dropIndex(data['indexName'])



def executeDropTable(data):
    indices=catalogManager.getIndexList(data['tableName'])
    for index in indices:
        indexManager.dropIndex(index[0])
        catalogManager.dropIndex(index[0])
    recordManager.dropTable(data['tableName'])
    catalogManager.dropTable(data['tableName'])



def executeDelete(data):
    recordManager.delete(data['from'],data['where'])



def quit():
    indexManager.closeIndices()
    catalogManager.closeCatalog()
    bufferManager.saveAll()
    bufferManager.closeAllFiles()
