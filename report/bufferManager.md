## Buffer Manager

### 总述

bufferManager模块不仅仅是实现了缓存功能，更重要是把对文件的IO操作封装在了一个模块内，使得其他模块不需要自己去处理IO操作，而只需调用bufferManager模块的`read`、`write`、`delete`函数。bufferManager会自动管理缓存，对于其他模块来说，不需要过多的处理缓存问题。

### 常量定义

`BLOCK_SIZE`：表示一个block有多少个字节，默认是4096（4K）

`MAX_BUFFER_AMOUNT`：表示一个文件对应的buffer最多有多少个block，默认是64

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

### bufferList

bufferList用来存储和组织缓存。它是一个**两级的字典**，一级的键是`filePath`，表示文件名（完整的文件路径），二级的键是`blockPosition`，表示的是这个文件的哪个block。

也就是说，根据`filePath`和`blockPosition`，可以获取到一个对应的buffer实例，它有`consistent`和`data`两个键，`data`的类型是`bytes`，存放的是block的**实际内容**，`consistent`的类型是`bool`，用来表示buffer中的这个block的数据和硬盘上对应的数据是否是**一致**的（也可以理解为用来表示buffer的数据是否**dirty**）

下面是一个bufferList的样例：

```python
{
    'db/student.db': {
        12:{
            'data': b'xxxxxxxx',
            'consistent': True
        },
        39:{
            'data': b'xxxxxxxx',
            'consistent': False
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

因此，为了保险起见，在获取buffer的时候，需要先检查f和p是否在bufferList中：

```python
if (filePath in bufferList) and (blockPosition in bufferList[filePath]):
    return bufferList[filePath][blockPosition]['data']
else:
    # handle error
```



