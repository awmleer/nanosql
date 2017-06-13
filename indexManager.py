from BPlusTree import *
import bufferManager
import catalogManager
import recordManager
import pickle
"""
todo:
add a new index when inserting a record 
todo:

What if this record is not valid?!!!!!
"""
ORDER=4
forest={}
def openIndices():
    global forest
    for key in (catalogManager.indicesInfo):# for each indexName
        with open(getIndexFileName(key),'rb') as fp:
         try:
	         newList=(pickle.load(fp))
	         forest[key]=BPlusTree.bulkload(newList,ORDER)
         except EOFError:
	         forest[key]=BPlusTree(ORDER)
def closeIndices():
    # save forest to file
    for key,value in dict.items(forest):
        with open(getIndexFileName(key),'wb') as fp:
            pickle.dump(value.items(),fp)
def insertIndex(indexName,value,no):
	"""
	the type must be correct
	"""
	forest[indexName].insert(value,no)
	return
def createIndex(indexName, tableName, columnName):
    global forest
    """
    create index on `key` in `tableName`
    e.g. create index stunameidx on student ( sname );
    """
    # establish B+Tree in Memory
    forest[indexName]=BPlusTree.bulkload(recordManager.selectWithNo(tableName,columnName),ORDER)
    return True
def select(indexName,value):
    tableName,columnNo=catalogManager.getTableAndColumnName(indexName)
    # single value
    No=forest[indexName][value]
    if No is None:
        return []
    else:
        # What if this record is not valid?!!!!!
        blockNo,blockPosition=NoToBlockNoAndPosition(tableName,No)
        tableSize=catalogManager.getTableSize(tableName)
        fileName=getTableFileName(tableName)
        blockContent=bufferManager.read(fileName,blockNo,cache=True)
        return recordManager.unpack(blockContent[blockPosition:blockPosition+tableSize],catalogManager.getFieldsList(tableName))
def dropIndex(indexName):
    """
    delete an index
    e.g. drop index stunameidx;
    """
    forest.pop(indexName)
    return True
def NoToBlockNoAndPosition(tableName,No):
    tableSize=catalogManager.getTableSize(tableName)
    BLOCK_SIZE=bufferManager.BLOCK_SIZE
    return (No*tableSize//BLOCK_SIZE,No*tableSize%BLOCK_SIZE)
def getIndexFileName(indexName):
    return ''.join(['index_',indexName,'.txt'])
def getTableFileName(tableName):
    return ''.join([tableName,'.txt'])

def testCreateIndex():
    createIndex('idx_student','student','no')
    createIndex('idx_age','student','age')
def testCloseIndex():
    closeIndices()
def testSelect():
    print(select('idx_age',91))
def testDropIndex():
    dropIndex('idx_age')# must be accompanied with drop catalog!!!
def showAllIndex():
	for key,value in dict.items(forest):
		print(key,": ",value.items())
openIndices()
if __name__=='__main__':
    # testCreateIndex()# seems work fine
    testSelect()# seems work fine
    # testDropIndex()
    # showAllIndex()
    testCloseIndex()# seems work fine