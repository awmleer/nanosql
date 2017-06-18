## Catalog Manager
### 总述
Catalog Manager 负责管理数据库的所有模式信息，包括：
1. 数据库中所有表的定义信息，包括名称、字段（列）主键在该上索引。
2. 表中每个字段的定义信息，包括类型、是否唯 一等。
3. 数据库中所有索引的定义，包括属表、建立在哪个字段上等。
Catalog Manager还必需提供 访问及操作上述信息的接口，Interpreter和API
形象的说，catalogManager是recordManager和indexManager的指挥员，后二者的操作总是要先从本模块中获取相应信息之后才可以正常进行。
### 主要功能接口
#### `createTable`
- 本函数被调用于create table语句之中，其具体作用是创建表的定义信息。并保存于`tablesInfo`之中。
- 传入参数：
  - 表名
  - 主键名
  - 字段信息
    - 字段名
    - 字段类型
    - 字段参数(字段长度，仅适用于`char`类型)
    - 是否`unique`
- 返回结果
  - 创建成功与否
#### `dropTable`
- 本函数被调用于drop table语句之中，其具体作用是在`tablesInfo`变量中删除该表的信息。
- 传入参数：
  - 表名
- 返回结果
  - 删除成功与否
#### `createIndex`
- 本函数被调用于create index语句之中，其具体作用是创建某一个表的某一个字段上的index的定义信息。并保存于`indicesInfo`之中。
- 传入参数：
  - 索引名
  - 表名
  - 字段序号
- 返回结果
  - 创建成功与否
#### `dropIndex`
- 本函数被调用于drop index语句之中，其具体作用是在`indicesInfo`变量中删除该表的信息。
- 传入参数：
  - 索引名
- 返回结果
  - 删除成功与否
### 数据结构
#### `tablesInfo`
- 本结构存储所有表的定义信息，每次程序启动之时从文件读至内存之中，以python字典的形式存于内存之中
- 每次程序结束之时保存于文件之中，在文件之中以json格式存储
- 结构说明
```python
{
  tableName: {
    'primaryKey': ,#主键名称,
    'size': ,#表的大小，单位为byte
    'fields':[
      'name': ,#字段名
      'type': ,#类型
      'typeParam': ,#'char'类型的长度
      'unique': ,#是否unique
      'index': #index的名字(如果有)
    ]
  }
}
```
#### `indicesInfo`
- 本结构存储所有索引的定义信息，每次程序启动之时从文件读至内存之中，以python字典的形式存于内存之中
- 每次程序结束之时保存于文件之中，在文件之中以json格式存储
- 结构说明
```python
{
  indexName: [
    tableName,#表名
    columnNo#字段序号
  ]

}
```
### 实现思路及算法
#### 功能类函数
##### `createTable`
- 基本思路是将传入的信息保存在`tablesInfo`变量之中
- 但是由于我们需要额外附加某些信息，而这些信息没有传入，需要通过计算。我们需要将传入的数据进行扩展，主要包括
  - 表的大小
    - 通过此变量，（由于我们采用的是定长存储策略）我们可以**不需遍历表的每一列信息就可以迅速定位到某一行在文件之中的位置**以及**迅速计算出当前的block是否有足够的剩余空间来存储表中插入的下一列内容**
    - 表的大小的计算方法如下（数据的详细存储方式请参见record manager模块的说明）：
      - 首先固定5 bytes的数据，分别保存列序号(no, 4 bytes)和删除标记(validation, 1 byte)
      - `int` 类型为4 bytes
      - `float` 类型为4 bytes
      - `char(n)` 类型为n bytes
    - 表的大小为以上数字之和
    - 通过表的大小来快速定位(时间复杂度为O(1))某一列在文件中的位置的方法在record manager模块中有详细说明
  - 每一个字段的index信息（即index名）。新表创建时默认设置所有index为 `None` type.
- 扩展之后，我们将以上的数据以`tablesInfo`所规定的结构存储，返回成功信息
##### `dropTable`
- 基本思路是将某一个表的信息从`tablesInfo`内删除
- 通过python `dict.pop()`函数我们可以方便的删除某一个表的信息，然后返回成功信息
##### `createIndex`
- 基本思路是将传入的index信息保存至`indicesInfo`变量中
- 同时额外需要将`tablesInfo`中的对应表的对应字段的`index`信息修改为该index的名称，以完成数据的统一
##### `dropIndex`
- 基本思路是将某个index从`indicesInfo`变量中删除(通过python `dict.pop()`函数)
- 同时额外需要将`tablesInfo`中的对应表的对应字段的`index`信息修改为`None`，以完成数据的统一
#### 信息查询类函数
以下函数供其他模块(如record manager, index manager, API)调用以获取相应信息
##### `findTable`
- 输入表名，作用是返回某一个表的完整信息，包括表的定义，大小，字段的定义，主键，索引等
- 实现方法为python `dict[]` 方法，内部实现采用了hash table的方法
- 如果该表不存在返回None
##### `existTable`
- 输入表名，作用是判断某一个表是否存在
- 返回值类型为bool type
##### `getTableNames`
- 无输入参数，作用是返回所有表的名称
- 实现方法为遍历`tablesInfo`，将所有key存入一个数组，返回该数组
##### `existIndex`
- 输入索引名，作用是判断某一个索引是否存在
- 返回值类型为bool type
##### `getIndexName`
- 输入表名+字段序号，返回该字段上的索引名
- 实现方法为通过`dict[]`方法查找到该表的信息，再通过字段数组的下标，定位到该字段的信息，查找该字段上的索引名
- 如果该字段上无索引，则返回None
##### `getTableAndColumnNo`
- 输入索引名，返回该索引所在的表名以及字段序号
- 实现方法为直接通过`dict[]`方法找到该index的信息，然后返回所需数据
##### `getFieldsList`
- 输入表名，返回该表上的所有字段信息
- 实现方法也为`dict[]`，结果以list的格式返回
##### `getTableSize`
- 输入表名，返回该表的一行内容在内存中（也等于在磁盘中）所占的空间大小，单位为 bytes
- 实现方法也为`dict[]`，结果以int type返回
##### `getIndexList`
- 输入表名，返回在该表上的所有索引信息
- 实现方法为遍历`indicesInfo`，如果该索引建立在该表上，则保存于list之中
- 返回结果格式为二维数组，其中每一列为[索引名,表名,字段(列)序号]
##### `getFieldNumber`
- 输入表名+字段名，返回该字段在该表之中的序号
- 实现方法为遍历`tablesInfo`，查找该字段
- 返回格式为int type
