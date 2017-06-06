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
"""
def strToBytes(string,size):
    by = str.encode(string)
    by += b"0" * (size - len(by))
    return by

def pack(tableName,valueList, fieldsList):
    i=0
    # add No at first, add validation at second
    bytesList=[struct.pack('i',countRecord(tableName)),struct.pack('?',1)]
    for field in fieldsList:
        if(field['type']=='int'):
            bytesList.append(struct.pack('i', int(valueList[i])))
        elif(field['type']=='float'):
            bytesList.append(struct.pack('f', float(valueList[i])))
        else:
            bytesList.append(strToBytes(valueList[i],field['typeParam']))
        i+=1
    return bytesList
def unpack(bytesList,fieldsList):
    i=0
    # if valid
    if not struct.unpack('?',bytesList[1]):
        return []
    # ignore 'No' at first
    bytesList=bytesList[2:]
    for field in fieldsList:
        if(field['type']=='int'):
            valueList.append(struct.unpack('i', bytesList[i])[0])
        elif(field['type']=='float'):
            valueList.append(struct.unpack('f', bytesList[i])[0])
        else:
            valueList.append(bytes.decode(bytesList[i]))
        i+=1
    return valueList
def countRecord(tableName):
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
    return True
def dropTable(tableName):
    #
    return True
def insertValues(tableName, valueList):
    fileName=getTableFileName(tableName)
    if not catalogManager.exist(tableName):
        return {  'status':'error','payload': 'table does not exist'}
    for item in valueList:
        # find unique(include primaryKey)(traverse all column) duplicated?
        pass
    fieldsList=catalogManager.getFieldsList()
    bytesRecord=b''.join(pack(valueList,fieldsList))
    # append the the last
    blockCount=bufferManager.blockCount(fileName)
    lastBlock=bufferManager.read(fileName,blockCount-1,cache=True)
    size=catalogManager.getTableSize(tableName)
    freeSpace=bufferManager.BLOCK_SIZE-len(lastBlock)
    if freeSpace>=size:
        #append to current blockBuffer
        bufferManager.write(fileName,blockCount-1,b''.join([lastBlock,bytesRecord]))
    else:
        #append to next blockBuffer
        bufferManager.write(fileName,blockCount,bytesRecord,cache=True)
    return return {  'status':'success','payload': ''}
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
if __name__=='__main__':
    # createTable('student')
    valueList=['123','123','123']
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
    print(unpack(pack(valueList,fieldsList),fieldsList))
