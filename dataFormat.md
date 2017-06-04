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
  ]
}
```



### Insert - Data Format

```json
{
  table: 'table1',
  
}
```





### Table - Data Format





### Query Result Data Format

```json
{
  status: 'success' | 'error',
  payload: ''
}
```





