## Data Structure

### table's information (in catalogManager)

相比于从core调用`catalog.createTable()`传进来的table数据结构, 我在本模块又对这个结构进行了扩展,增添了size,index属性

```json
tablesInfo[tableName]={
  'primaryKey':'no',
  'size'*: 21,
  'fields'**:[{
  'name':'student_name',
  'type':'char' | 'int' | 'float',
  'typeParam':None|8,
  'unique':True|False,
  'index'*:'index_on_student_name' | None
  }]
}
```

### index's information (in catalogManager)

```python
indicesInfo[indexName]=[
    tableName,
    columnNo# 第几列
]
```

## Methods

### create table

- call `catalogManager.createTable()`
- call `catalogManager.createIndex()` for every `unique` field
- call `recordManager.createTable()`
- call `indexManager.createIndex()` for every `unique` field

### create index

- call `catalogManager.createIndex()`
- call `indexManager.createIndex()`

### insert

- call `recordManager.insert()`  (which include **detect duplicated unique** values and **update index**)

### select

- call `recordManager.select()` (which will automatically **use index** if it is possible)

### delete

- call `recordManager.delete()` (do not need to take care of the deletion of index because of BUG of BPlusTree)	

### drop index

- call `indexManager.dropIndex()`
- call `calalogManage.dropIndex()`

### drop table

- drop all indices first
- call `recordManager.dropTable()`
- call `catalogManager.dropTable()` 