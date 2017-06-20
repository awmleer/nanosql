## Buffer Manager

### 总述

bufferManager模块不仅仅是实现了缓存功能，更重要是把对文件的IO操作封装在了一个模块内，使得其他模块不需要自己去处理IO操作，而只需调用bufferManager模块的`read`、`write`、`delete`函数。bufferManager会自动管理缓存，对于其他模块来说，不需要过多的处理缓存问题。

### 常量定义

`BLOCK_SIZE`：表示一个block有多少个字节，默认是4096（4K）

`MAX_BUFFER_AMOUNT`：表示一个文件对应的buffer最多有多少个block，默认是256

### fileList

fileList是一个字典，用来记录所有打开了的文件的信息，下面是一个fileList的样例：

```python
{
    'db/student.db': <FileObject>,
    'db/index_name.db': <FileObject>,
    ...
}
```

之所以采用了**字典**来存储这些信息，而不是使用**数组**（Python中也称列表），是因为我们需要频繁的做“**根据file的名字获取到对应的fileObject**”这种操作，如果使用数组，需要遍历整个数组才能检索到想要的fileObject，这是十分低效的，而Python的字典本质上就是一张**哈希表**，做这种**键值查询**是非常快的。

一个文件，在打开后，是默认不会自动关闭的，而是直到**程序退出**的时候才统一进行关闭，这是为了避免频繁的文件open/close操作。

### bufferList

bufferList用来存储和组织缓存。它是一个**两级的字典**，一级的键是`filePath`，表示文件名（完整的文件路径），二级的键是`blockPosition`，表示的是这个文件的哪个block。

也就是说，根据`filePath`和`blockPosition`，可以获取到一个对应的buffer实例，它有`consistent`、`pinned`和`data`三个键，`data`的类型是`bytes`，存放的是block的**实际内容**，`consistent`的类型是`bool`，用来表示buffer中的这个block的数据和硬盘上对应的数据是否是**一致**的（也可以理解为用来表示buffer的数据是否**dirty**），`pinned`的类型也是`bool`，用来表示这块buffer是否是被锁定的。

下面是一个bufferList的样例：

```python
{
    'db/student.db': {
        12:{
            'data': b'xxxxxxxx',
            'consistent': True,
            'pinned': False
        },
        39:{
            'data': b'xxxxxxxx',
            'consistent': False,
            'pinned': False
        },
        ...
    },
    'db/index_name.db': {
        ...
    },
    ...
}
```

如果想获取名为`f`的文件的位置为`p`对应的buffer，只需`bufferList[f][p]`即可。

如果文件`f`在`bufferList`中，但是`p`并不在`bufferList[f]`中，那么调用`bufferList[f][p]`会得到`None`，但是，如果文件`f`并不存在`bufferList`中，则会出现错误，因为`bufferList[f]`已经是`None`了，此时`bufferList[f][p]`就成了`None[p]`。

因此，为了保险起见，在获取buffer的时候，需要先**检查f和p是否在bufferList中**：

```python
if (filePath in bufferList) and (blockPosition in bufferList[filePath]):
    return bufferList[filePath][blockPosition]['data']
else:
    # handle error
```

### openFile

函数openFile的作用是，打开文件，并且把它加入到fileList中。

```python
def openFile(filePath):
    f=open(filePath,'ab')
    f.close()
    f=open(filePath,'rb+')
    fileList[filePath]=f
    return f
```

之所以先用`ab`模式打开了文件又关闭掉，是因为在用`rb+`方式打开时，如果文件不存在，并**不会自动创建**，而是会报错。经过一段时间的研究，我们发现，上面的解决方法已经是相对比较优雅的做法了。

### getFile

参数：`filePath`

返回file的对象，如果`filePath`在`fileList`中不存在对应的文件对象，则自动打开这个文件。

### closeAllFiles

关闭所有的文件

### read

参数：`filePath`  `blockPosition`  `cache=False`

返回指定文件的指定block的数据（bytes类型）。

是否需要缓存由`cache`参数控制，默认是`False`。

如果buffer的数量达到了预设的上限，则会先调用`freeBuffer`，释放一个buffer：

```python
if (blockPosition not in bufferList[filePath]) and (len(bufferList[filePath])>=MAX_BUFFER_AMOUNT):
	freeBuffer(filePath)
```

### write

参数：`filePath`  `blockPosition`  `data`  `cache=False`

把`data`的内容写入到指定文件的指定位置或者对应的buffer中（取决`cache`参数）。

如果启用了缓存，则还需要同时把buffer的`consistent`设置为`False`。

### delete

参数：`filePath`

删除文件，同时删除该文件对应的所有缓存。

### pin

参数：`filePath`  `blockPosition`

把指定的buffer标记为`pinned`。

### blockCount

参数：`filePath`

返回文件的大小（以block记）

### freeBuffer

参数：`filePath`

释放一个buffer，采用的替换策略是**Random Replacement**。

相比于LUR和MUR，RR的优势不仅仅在于实现简单，更重要的是，它并不会在buffer的read和write时产生**维护开销**，这使得read和write可以更快速的进行。

我们在设计这个系统时发现，由于buffer开的比较大，实际运行中很少会需要做buffer的释放操作，因此由**加速大概率事件**原理，采用RR替换策略，可以完全去除掉buffer访问频度的统计开销，从而实现更快的IO操作。

### save

参数：`filePath`

把该文件对应的所有buffer中，`consistent`为`False`的那些，写回硬盘的文件中。

```python
for position in bufferList[filePath]:
    blockBuffer=bufferList[filePath][position]
    if not blockBuffer['consistent']:
        f.seek(int(position)*BLOCK_SIZE,io.SEEK_SET)
        f.write(blockBuffer['data'])
```

### saveAll

对`bufferList`中的所有文件，依次调用`save`函数。

