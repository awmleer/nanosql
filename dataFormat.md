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
  fields: ['field1', 'field2'] | None,//None represents for "*"
  from: 'table1',
  where:[
    {
      field: 'field1',
      operator: '=' | '<>' | '<' | '>' | '<=' | '>=',
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





