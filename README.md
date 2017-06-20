# NanoSQL

![screenshot](./report/photos/screenshot.png)

### Dependencies

- [clint](https://github.com/kennethreitz/clint) 0.5.1
- python 3.5 or 3.6
- flask


### Sample SQLs

```sql
create table student (
  sno char(8),
  sname char(16) unique,
  sage int,
  sgender char (1),
  primary key ( sno )
);
```

```sql
create index stunameidx on student ( sname );
```

```sql
insert into student values ('12345678','wy',22,'M');
```

See more test cases at: `test/sample.txt`
