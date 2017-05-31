def createTable(tableName, columnMap, primaryKeyName, uniqueNameList):
    """

    :param tableName:
    :param columnMap:{columnName:type}
    :param primaryKeyName:
    :param uniqueNameList:[columnName]
    :return:successful or not

    this function should record
        the tableName,
        number of columns,
        name & type of columns,
        primary key,
        unique key,
        the name of column that has index & indexName
    """
    return True
def dropTable(tableName):
    """

    :param tableName:
    :return: successful or not

    delete all the record of this table
    """
    return True
def findTable(tableName):
    """

    :param tableName:
    :return: the information of the table in MAP

    give tableName, return the information of the table
    """
    tableInfo={}
    return  tableInfo
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
def addIndexRecord(indexName,tableName, columnName):
    return True
def dropIndexRecord(indexName):
    return True
def getAllColumn(tableName):
    columnList=[]
    return columnList
def getTableSize(tableName):
    """
    :param tableName:
    :return: the number of bytes of one row of record
    """

    return size