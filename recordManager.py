"""
Question: how to control the behavior when the we need to change the next block (when space of current block is not enough)
"""
import bufferManager
import struct
import catalogManager
import indexManager
import math
# bytes conversion
###(10086).to_bytes(4, byteorder='big')
###int.from_bytes(b'\x00\x00\x00\x01', byteorder='little')
###struct.pack('i', 3)
###struct.unpack('i', b'\x00\x00\x00\x01')
###struct.pack('f', 3.141592654)
###struct.unpack('f', b'\xdb\x0fI@')
# little end by default
"""
todo:
use selectIndex inside select function
todo:
delete using index
"""



def strToBytes(string,size):
    by = str.encode(string)
    by += b"\x00" * (size - len(by))
    return by


def pack(tableName,recordList, fieldsList):
    i=0
    # add No at first, add validation at second
    count=countRecord(tableName)
    bytesList=[struct.pack('i',count),struct.pack('?',1)]
    for field in fieldsList:
        if(field['type']=='int'):
            bytesList.append(struct.pack('i', int(recordList[i])))
        elif(field['type']=='float'):
            bytesList.append(struct.pack('f', float(recordList[i])))
        else:
            bytesList.append(strToBytes(recordList[i],field['typeParam']))
        i+=1

    return count,b''.join(bytesList)


def unpack(bytesRecord,fieldsList):
    i=0
    recordList=[]
    # if valid
    if not struct.unpack('?',bytesRecord[4:5])[0]:
        return []
    # ignore 'No' at first
    bytesRecord=bytesRecord[5:]
    for field in fieldsList:
        if(field['type']=='int'):
            recordList.append(struct.unpack('i', bytesRecord[i:i+4])[0])
            i+=4
        elif(field['type']=='float'):
            recordList.append(struct.unpack('f', bytesRecord[i:i+4])[0])
            i+=4
        else:
            strLength=field['typeParam']
            string=bytes.decode(bytesRecord[i:i+strLength]).strip('\x00')
            recordList.append(string)
            i+=(strLength)
    return recordList


def unpackWithNo(bytesRecord,fieldsList):
    i=0
    recordList=[]
    # if valid
    if not struct.unpack('?',bytesRecord[4:5])[0]:
        return []
    # unpack No first
    recordList.append(struct.unpack('i', bytesRecord[0:4])[0])
    bytesRecord=bytesRecord[5:]
    for field in fieldsList:
        if(field['type']=='int'):
            recordList.append(struct.unpack('i', bytesRecord[i:i+4])[0])
            i+=4
        elif(field['type']=='float'):
            recordList.append(struct.unpack('f', bytesRecord[i:i+4])[0])
            i+=4
        else:
            strLength=field['typeParam']
            string=bytes.decode(bytesRecord[i:i+strLength]).strip('\x00')
            recordList.append(string)
            i+=(strLength)
    return recordList


def countRecord(tableName):
    """
    return the total Record of this table (including deleted )
    """
    size=catalogManager.getTableSize(tableName)
    fileName=getTableFileName(tableName)
    blockCount=bufferManager.blockCount(fileName)
    if(blockCount==0):
        return 0
    count=(blockCount-1)*math.floor(bufferManager.BLOCK_SIZE/size)
    lastBlock=bufferManager.read(fileName,blockCount-1,cache=True)
    return count+math.ceil(len(lastBlock)/size)


def createTable(tableName):
    #find whether exist????
    if catalogManager.existTable(tableName):
        return {  'status':'error','payload': 'table already exists'}
    fileName=getTableFileName(tableName)
    bufferManager.write(fileName,0,b'',cache=True)
    return {  'status':'success','payload': ''}


def dropTable(tableName):
    bufferManager.delete(getTableFileName(tableName))
    return True


def insert(tableName, recordList):
    fileName=getTableFileName(tableName)
    if not catalogManager.existTable(tableName):
        return {  'status':'error','payload': 'table does not exist'}
    fieldsList=catalogManager.getFieldsList(tableName)
    i=0
    for field in fieldsList:
        if not field['unique']:
            i+=1
            continue
        if(field['type']=='int'):
            value=int(recordList[i])
        elif(field['type']=='float'):
            value=float(recordList[i])
        else:
            value=str(recordList[i])
        if (select('student',['*'],[{'field':field['name'],'operand':'=','value':value}])) !=[[]]:
            return {  'status':'error','payload': 'duplicated unique key'}
        i+=1

    no,bytesRecord=pack(tableName,recordList,fieldsList)
    # append the the last
    blockCount=bufferManager.blockCount(fileName)
    if blockCount==0:
        blockCount=1
    lastBlock=bufferManager.read(fileName,blockCount-1,cache=True)
    size=catalogManager.getTableSize(tableName)
    freeSpace=bufferManager.BLOCK_SIZE-len(lastBlock)
    if freeSpace>=size:
        #append to current blockBuffer
        bufferManager.write(fileName,blockCount-1,b''.join([lastBlock,bytesRecord]),cache=True)
    else:
        #塞入占位符 first
        bufferManager.write(fileName,blockCount-1,b''.join([lastBlock,b'\x00'*freeSpace]),cache=True)
        #append to next blockBuffer
        bufferManager.write(fileName,blockCount,bytesRecord,cache=True)
    # insert index
    for indexItem in catalogManager.getIndexList(tableName):
        # [indexName, tableName, columnNo]
        indexName=indexItem[0]
        columnNo=indexItem[2]
        key=recordList[columnNo]
        # select type
        if(fieldsList[columnNo]['type']=='int'):
            key=int(key)
        elif(fieldsList[columnNo]['type']=='float'):
            key=float(key)
        indexManager.insertIndex(indexName,key,no)
    return {  'status':'success','payload': ''}


