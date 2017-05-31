# Data Format Documentation



### Query Data Format

```json
{
  operation: 'select' | 'insert' | 'delete' | ...
  data:<Operation Data>
}
```







### Select Operation Data Format

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



### Insert Operation Data Format

```json
{
  table: 'table1',
  
}
```





### Table Operation Data Format





### Query Result Data Format

```json
{
  status: 'success' | 'error',
  payload: ''
}
```





