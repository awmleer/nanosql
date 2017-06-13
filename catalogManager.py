import json
"""
bytes to string : btyes.decode()
string to bytes: str.encode()
len(str)
"""
"""
todo:
problem: we need the order of fields is the same as when it is created
so change fields to list
"""
"""
```json
tablesInfo[tableName]={
'primaryKey':
'size'*:
'fields'**:[{
'name':
'type':
'typeParam':
'unique':
'index'*:str(indexName) or None
}]
}
```
"""
tablesInfo={}
indicesInfo={}#{indexName:[ tableName,columnNo]}
def openCatalog():
    global tablesInfo,indicesInfo
    # simple method from json file to dict
    try:
        with open('tableCatalog.txt','r') as infile:
            tablesInfo=json.load(infile)
        with open('indexCatalog.txt','r') as infile:
            indicesInfo=json.load(infile)
    except IOError:
        pass
    except json.decoder.JSONDecodeError:
        pass
    return
def closeCatalog():
    # from tablesInfo(dict) to json
    with open("tableCatalog.txt",'w') as outfile:
        json.dump(tablesInfo,outfile)
    with open("indexCatalog.txt",'w') as outfile:
        json.dump(indicesInfo,outfile)
def extend(tableName,primaryKey,fields):
    value={}
    value['primaryKey']=primaryKey
    value['fields']=[]
    size=5# int(No)+bool(validation)
    for item in fields:
        if(item['type']=='char'):
            size+=item['typeParam']
        else:
            size+=4 # float or int
        value['fields'].append({
        'name':item['name'],
        'type':item['type'],
        'typeParam':item['typeParam'],
        'unique':item['unique'],
        'index':None
        })
    value['size']=size
    return value

def createTable(tableName,primaryKey,fields):
    """
    :param tableName:
    :param primaryKey:
    :param fields:{columnName:[int(type),bool(unique)],bool(index)}(type: -1:int,0:float,1~255:char(1~255))
    :return:successful or not
    this function should record
        the tableName,
        number of columns,
        name & type of columns,
        primary key,
        unique key,
        the name of column that has index & indexName
    """
    global tablesBlockList
    myFields=extend(tableName,primaryKey,fields)
    # add to dict
    # dict merge
    # for key in myFields:
    #     myFields[key].append(False)
    tablesInfo[tableName]=myFields
    # add to file
    # NO need anymore
    # tablesBlockList+=tableDictToStr(tableName,tablesInfo[tableName])
    # write list
    return True
def dropTable(tableName):
    """
    :param tableName:
    :return: successful or not

    delete all the record of this table
    """
    # delete all the index
    """
    for columnName, columnInfo in dict.items(tablesInfo[tableName]['fields']):
        indexName=columnInfo['index']
        if(indexName is not None):
            indexManager.dropIndex(indexName)
            dropIndex(indexName)    
    """

    # delete table
    tablesInfo.pop(tableName)
    return True
def findTable(tableName):
    """
    :param tableName:
    :return:
    {
'primaryKey':'no',
'size'*: 21,
'fields'**:[{
'name':'student_name',
'type':'char' | 'int' | 'float',
'typeParam':None|8,
'unique':True|False,
'index'*:'index_on_student_name' | None
}]
}
    give tableName, return the information of the table
    """
    if(tableName in tablesInfo):
        return tablesInfo[tableName]
    else:
        return None

def existTable(tableName):
    return tableName in tablesInfo
def existIndex(indexName):
    return indexName in indicesInfo
def getIndexName(tableName,columnNo):
    """
    give tableName&columnName, return indexName if there is index(else return '')
    """
    for key,value in dict.items(indicesInfo):
        if value[0]==tableName and value[1]==columnNo:
            return key
    return None
def getTableAndColumnName(indexName):
    """
    give indexName, return [tableName,columnName]
    """
    return (indicesInfo[indexName])
def createIndex(indexName, tableName, columnNo):
    # add to dict
    global numOfIndices,indicesBlockList
    indicesInfo[indexName]=[tableName,columnNo]
    # add to list
    # update tablesInfo
    tablesInfo[tableName]['fields'][columnNo]['index']=indexName
    return True
def dropIndex(indexName):
    # pop in indicesInfo
    tableName,columnName=getTableAndColumnName(indexName)
    indicesInfo.pop(indexName)
    # reset None in tablesInfo
    tablesInfo[tableName]['fields'][columnName]['index']=None
    return True
def getFieldsList(tableName):
    return tablesInfo[tableName]['fields']
def getTableSize(tableName):
    # return the size (length) of one record
    return tablesInfo[tableName]['size']
def getTableInfo(tableName):
    return tablesInfo[tableName]
def getIndexList(tableName):
    indexList=[]
    for key,value in dict.items(indicesInfo):
        if (value[0]==tableName):
            indexList.append([key]+value)
    return indexList
# DEBUG

#initialize tablesBlockList
openCatalog()
# ORIGINAL method (useful in other managers)
# i=0
# length=len(tablesBlockList)
# # initialize tablesInfo
# while i<length:
#     numOfColumns=int(tablesBlockList[i+3])
#     temp=tableListToDictValue(tablesBlockList[i:i+5+4*numOfColumns])
#     if temp is None:
#         i+=(5+4*numOfColumns)
#     else:
#         tablesInfo[tablesBlockList[i+2]]=temp
#         i+=(5+4*numOfColumns)
#         numOfTables+=1
# # initialize indicesBlockList
# """
# file format of indexCatalog.txt:
# [0]:int No,
# [1]:bool validation,
# [2]:str indexName,
# [3]:str tableName,
# [4]:str columnName;
# """
# i=0
# length=len(indicesBlockList)
# # initialize indicesInfo
# while i<length:
#     temp=indexListToDictValue(indicesBlockList[i:i+5])
#     if temp is None:
#         i+=5
#     else:
#         indicesInfo[indicesBlockList[i+2]]=temp#No,tableName,columnName
#         i+=5
#         numOfIndices+=1
# tablesBlockList=[]# can we put this line after we read it to dict in __init__()????? (save memory)
# indicesBlockList=[]# can we put this line after we read it to dict in __init__()????? (save memory)
def testCreateTable():
    tableName='student'
    primaryKey='no'
    fields=[
     {'name': 'no', 'type': 'char', 'unique': True, 'typeParam': 8},
     {'name': 'age', 'type': 'int', 'unique': False, 'typeParam': None},
     {'name': 'grade', 'type': 'float', 'unique': False, 'typeParam': None}
     ]
    createTable(tableName,primaryKey,fields)
def testCreateIndex():
    createIndex('idx_student', 'student', 0)
    createIndex('idx_age', 'student', 1)
if __name__=='__main__':
    print(tablesInfo)
    print(indicesInfo)
    testCreateTable()
    testCreateIndex()
    print(tablesInfo)
    print(indicesInfo)
    # dropTable('student')
    closeCatalog()
