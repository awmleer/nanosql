import io,math

fileList={}

BLOCK_SIZE=4096


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


def read(filePath,blockPosition):
    f=getFile(filePath)
    f.seek(blockPosition*BLOCK_SIZE,io.SEEK_SET)
    f.read(BLOCK_SIZE)

def write(filePath,blockPosition,content):
    f=getFile(filePath)
    f.seek(blockPosition*BLOCK_SIZE,io.SEEK_SET)
    print(f.tell())
    f.write(content)

def blockCount(filePath):
    f=getFile(filePath)
    f.seek(0,io.SEEK_END)
    return math.ceil(f.tell()/BLOCK_SIZE)



if __name__=='__main__':
    print(blockCount('test.txt'))
    # f=openFile('test.txt')
    # f.seek(100,io.SEEK_END)
    # print(f.read())
    # print(f.tell())
    # write('test.txt',0,b'awmleer')
    closeAllFiles()



