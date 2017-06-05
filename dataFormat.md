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
        { maxLength: <int> } //for char type
        None, //for other types
      unique: <boolean>
  }],
  primaryKey
}
```



### Drop Tabel - Data Format

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
  where:[
    {
      field: 'field1',
      operand: '=' | '<>' | '<' | '>' | '<=' | '>=',
      value: 'string' | 42
    }
  ] or None
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
  tableName,
  where:[
    {
      field: 'field1',
      operand: '=' | '<>' | '<' | '>' | '<=' | '>=',
      value: 'string' | 42
    }
  ] or None//same as SELECT
}
```





### Create Index - Data Format

```json
{
  indexName,
  tableName,
  fieldNames:[]
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
  payload: ''
}
```





