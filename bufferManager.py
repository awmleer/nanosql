import io,math,random,os

fileList={}
bufferList={}

BLOCK_SIZE=4096
MAX_BUFFER_AMOUNT=64


def openFile(filePath):
    f=open(filePath,'ab')
    f.close()
    f=open(filePath,'rb+')
    fileList[filePath]=f
    return f


def closeAllFiles():
    for key in fileList:
        fileList[key].close()


def getFile(filePath):
    if filePath in fileList:
        return fileList[filePath]
    else:
        return openFile(filePath)


def freeBuffer(filePath):
    keys=list(bufferList[filePath].keys())
    if len(keys)==0: return
    i=random.randint(0,len(keys))
    del bufferList[filePath][keys[i]]
def read(filePath,blockPosition,cache=False):
    if (filePath in bufferList) and (blockPosition in bufferList[filePath]):
        return bufferList[filePath][blockPosition]['data']
    f=getFile(filePath)
    f.seek(blockPosition*BLOCK_SIZE,io.SEEK_SET)
    data=f.read(BLOCK_SIZE)
    if cache:
        if filePath not in bufferList:
            bufferList[filePath]={}
        if (blockPosition not in bufferList[filePath]) and (len(bufferList[filePath])>=MAX_BUFFER_AMOUNT): #need to add a bufferBlock but the the amount reaches the MAX value
            freeBuffer(filePath)
        bufferList[filePath][blockPosition]={
            'consistent':True,
            'data':data
        }
    return data #bytes


def write(filePath,blockPosition,data,cache=False):
    if cache:
        if filePath not in bufferList:
            bufferList[filePath]={}
        if (blockPosition not in bufferList[filePath]) and (len(bufferList[filePath])>=MAX_BUFFER_AMOUNT): #need to add a bufferBlock but the the amount reaches the MAX value
            freeBuffer(filePath)
        bufferList[filePath][blockPosition]={
            'consistent':False,
            'data':data
        }
    else:
        if (filePath in bufferList) and (blockPosition in bufferList[filePath]):
            del bufferList[filePath][blockPosition]
        f = getFile(filePath)
        f.seek(blockPosition * BLOCK_SIZE, io.SEEK_SET)
        f.write(data)  # type of data is 'bytes'


def delete(filePath):
    save(filePath)
    if filePath in bufferList:
        del bufferList[filePath]
    os.remove(filePath)



def blockCount(filePath):
    f=getFile(filePath)
    f.seek(0,io.SEEK_END)
    count=math.ceil(f.tell()/BLOCK_SIZE)
    if filePath in bufferList:
        for position in bufferList[filePath]:
            if position>=count: count=position+1
    return count


def save(filePath):
    if filePath not in bufferList:
        return
    f=getFile(filePath)
    for position in bufferList[filePath]:
        blockBuffer=bufferList[filePath][position]
        if not blockBuffer['consistent']:
            f.seek(int(position)*BLOCK_SIZE,io.SEEK_SET)
            f.write(blockBuffer['data'])


def saveAll():
    for filePath in bufferList:
        save(filePath)


# just for DEBUG
if __name__=='__main__':
    # print(blockCount('test.db'))
    # write('test.db',2,b'lorem',True)
    print(blockCount('db/test.db'))
    # saveAll()
    # read('test.db',1)
    # f=openFile('test.db')
    # f.seek(100,io.SEEK_END)
    # print(f.read())
    # print(f.tell())
    # write('test.db',0,b'awmleer')
    closeAllFiles()