def delete(tableName,where):
    # get each rows
    # satisfy conditions?
    fileName=getTableFileName(tableName)
    blockCount=bufferManager.blockCount(fileName)
    size=catalogManager.getTableSize(tableName)
    recordList=[]
    count=0
    if where==[]:
        #delete all
        myWhere=[]
    # if condition is not empty
    myWhere=convertInWhere(tableName,where)
    for blockNo in range(blockCount):
        # this is a copy
        blockContent=bufferManager.read(fileName,blockNo,cache=True)
        ba=bytearray(blockContent)
        # divide this blockContent into rows
        rows=len(blockContent)//size
        for i in range(rows):
            oneRecord=unpack(blockContent[i*size:(i+1)*size],catalogManager.getFieldsList(tableName))
            if(oneRecord==[]):# deleted before
                continue
            flag=True
            for condition in myWhere:
                if not (eval(''.join([repr(oneRecord[condition['field']]),condition['operand'],repr(condition['value'])]))):
                    flag=False
                    break
            if flag:
                # i think i should change validation bit directly
                ba[i*size+4]=0
                count+=1
        bufferManager.write(fileName,blockNo,bytes(ba),cache=True)
    return {'status': 'success', 'payload': count}


def fieldsNameTofieldsNo(tableName,fieldName):
    i=0
    for field in catalogManager.getFieldsList(tableName):
        if field['name']==fieldName:
            return i
        else:
            i+=1
    return None


def convertInWhere(tableName,where):
    for condition in where:
        condition['field']=fieldsNameTofieldsNo(tableName,condition['field'])
        if(condition['operand']=='<>'):
            condition['operand']='!='
        elif(condition['operand']=='='):
            condition['operand']='=='
    return where


def select(tableName,fields,where):
    """
    select and project
    """
    # get each rows
    # satisfy conditions?
    # if we can select using index
    fieldsList=catalogManager.getFieldsList(tableName)
    if(where==[]):
        # select all!!!!!
        myWhere=[]
    else:
        myWhere=convertInWhere(tableName,where)
        indexName=catalogManager.getIndexName(tableName,myWhere[0]['field'])
        if len(myWhere)==1 and indexName is not None and myWhere[0]['operand'] == '==':
            #convert type
            value=myWhere[0]['value']
            type=fieldsList[myWhere[0]['field']]['type']
            if(type=='int'):
                value=int(value)
            elif(type=='float'):
                value=float(value)
            return indexManager.select(indexName,fields,value)
    # else we use default select methods
    fileName=getTableFileName(tableName)
    blockCount=bufferManager.blockCount(fileName)
    size=catalogManager.getTableSize(tableName)
    recordList=[]

    myFields=[]
    if(fields==['*']):
        myFields=['*']
    else:
        for item in fields:
            myFields.append(fieldsNameTofieldsNo(tableName,item))
    for blockNo in range(blockCount):
        # this is a copy
        blockContent=bufferManager.read(fileName,blockNo,cache=True)
        # divide this block into rows
        rows=len(blockContent)//size
        for i in range(rows):
            oneRecord=unpack(blockContent[i*size:(i+1)*size],fieldsList)
            if(oneRecord==[]):
                continue
            flag=True
            for condition in myWhere:
                if not (eval(''.join([repr(oneRecord[condition['field']]),condition['operand'],repr(condition['value'])]))):
                    flag=False
            if flag:
                #project
                newRecord=[]
                if(myFields==['*']):
                    newRecord=oneRecord
                else:
                    for No in myFields:
                        #copy !!!
                        newRecord.append(oneRecord[No])
                #append
                recordList.append(newRecord)
    return recordList


def selectWithNo(tableName,columnName):
    fileName=getTableFileName(tableName)
    blockCount=bufferManager.blockCount(fileName)
    size=catalogManager.getTableSize(tableName)
    recordList=[]
    fieldNo=fieldsNameTofieldsNo(tableName,columnName)
    for blockNo in range(blockCount):
        # this is a copy
        blockContent=bufferManager.read(fileName,blockNo,cache=True)
        # divide this block into rows
        rows=len(blockContent)//size
        for i in range(rows):
            oneRecord=unpackWithNo(blockContent[i*size:(i+1)*size],catalogManager.getFieldsList(tableName))
            if(oneRecord==[]):
                continue
            recordList.append([oneRecord[fieldNo+1],oneRecord[0]])# key and value
    recordList=sorted(recordList,key=lambda record:record[0])
    return recordList


def getTableFileName(tableName):
    return ''.join([tableName,'.db'])


def testInsert():
    myRange=100
    for i in range(myRange):
        print(insert('student',['{:05d}'.format(i),'{:05d}'.format(myRange-i),'{:05.1f}'.format(i/2)]))


def testSelect():
    print(select('student',['*'],[
    {'field':'no','operand':'=','value':'00010'}
    ]))


def testDelete():
    delete('student',[
    # {'field':'age','operand':'=','value':91}
        ])
    # delete('student',[])


def testInsertAdditional():
    insert('student',['0014','91','104.0'])

if __name__=='__main__':
    # createTable('student')
    # testInsertAdditional()
    testDelete()
    testInsert()
    testSelect()
    # testInsert()
    indexManager.closeIndices()
    bufferManager.saveAll()

