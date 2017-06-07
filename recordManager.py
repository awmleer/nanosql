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
is it a good choice to use pack() to add 'No' directly?
maybe....

remember to read 占位符 at the end of each block
"""
def strToBytes(string,size):
    by = str.encode(string)
    by += b"0" * (size - len(by))
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

    # if valid
    if not struct.unpack('?',bytesRecord[4]):
        return []
    # ignore 'No' at first
    bytesRecord=bytesRecord[5:]
    for field in fieldsList:
        if(field['type']=='int'):
            recordList.append(struct.unpack('i', bytesRecord[i])[0])
            i+=4
        elif(field['type']=='float'):
            recordList.append(struct.unpack('f', bytesRecord[i])[0])
            i+=4
        else:
            string=bytes.decode(bytesRecord[i])
            recordList.append(string)
            i+=len(string)
    return recordList
def countRecord(tableName):
    """
    return the total Record of this table (including deleted )
    """
    size=catalogManager.getTableSize(tableName)
    fileName=getTableFileName(tableName)
    blockCount=bufferManager.blockCount(fileName)
    count=(blockCount-1)*math.floor(bufferManager.BLOCK_SIZE/size)
    lastBlock=bufferManager.read(fileName,blockCount-1,cache=True)
    return count+len(lastBlock)/size
def createTable(tableName):
    #find whether exist????
    if catalogManager.exist(tableName):
        return {  'status':'error','payload': 'table already exists'}
    fileName=getTableFileName(tableName)
    bufferManager.write(fileName,0,(10086).to_bytes(4, byteorder='big'),cache=False)
    a=bufferManager.read(fileName,0)
    print(len(a))
    b=int.from_bytes(a, byteorder='big')
    print(b)
    bufferManager.save(fileName)
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
    fieldsList=catalogManager.getFieldsList()
    bytesRecord=b''.join(pack(recordList,fieldsList))
    # append the the last
    blockCount=bufferManager.blockCount(fileName)
    lastBlock=bufferManager.read(fileName,blockCount-1,cache=True)
    size=catalogManager.getTableSize(tableName)
    freeSpace=bufferManager.BLOCK_SIZE-len(lastBlock)
    if freeSpace>=size:
        #append to current blockBuffer
        bufferManager.write(fileName,blockCount-1,b''.join([lastBlock,bytesRecord]),cache=True)
    else:
        #塞入占位符 first
        bufferManager.write(fileName,blockCount-1,b'0'*freeSpace,cache=True)
        #append to next blockBuffer
        bufferManager.write(fileName,blockCount,bytesRecord,cache=True)
    return return {  'status':'success','payload': ''}
def delete(tableName,where):
    # get each rows
    # satisfy conditions?
    fileName=getTableFileName(fileName)
    blockCount=bufferManager.blockCount(fileName)
    size=catalogManager.getTableSize(tableName)
    recordList=[]
    count=0
    if where=[]:
        #delete all
        for block in range(blockCount):
            blockContent=bufferManager.read(fileName,blockNo,cache=True)
            ba=bytearray(blockContent)
            rows=len(blockContent)//size
            for i in range(rows):
                # how to manipulate bytes object
                ba[i*size+4]=0
                count+=1
            #no need to append 占位符 at last
            bufferManager.write(fileName,blockNo,byte(ba),cache=True)
        return count
    # if condition is not empty
    myWhere=convertInWhere(where)
    for blockNo in range(blockCount):
        # this is a copy
        blockContent=bufferManager.read(fileName,blockNo,cache=True)
        ba=bytearray(blockContent)
        # divide this blockContent into rows
        rows=len(blockContent)//size
        flag=True
        for i in range(rows):
            oneRecord=unpack(blockContent[i*size:(i+1)*size])
            if(oneRecord==[]):# deleted before
                continue
            for condition in myWhere:
                if not (eval(''.join([oneRecord[condition['field']],condition['operand'],condition['value']]))):
                    flag=False
                    break
            if flag:
                # i think i should change validation bit directly
                ba[i*size+4]=0
                count+=1
        bufferManager.write(fileName,blockNo,byte(ba),cache=True)
    return count
def fieldsNameTofieldsNo(fieldName):
    i=0
    for field in catalogManager.getFieldsList():
        if field['name']==fieldName:
            return i
        else:
            i+=1
def convertInWhere(where):
    for condition in where:
        condition['from']=fieldsNameTofieldsNo(condition['from'])
        if(condition['operand']=='<>'):
            condition['operand']='!='
        elif(condition['operand']=='='):
            condition['operand']='=='
    return where
def select(tableName,fields,where):
    """
    select and project
    """
    """
    todo:
    how to convert fields name to fields No?
    """
    # get each rows
    # satisfy conditions?
    fileName=getTableFileName(fileName)
    blockCount=bufferManager.blockCount(fileName)
    size=catalogManager.getTableSize(tableName)
    recordList=[]
    myWhere=convertInWhere(where)
    for blockNo in range(blockCount):
        # this is a copy
        blockContent=bufferManager.read(fileName,blockNo,cache=True)
        # divide this block into rows
        rows=len(blockContent)//size
        flag=True
        for i in range(rows):
            oneRecord=unpack(blockContent[i*size:(i+1)*size])
            for condition in myWhere:
                if not (eval(''.join([oneRecord[condition['field']],condition['operand'],condition['value']]))):
                    flag=False
            if flag:
                #append
                recordList.append(oneRecord)
    return recordList
def getTableFileName(tableName):
    return ''.join([tableName,'.txt'])
if __name__=='__main__':
    # createTable('student')
    recordList=['123','123','123']
    fieldsList=[
    {
    'type':'int',
    'typeParam':None
    },
    {
    'type':'float',
    'typeParam':None
    },
    {
    'type':'char',
    'typeParam':10
    }
    ]
    print(unpack(pack(recordList,fieldsList),fieldsList))
