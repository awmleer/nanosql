## Core

### 总述

core模块是整个NanoSQL系统的**枢纽**，它连接着除了bufferManager以外的所有模块。

core模块的入口点是`execute`函数，它以`command`（SQL语句字符串）为参数，先调用interpreter模块做SQL语句的解析，然后对不同的语句类型做不同的处理，相应去调用底层模块的函数，实现SQL语句所表示的逻辑操作，最后把执行结果返回给shell模块或web模块。

下面列举一下每条语句的**处理逻辑**：

### create table

1. 调用catalogManager查看是否已经存在了名字相同的表，如果是的话直接返回报错。
2. 把主键自动设置为unique。（便于下一步处理）
3. 对所有unique的字段，**自动建立索引**。

>注：之所以会在create table的时候给**所有**unique的字段都**自动建立索引**，是为了加速insert速度，在测试样例中，会先进行1万条数据的insert操作，如果此时不是所有的unique字段都被建立过索引的话，就会速度特别特别慢。因为每一次insert操作，都需要遍历整张表，来确保新插入的数据在原来的表里是不存在的。而如果有索引的话，则不需要遍历整张表，而是只需要在B+树上做一次查询即可，经测试，这会产生**极大**的速度提升。

### insert

1. 判断表是否存在，如果不存在，直接返回报错。
2. 调用recordManager模块的`insert`函数。

### select

1. 判断表是否存在，如果不存在，直接返回报错。
2. 根据catalogManager提供的信息，检查是否每个字段都在表中存在，如果出现**非法字段**，直接返回报错。
3. 把要查询的字段名转成字段的编号。（即，把列的**名字**，转成是**第几列**）
4. 调用recordManager的`select`函数，获取数据。

### create index

1. 判断表是否存在，如果不存在，直接返回报错。
2. 把字段名转成字段编号，如果字段不存在，直接返回报错。
3. 分别调用indexManager的`createIndex`函数和catalogManager的`createIndex`函数，建立索引。

### drop index

1. 判断表是否存在，如果不存在，直接返回报错。
2. 分别调用indexManager的`dropIndex`函数和catalogManager的`dropIndex`函数，删除索引。

### delete

1. 判断表是否存在，如果不存在，直接返回报错。
2. 调用recordManager的`delete`函数。

### drop table

1. 判断表是否存在，如果不存在，直接返回报错。
2. 把这张表对应的所有的索引都drop掉。
3. 调用recordManager的`dropTable`函数，删除表对应的记录。
4. 调用catalogManager的`dropTable`函数，删除表的信息。

### show tables

1. 调用catalogManager的getTableNames函数，获取到所有表的名字。
2. 根据获取到的数据拼接成可以让shell或者web模块直接渲染显示的二维表格字典。

### quit()

quit函数的主要作用是在程序退出时，保存缓存、关闭文件。

因此，程序在退出前，需要先调用quit()函数。