import bufferManager
def createTable(tableName):
    #find whether exist????
    write(getTableFileName(tableName),0,b'')
    return True
def dropTable(tableName):
    #
    return True
def insertValues(tableName, valueList):

    return True
def deleteValues(tableName, primaryKeyList):
    """
    delete rows whose primaryKey is in primaryKeyList
    """
    return True
def deleteValuesUsingCondition(tableName, conditionList):
    """
    delete rows satisfying conditionList
    """
    return True
def findValues(tableName, conditionList):
    """
    delete rows using conditionList
    """
    result=[]
    return result
def getTableFileName(tableName):
    return ''.join([tableName,'.txt'])
