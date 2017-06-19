## Interpreter

### 总述

interpreter模块的主要功能是把输入的SQL语句字符串解析成字典，再返回给core模块。

interpreter模块的核心函数是`interpret`，这也是这个模块的入口点，在这个函数中，首先是把`command`的最前面的空格通过`removeFrontSpaces`函数去除掉，然后再对`command`的最前面的字符进行匹配，从而识别出这条SQL语句是属于哪种命令。然后再根据不同的命令类型，去分别调用不同的解析函数，将命令的各项参数解析出来，放到字典的`data`字段，和`operation`字段合在一起返回给core模块。

最终interpreter返回给core模块的数据格式如下：

```json
{
  operation: 'select' | 'insert' | 'delete' | 'createTable' ...
  data:<Operation Data>
}
```

其中`operation`字段是一个字符串，表示SQL语句的类型，`data`字段是一个Operation Data对象，用来表示SQL语句的具体参数，根据不同的SQL类型，`data`的格式也会有所变化。列举如下：

### Create Table - Operation Data Format

```json
{
  tableName,
  fields:[{
      name,
      type: 'char' | 'int' | 'float',
      typeParam:
        <int> //for char type, means max length
        None, //for other types
      unique: <boolean>
  }],
  primaryKey
}
```

### Drop Table - Operation Data Format

```json
{
  tableName
}
```

### Select - Operation Data Format

```json
{
  fields: ['field1', 'field2', '*'],
  from: 'table1',
  orderBy: None | 'fieldName', //None means no need to order
  limit: None | 42 // a non-negative, 0 means no need to limit
  where:[
    {
      field: 'field1',
      operand: '=' | '<>' | '<' | '>' | '<=' | '>=',
      value: 'string' | 42
    }
  ] //note: array can be empty, like: []
}
```

### Insert - Operation Data Format

```json
{
  tableName: 'table1',
  values:[]
}
```

### Delete - Operation Data Format

```json
{
  from,
  where:[
    {
      field: 'field1',
      operand: '=' | '<>' | '<' | '>' | '<=' | '>=',
      value: 'string' | 42
    }
  ]//same as SELECT
}
```

### Create Index - Operation Data Format

```json
{
  indexName,
  tableName,
  fieldName
}
```

### Drop Index - Operation Data Format

```json
{
  indexName
}
```