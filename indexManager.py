from BPlusTree import *
import bufferManager
import catalogManager
import recordManager
import pickle
import os
"""
todo:
project when select using index
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


def select(indexName,fields,value):
    tableName,columnNo=catalogManager.getTableAndColumnName(indexName)
    # single value
    No=forest[indexName][value]
    if No is None:
        return [[]]
    else:
        blockNo,blockPosition=NoToBlockNoAndPosition(tableName,No)
        tableSize=catalogManager.getTableSize(tableName)
        fileName=getTableFileName(tableName)
        blockContent=bufferManager.read(fileName,blockNo,cache=True)
        try:
            oneRecord=recordManager.unpack(blockContent[blockPosition:blockPosition + tableSize],
                             catalogManager.getFieldsList(tableName))
        except :
            print(blockNo,blockPosition,": ",blockContent)
        # convert field
        myFields = []
        if (fields == ['*']):
            myFields = ['*']
        else:
            for item in fields:
                myFields.append(recordManager.fieldsNameTofieldsNo(tableName, item))
        # project
        newRecord = []
        if (myFields == ['*']):
            newRecord = oneRecord
        else:
            for No in myFields:
                # copy !!!
                newRecord.append(oneRecord[No])
        # append
        return [newRecord]


def dropIndex(indexName):
    """
    delete an index
    e.g. drop index stunameidx;
    """
    forest.pop(indexName)
    os.remove(getIndexFileName(indexName))
    return True


def NoToBlockNoAndPosition(tableName,No):
    tableSize = catalogManager.getTableSize(tableName)
    BLOCK_SIZE = bufferManager.BLOCK_SIZE
    capacityPerBlock=BLOCK_SIZE//tableSize

    a,b=(No // (capacityPerBlock+1),(No  % capacityPerBlock)*tableSize )
    # if (BLOCK_SIZE-b)<tableSize:
    #     a+=1
    #     b=0
    return (a,b)


def getIndexFileName(indexName):
    return ''.join(['index_',indexName,'.db'])


def getTableFileName(tableName):
    return ''.join([tableName,'.db'])


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
    # testSelect()# seems work fine
    # testDropIndex()
    showAllIndex()
    testCloseIndex()# seems work fine