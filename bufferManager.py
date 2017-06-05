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
        return bufferList[filePath][blockPosition]
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
        print(f.tell())
        f.write(data)  # type of data is 'bytes'


def delete(filePath):
    save(filePath)
    del bufferList[filePath]
    os.remove(filePath)



def blockCount(filePath):
    f=getFile(filePath)
    f.seek(0,io.SEEK_END)
    return math.ceil(f.tell()/BLOCK_SIZE)


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
    # print(blockCount('test.txt'))
    write('test.txt',0,b'lorem',True)
    saveAll()
    read('test.txt',1)
    # f=openFile('test.txt')
    # f.seek(100,io.SEEK_END)
    # print(f.read())
    # print(f.tell())
    # write('test.txt',0,b'awmleer')
    closeAllFiles()



