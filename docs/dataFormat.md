# Data Format Documentation



### Query Data Format

```json
{
  operation: 'select' | 'insert' | 'delete' | 'createTable' ...
  data:<Operation Data>
}
```





### Create Table - Data Format

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



### Drop Table - Data Format

```json
{
  tableName
}
```





### Select - Data Format

```json
{
  fields: ['field1', 'field2', '*'],
  from: 'table1',
  orderBy: None | 'fieldName', //None means no need to order
  limit: 42 // a non-negative, 0 means no need to limit
  where:[
    {
      field: 'field1',
      operand: '=' | '<>' | '<' | '>' | '<=' | '>=',
      value: 'string' | 42
    }
  ] //note: array can be empty, like: []
}
```



### Insert - Data Format

```json
{
  tableName: 'table1',
  values:[]
}
```





### Delete - Data Format

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





### Create Index - Data Format

```json
{
  indexName,
  tableName,
  fieldName
}
```





### Drop Index - Data Format

```json
{
  indexName
}
```





### Query Result Data Format

```json
{
  status: 'success' | 'error',
  payload: ...
}
```





