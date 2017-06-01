import io,math

fileList={}
bufferList={}

BLOCK_SIZE=4096
MAX_BUFFER_AMOUNT=64

def openFile(filePath):
    f=open(filePath,'ab+')
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




def read(filePath,blockPosition,cache=False):
    if cache:
        if (filePath in bufferList) and (blockPosition in bufferList[filePath]):
            return bufferList[filePath][blockPosition]
    f=getFile(filePath)
    f.seek(blockPosition*BLOCK_SIZE,io.SEEK_SET)
    data=f.read(BLOCK_SIZE)
    if cache:
        if filePath not in bufferList:
            bufferList[filePath]={}
        bufferList[filePath][blockPosition]={
            'consistent':True,
            'data':data
        }
    return data #bytes


def write(filePath,blockPosition,data,cache=False):
    if cache:
        if filePath not in bufferList:
            bufferList[filePath]={}
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
        f.write(data)  # type of content is 'bytes'



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
        if blockBuffer['consistent']:
            continue
        f.seek(position,io.SEEK_SET)
        f.write(blockBuffer['data'])


def saveAll():
    for filePath in bufferList:
        save(filePath)


# just for DEBUG
if __name__=='__main__':
    print(blockCount('test.txt'))
    # f=openFile('test.txt')
    # f.seek(100,io.SEEK_END)
    # print(f.read())
    # print(f.tell())
    # write('test.txt',0,b'awmleer')
    closeAllFiles()



