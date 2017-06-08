"""
Question: how to control the behavior when the we need to change the next block (when space of current block is not enough)
"""
import bufferManager
import struct
import catalogManager
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
when we encode a str to bytes that len is not enought, we use b'0' to 占位,
But how could be decode this bytes to str?
str.strip('\x00')
"""
def strToBytes(string,size):
    by = str.encode(string)
    by += b"\x00" * (size - len(by))
    return by
def pack(tableName,recordList, fieldsList):
    i=0
    # add No at first, add validation at second
    bytesList=[struct.pack('i',countRecord(tableName)),struct.pack('?',1)]
    for field in fieldsList:
        if(field['type']=='int'):
            bytesList.append(struct.pack('i', int(recordList[i])))
        elif(field['type']=='float'):
            bytesList.append(struct.pack('f', float(recordList[i])))
        else:
            bytesList.append(strToBytes(recordList[i],field['typeParam']))
        i+=1
    return bytesList
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
    lastBlock=bufferManager.read(fileName,blockCount-1,cache=False)
    return count+math.ceil(len(lastBlock)/size)
def createTable(tableName):
    #find whether exist????
    if catalogManager.exist(tableName):
        return {  'status':'error','payload': 'table already exists'}
    fileName=getTableFileName(tableName)
    bufferManager.write(fileName,0,b'',cache=False)
    return {  'status':'success','payload': ''}
def dropTable(tableName):
    bufferManager.delete(getTableFileName(tableName))
    return True
def insertValues(tableName, recordList):
    fileName=getTableFileName(tableName)
    if not catalogManager.exist(tableName):
        return {  'status':'error','payload': 'table does not exist'}
    for item in recordList:
        # find unique(include primaryKey)(traverse all column) duplicated?
        pass
    fieldsList=catalogManager.getFieldsList(tableName)
    bytesRecord=b''.join(pack(tableName,recordList,fieldsList))
    # append the the last
    blockCount=bufferManager.blockCount(fileName)
    if blockCount==0:
        blockCount=1
    lastBlock=bufferManager.read(fileName,blockCount-1,cache=False)
    size=catalogManager.getTableSize(tableName)
    freeSpace=bufferManager.BLOCK_SIZE-len(lastBlock)
    if freeSpace>=size:
        #append to current blockBuffer
        bufferManager.write(fileName,blockCount-1,b''.join([lastBlock,bytesRecord]),cache=False)
    else:
        #塞入占位符 first
        bufferManager.write(fileName,blockCount-1,b'0'*freeSpace,cache=False)
        #append to next blockBuffer
        bufferManager.write(fileName,blockCount,bytesRecord,cache=False)
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
        blockContent=bufferManager.read(fileName,blockNo,cache=False)
        ba=bytearray(blockContent)
        # divide this blockContent into rows
        rows=len(blockContent)//size
        for i in range(rows):
            oneRecord=unpack(blockContent[i*size:(i+1)*size],catalogManager.getFieldsList(tableName))
            if(oneRecord==[]):# deleted before
                continue
            flag=True
            for condition in myWhere:
                if not (eval(''.join([str(oneRecord[condition['field']]),condition['operand'],str(condition['value'])]))):
                    flag=False
                    break
            if flag:
                # i think i should change validation bit directly
                ba[i*size+4]=0
                count+=1
        bufferManager.write(fileName,blockNo,bytes(ba),cache=False)
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
    fileName=getTableFileName(tableName)
    blockCount=bufferManager.blockCount(fileName)
    size=catalogManager.getTableSize(tableName)
    recordList=[]
    if(where==[]):
        # select all!!!!!
        myWhere=[]
    else:
        print(where)
        myWhere=convertInWhere(tableName,where)
    myFields=[]
    if(fields==['*']):
        myFields=['*']
    else:
        for item in fields:
            myFields.append(fieldsNameTofieldsNo(tableName,item))
    for blockNo in range(blockCount):
        # this is a copy
        blockContent=bufferManager.read(fileName,blockNo,cache=False)
        # divide this block into rows
        rows=len(blockContent)//size
        for i in range(rows):
            oneRecord=unpack(blockContent[i*size:(i+1)*size],catalogManager.getFieldsList(tableName))
            if(oneRecord==[]):
                continue
            flag=True
            for condition in myWhere:
                if not (eval(''.join([str(oneRecord[condition['field']]),condition['operand'],str(condition['value'])]))):
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
def getTableFileName(tableName):
    return ''.join([tableName,'.txt'])
if __name__=='__main__':
    # createTable('student')
    print(insertValues('student',['0000','90','19.0']))
    print(select('student',['*'],[{'field':'age','operand':'=','value':20}]))
    print(delete('student',[]))
