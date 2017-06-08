import bufferManager
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
    # ORIGINAL method: useful for other managers
    # try:
    #     f=open("tableCatalog.txt",'r')
    #     tablesBlockList=f.read().split()
    #     f.close()
    # except IOError:
    #     pass
    # try:
    #     f=open("indexCatalog.txt",'r')
    #     indicesBlockList=f.read().split()
    #     f.close()
    # except IOError:
    #     pass
    return
def closeCatalog():
    # from tablesInfo(dict) to json
    with open("tableCatalog.txt",'w') as outfile:
        json.dump(tablesInfo,outfile)
    with open("indexCatalog.txt",'w') as outfile:
        json.dump(indicesInfo,outfile)
    # for key,value in dict.items(tablesInfo):
    #     No,numOfColumns,primaryKey=value[0:3]
    #     tableName=key
    #     fields=[]
    #     for key2,value2 in dict.items(value[3]):
    #         fields+=[key2,str(value2[0]),str(value2[1],str(value2[2]))]
    #     tablesBlockList+=([str(No),str(True),tableName,str(numOfColumns),primaryKey]+fields)
    # f=open("tableCatalog.txt",'w')
    # f.write(' '.join(tablesBlockList))
    # f.close()
    # for key,value in dict.items(tablesInfo):
    #     No=value[0]
    #     indexName=key
    #     tableName,columnName=value[1:3]
    #     validation='True'
    #     indicesBlockList+=([str(No),validation,indexName,tableName,columnName])
    # f=open("indexCatalog.txt",'w')
    # f.write(' '.join(indicesBlockList))
    # f.close()
    # return
def tableListToDictValue(data):
    """
    given a data[] of one table, return a formatted tableInfoValue
    """
    No=int(data[0])
    validation=bool(data[1])
    numOfColumns=int(data[3])
    if not validation:
        return None
    tableInfoValue=[No,numOfColumns,data[4]]
    j=0
    column={}
    while j<numOfColumns:
        j+=1
        column[data[1+4*j]]=[int(data[4*j+2]),bool(data[4*j+3]),bool(data[4*j+4])]
    tableInfoValue.append(column)
    return tableInfoValue
def indexListToDictValue(data):
    validation=bool(data[1])
    if not validation:
        return None
    else:
        return [int(data[0]),data[3],data[4]]#No,tableName,columnName
def tableDictToStr(tableName,tableInfoValue):
    numOfColumns=tableInfoValue[1]
    table1=[str(tableInfoValue[0]),'1',tableName,str(numOfColumns),tableInfoValue[2]]
    table2=[]
    for key,value in dict.items(tableInfoValue[3]):
        table2+=([key,str(value[0]),str(value[1]),str(value[2])])
    return table1+table2
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
# def convertIn(fields):
#     myFields={}
#     for item in fields:
#         value=[-1,True,False]
#         if(item['type']=='float'):
#             value[0]=0
#         elif(item['type']=='char'):
#             value[0]=item['typeParam']['maxLength']
#         value[1]=item['unique']
#         myFields[item['name']]=value
#     return myFields
# def convertOut(tableName, primaryKey, fields):
#     newFields=[]
#     for key,value in dict.items(fields):
#         temp={}
#         temp['name']=key
#         if(value[0]==-1):
#             temp['type']='int'
#             temp['typeParam']={'maxLength':None}
#         elif(value[0]==0):
#             temp['type']='float'
#             temp['typeParam']={'maxLength':None}
#         else:
#             temp['type']='char'
#             temp['typeParam']={'maxLength':value[0]}
#         temp['unique']=value[1]
#         newFields.append(temp)
#     return {
#     'tableName':tableName,
#     'fields':newFields,
#     'primaryKey':primaryKey
#     }
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
    global numOfTables,tablesBlockList
    myFields=extend(tableName,primaryKey,fields)
    # add to dict
    # dict merge
    # for key in myFields:
    #     myFields[key].append(False)
    tablesInfo[tableName]=myFields
    numOfTables+=1
    # add to file
    # NO need anymore
    # tablesBlockList+=tableDictToStr(tableName,tablesInfo[tableName])
    # write list
    addIndexRecord(''.join(['index_',primaryKey]),tableName,primaryKey)
    return True
def dropTable(tableName):
    """
    :param tableName:
    :return: successful or not

    delete all the record of this table
    """
    # delete all the index
    for columnName, columnInfo in dict.items(tablesInfo[tableName]['fields']):
        indexName=columnInfo['index']
        if(indexName is not None):
            dropIndexRecord(indexName)
    # delete table
    tablesInfo.pop(tableName)
    return True
def findTable(tableName):
    """
    :param tableName:
    :return: {tableName:xxx,No:xxx,numOfColumns:xxx,etc}

    give tableName, return the information of the table
    """
    if(tableName in tablesInfo):
        infoList=tablesInfo[tableName]
        return {'tableName':tableName,'No':infoList[0],'numOfColumns':infoList[1],\
        'column':infoList[3],'primaryKey':infoList[2]}
    else:
        return None
    return tablesInfo[tableName]
def exist(tableName):
    return tableName in tablesInfo
def valueValidation(tableName,row):
    """
    check whether this row is valid for this table
    """
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
    return [indicesInfo[indexName]['tableName'],indicesInfo[indexName]['columnName']]
def addIndexRecord(indexName,tableName, columnName):
    # add to dict
    global numOfIndices,indicesBlockList
    indicesInfo[indexName]={
    'tableName':tableName,
    'columnName':columnName
    }
    # add to list
    numOfIndices+=1
    # update tablesInfo
    for field in tablesInfo[tableName]['fields']:
        if(field['name']!=columnName):
            continue
        else:
            field['index']=indexName
    return True
def dropIndexRecord(indexName):
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
def getTableSize(tableName):
    """
    :param tableName:
    :return: the number of bytes of one row of record
    """
    return tablesInfo[tableName]['size']
# DEBUG
tablesBlockList=[]#blocks of str type
tablesInfo={}#{tableName:[No,numOfColumns,primaryKey,{columnName:[type,unique,index]}]}
indicesBlockList=[]
indicesInfo={}#{indexName:[No, tableName,columnName]}
numOfTables=0
numOfIndices=0
"""
file format of recordCatalog.txt:
(totalLength:5+4*(numOfColumns))
[0]:No.
[1]:bool validation,# set when deleted
[2]:str tableName,
[3]:int numOfColumns,
[4]:str primaryKey;
[5+4*i]str columnName+type+unique?+index?[numOfColumns],
"""
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

if __name__=='__main__':
    tableName='student'
    primaryKey='no'
    fields=[
     {'name': 'no', 'type': 'char', 'unique': True, 'typeParam': 8},
     {'name': 'age', 'type': 'int', 'unique': False, 'typeParam': None},
     {'name': 'grade', 'type': 'float', 'unique': False, 'typeParam': None}
     ]
    print(tablesInfo)
    createTable(tableName,primaryKey,fields)
    # dropTable('student')
    closeCatalog()
