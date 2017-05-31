def createIndex(indexName, tableName, columnName):
    """
    create index on `key` in `tableName`
    e.g. create index stunameidx on student ( sname );
    """
    return True
def dropIndex(indexName):
    """
    delete an index
    e.g. drop index stunameidx;
    """
    return True
def findValuesByIndex(indexName,condition):
    """
    find values using index and ONE condition
    """
    result=[]
    return result
def getIndexName(tableName,columnName):
    """
    give tableName&columnName, return indexName if there is index(else return '')
    """
    indexName=''
    return indexName
def getTableAndColumnName(indexName):
    """
    give indexName, return [tableName,columnName]
    """
    tableName=''
    columnName=''
    return [tableName,columnName]
