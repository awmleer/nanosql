import interpreter
import bufferManager, catalogManager, recordManager, indexManager

def execute(command):
    queryData=interpreter.interpret(command)
    # print(queryData)  # for DEBUG
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
        result=executeCreateTable(queryData['data'])
        if result['status']=='success':
            return {
                'status': 'success',
                'payload': 'Table '+queryData['data']['tableName']+' was successfully created.'
            }
        else:
            return result

    if queryData['operation']=='insert':
        result=executeInsert(queryData['data'])
        if result['status'] == 'success':
            return {
                'status': 'success',
                'payload': 'Successfully inserted a record into table '+queryData['data']['tableName']
            }
        else:
            return result

    if queryData['operation']=='select':
        result=executeSelect(queryData['data'])
        if result['status'] == 'success':
            return {
                'status': 'success',
                'payload': result['payload']
            }
        else:
            return result

    if queryData['operation']=='delete':
        return executeDelete(queryData['data'])

    if queryData['operation']=='createIndex':
        result=executeCreateIndex(queryData['data'])
        if result['status'] == 'success':
            return {
                'status': 'success',
                'payload': 'Index '+queryData['data']['indexName']+' was successfully created.'
            }
        else:
            return result

    if queryData['operation']=='dropIndex':
        result=executeDropIndex(queryData['data'])
        if result['status'] == 'success':
            return {
                'status': 'success',
                'payload': 'Index ' + queryData['data']['indexName'] + ' was successfully removed.'
            }
        else:
            return result

    if queryData['operation']=='dropTable':
        result=executeDropTable(queryData['data'])
        if result['status'] == 'success':
            return {
                'status': 'success',
                'payload': 'Table ' + queryData['data']['tableName'] + ' was successfully removed.'
            }
        else:
            return result

    return {
        'status':'error',
        'payload':'Interpreter failed'
    }



def executeCreateTable(data):
    if catalogManager.existTable(data['tableName']):
        return {'status': 'error', 'payload': 'Table '+data['tableName']+' already exists'}
    fields = data['fields']
    result=recordManager.createTable(data['tableName'])
    if result['status']=='error':
        return result
    result=catalogManager.createTable(data['tableName'], data['primaryKey'], fields)
    if result['status']=='error':
        return result
    for field in fields:
        if field['name']==data['primaryKey']:  # auto set primary key to unique
            field['unique']=True
            # catalogManager.createIndex('auto$' + data['tableName'] + '$' + field['name'], data['tableName'],columnCount)
    columnCount=0
    for field in fields:
        if field['unique']:
            result=catalogManager.createIndex('auto$'+data['tableName']+'$'+field['name'],data['tableName'],columnCount)
            if result['status'] == 'error':
                return result
        columnCount+=1
    columnCount=0
    for field in fields:
        if field['unique']:
            result=indexManager.createIndex('auto$'+data['tableName']+'$'+field['name'],data['tableName'],columnCount)
            if result['status'] == 'error':
                return result
        columnCount+=1
    return {
        'status':'success',
        'payload':None
    }



def executeInsert(data):
    if not catalogManager.existTable(data['tableName']):
        return {'status': 'error', 'payload': 'Table does not exist'}
    return recordManager.insert(data['tableName'],data['values'])



def executeSelect(data):
    if not catalogManager.existTable(data['from']):
        return {'status': 'error', 'payload': 'Table '+data['from']+' does not exist'}
    head=[]
    fieldList=catalogManager.getFieldsList(data['from'])
    fields=[]
    for f in fieldList:
        fields.append(f['name'])
    for field in data['fields']:
        if field in fields or '*' in data['fields']:
            head.append(field)
        else:
            return {'status': 'error', 'payload': 'Field '+field+' does not exist'}
    result=recordManager.select(data['from'],data['fields'],data['where'])
    if result['status']=='error':
        return result
    return {
        'status':'success',
        'payload':{
            'head': head,
            'body': result['payload']
        }
    }



def executeCreateIndex(data):
    if not catalogManager.existIndex(data['indexName']):
        return {'status': 'error', 'payload': 'Index already exists'}
    no=catalogManager.getFieldNumber(data['tableName'],data['fieldName'])
    if no==-1:
        return {'status': 'error', 'payload': 'Field '+data['fieldName']+' does not exist'}
    result=catalogManager.createIndex(data['indexName'],data['tableName'],no)
    if result['status']=='error':
        return result
    return indexManager.createIndex(data['indexName'],data['tableName'],no)



def executeDropIndex(data):
    if not catalogManager.existIndex(data['indexName']):
        return {'status': 'error', 'payload': 'Index does not exist'}
    result=indexManager.dropIndex(data['indexName'])
    if result['status']=='error':
        return result
    return catalogManager.dropIndex(data['indexName'])



def executeDropTable(data):
    if not catalogManager.existTable(data['tableName']):
        return {'status': 'error', 'payload': 'Table '+data['tableName']+' does not exist'}
    indices=catalogManager.getIndexList(data['tableName'])
    for index in indices:
        result=indexManager.dropIndex(index[0])
        if result['status'] == 'error':
            return result
        result=catalogManager.dropIndex(index[0])
        if result['status'] == 'error':
            return result
    result=recordManager.dropTable(data['tableName'])
    if result['status']=='error':
        return result
    return catalogManager.dropTable(data['tableName'])



def executeDelete(data):
    if not catalogManager.existTable(data['from']):
        return {'status': 'error', 'payload': 'Table '+data['tableName']+' does not exist'}
    return recordManager.delete(data['from'],data['where'])



def quit():
    indexManager.closeIndices()
    catalogManager.closeCatalog()
    bufferManager.saveAll()
    bufferManager.closeAllFiles()
