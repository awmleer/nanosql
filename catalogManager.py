"""
Question: how to control the behavior when the we need to change the next block (when space of current block is not enough)
"""
import bufferManager
"""
bytes to string : btyes.decode()
string to bytes: str.encode()
len(str)
"""
"""
todo:
is "No" necessary in this module?YES
YES it is useful when we try to delete one table (use No to locate the index of that table....)
So add No. to where it should be
"""
class catalogManager(object):
    """docstring for catalogManager."""
    tablesBlockList=[]#blocks of str type
    tablesInfo={}#{tableName:[No,numOfColumns,primaryKeyName,{columnName:[type,unique,index]}]}
    indicesBlockList=[]
    indicesInfo={}#{indexName:[No, tableName,columnName]}
    numOfTables=0
    numOfIndices=0
    def __init__(self):
        """
        file format of recordCatalog.txt:
        (totalLength:5+4*(numOfColumns))
        [0]:No.
        [1]:bool validation,# set when deleted
        [2]:str tableName,
        [3]:int numOfColumns,
        [4]:str primaryKeyName;
        [5+4*i]str columnName+type+unique?+index?[numOfColumns],
        """
        #initialize self.tablesBlockList
        self.openCatelog()
        i=0
        length=len(self.tablesBlockList)
        # initialize self.tablesInfo
        while i<length:
            numOfColumns=int(self.tablesBlockList[i+3])
            temp=self.tableListToDictValue(self.tablesBlockList[i:i+5+4*numOfColumns])
            if temp is None:
                i+=(5+4*numOfColumns)
            else:
                self.tablesInfo[self.tablesBlockList[i+2]]=temp
                i+=(5+4*numOfColumns)
                self.numOfTables+=1
        # initialize self.indicesBlockList
        """
        file format of indexCatalog.txt:
        [0]:int No,
        [1]:bool validation,
        [2]:str indexName,
        [3]:str tableName,
        [4]:str columnName;
        """
        i=0
        length=len(self.indicesBlockList)
        # initialize self.indicesInfo
        while i<length:
            temp=indexListToDictValue(self.indicesBlockList[i:i+5])
            if temp is None:
                i+=5
            else:
                self.indicesInfo[self.indicesBlockList[i+2]]=temp#No,tableName,columnName
                i+=5
                self.numOfIndices+=1
        return
    def openCatelog(self):
        try:
            f=open("tableCatalog.txt",'r+')
            self.tablesBlockList=f.read().split()
            f.close()
        except IOError:
            pass
        try:
            f=open("indexCatalog.txt",'r+')
            self.indicesBlockList=f.read().split()
            f.close()
        except IOError:
            pass
        return
    def closeCatelog(self):
        f=open("tableCatalog.txt",'w')
        f.write(' '.join(self.tablesBlockList))
        f.close()
        f=open("indexCatalog.txt",'w')
        f.write(' '.join(self.indicesBlockList))
        f.close()
        return
    def tableListToDictValue(self,data):
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
    def indexListToDictValue(self,data):
        validation=bool(data[1])
        if not validation:
            return None
        else:
            return [int(data[0]),data[3],data[4]]#No,tableName,columnName
    def tableDictToStr(self,tableName,tableInfoValue):
        numOfColumns=tableInfoValue[1]
        table1=[str(tableInfoValue[0]),'1',tableName,str(numOfColumns),tableInfoValue[2]]
        table2=[]
        for key,value in dict.items(tableInfoValue[3]):
            table2+=([key,str(value[0]),str(value[1]),str(value[2])])
        return table1+table2
    def createTable(self,tableName, primaryKeyName, columnMap):
        """
        :param tableName:
        :param primaryKeyName:
        :param columnMap:{columnName:[int(type),bool(unique)]}(type: -1:int,0:float,1~255:char(1~255))
        :return:successful or not
        this function should record
            the tableName,
            number of columns,
            name & type of columns,
            primary key,
            unique key,
            the name of column that has index & indexName
        """
        # add to dict
        # dict merge
        for key in columnMap:
            columnMap[key].append(False)
        self.tablesInfo[tableName]=[self.numOfTables,len(columnMap),primaryKeyName,columnMap]
        self.numOfTables+=1
        # add to file
        self.tablesBlockList+=self.tableDictToStr(tableName,self.tablesInfo[tableName])
        # write list
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
        :return: {tableName:xxx,No:xxx,numOfColumns:xxx,etc}

        give tableName, return the information of the table
        """
        if(tableName in self.tablesInfo):
            infoList=self.tablesInfo[tableName]
            return {'tableName':tableName,'No':infoList[0],'numOfColumns':infoList[1],\
            'column':infoList[3],'primaryKeyName':infoList[2]}
        else:
            return None
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
# DEBUG
if __name__=='__main__':
    a=catalogManager()
    tableName='ha'
    primaryKeyName='id'
    columnMap={
    'id':[10,True],# char(20) unique
    'name':[20,False],# char(20) not unique
    'age':[-1,False]# int not unique
    }
    a.createTable(tableName,primaryKeyName,columnMap)
    print(a.tablesBlockList,a.tablesInfo)
    a.closeCatelog()
