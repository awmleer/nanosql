import re

def interpret(command):
    command=removeFrontSpaces(command)
    if re.match('^select',command):
        command=re.sub('^select','',command)
        return {
            'operation': 'select',
            'data': parseSelectStatement(command)
        }
    elif re.match('^create +table',command):
        command=re.sub('^create +table','',command)
        return {
            'operation': 'createTable',
            'data': parseCreateTableStatement(command)
        }
    elif re.match('^insert',command):
        return {
            'operation': 'insert',
            'data': parseInsert(command)
        }
    elif re.match('^delete from',command):
        return {
            'operation': 'delete',
            'data': parseDeleteStatement(command)
        }
    elif re.match('^drop table',command):
        return {
            'operation': 'dropTable',
            'data': parseDropTableStatement(command)
        }
    elif re.match('^create index',command):
        return {
            'operation': 'createIndex',
            'data': parseCreateIndexStatement(command)
        }
    elif re.match('^drop index',command):
        return {
            'operation': 'dropIndex',
            'data': parseDropIndexStatement(command)
        }
    else:
        return {
            'operation': 'unknown',
            'data': None
        }



def removeFrontSpaces(text):
    return re.sub('^ +','',text)

def removeRearSpaces(text):
    return re.sub(' +$','',text)

def removeEndsSpaces(text):
    return removeRearSpaces(removeFrontSpaces(text))




def parseCreateTableStatement(command):
    temp=re.split('\(',command,1)
    tableName= removeEndsSpaces(
        re.sub('create +table +','',temp[0])
    )
    rawFieldStrings=re.split(
        ',',
        re.sub('\); *$','',temp[1])
    )
    fields=[]
    primaryKey=None
    for rawFieldString in rawFieldStrings:
        rawFieldString=re.sub(' *,$','',removeEndsSpaces(rawFieldString))
        if re.match('^primary +key',rawFieldString):
            primaryKey=re.sub(
                '\)$',
                '',
                re.sub('primary key \(', '', rawFieldString)
            )
            primaryKey=removeEndsSpaces(primaryKey)
            continue
        temp=re.split(' +',rawFieldString,1)
        field={
            'name':'',
            'type':'',
            'typeParam':None,
            'unique':False
        }
        field['name']=removeEndsSpaces(temp[0])
        if re.match('^char',temp[1]):
            field['type']='char'
            field['typeParam']=re.split(
                '\)',
                re.split('\(', temp[1], 1)[1]
            )[0]
            field['typeParam']=int(field['typeParam'])
        elif re.match('^int',temp[1]):
            field['type']='int'
        elif re.match('^float',temp[1]):
            field['type']='float'
        else:
            return "error"  # TODO raise error: unknown field type: re.split(' +',temp[1])[0]
        if re.search(' unique$',rawFieldString):
            field['unique']=True
        fields.append(field)
    if not primaryKey:
        return "error"  # TODO raise error: no primary key
    return {
        'tableName':tableName,
        'fields':fields,
        'primaryKey':primaryKey
    }



def parseInsert(command):
    temp=re.split(' +values *',command)
    tableName=re.sub(' *insert into *','',temp[0])
    valuesString=re.sub(
        ' *\) *; *','',
        re.sub('\( *','',temp[1])
    )
    rawValues=re.split(',',valuesString)
    values=[]
    for rawValue in rawValues:
        value=re.sub('\' *$','',rawValue)
        value=re.sub('^ *\'','',value)
        values.append(value)
    return {
        'tableName':tableName,
        'values':values
    }



def parseWheres(whereString):
    rawWheres=re.split(' and ',whereString)
    wheres=[]
    for rawWhere in rawWheres:
        operand=''
        if re.search('<>',rawWhere):
            operand='<>'
        elif re.search('>',rawWhere):
            operand='>'
        elif re.search('<',rawWhere):
            operand='<'
        elif re.search('>=',rawWhere):
            operand='>='
        elif re.search('<=',rawWhere):
            operand='<='
        elif re.search('=',rawWhere):
            operand='='
        if operand=='':
            return "error" # TODO raise error
        operators=re.split(operand,rawWhere)
        wheres.append({
            'operand':operand,
            'field':removeEndsSpaces(operators[0]),
            'value':removeEndsSpaces(operators[1])
        })
    return wheres


def parseSelectStatement(command):
    # command=removeFrontSpaces(command)
    command=re.sub(' *;$','',command)
    strings=re.split(' from ',command)
    fieldString=strings[0]
    strings=re.split(' where ',strings[1])
    fromString=strings[0]
    if len(strings)>1:
        whereString=strings[1]
        wheres=parseWheres(whereString)
    else:
        wheres=[]

    rawFields=re.split(',',fieldString)
    fields=[]
    for rawField in rawFields:
        fields.append(removeEndsSpaces(rawField))

    return {
        'fields':fields,
        'from':removeEndsSpaces(fromString),
        'where':wheres
    }


def parseDeleteStatement(command):
    strings = re.split('delete from ', command)
    strings = re.split(' where ', strings[1])
    fromString = strings[0]
    if len(strings) > 1:
        whereString = strings[1]
        wheres = parseWheres(whereString)
    else:
        wheres = []
    return {
        'from':removeEndsSpaces(fromString),
        'where':wheres
    }



def parseDropTableStatement(command):
    tableName=re.sub(
        '^drop table *',
        '',
        re.sub(' *; *$','',command)
    )
    return {
        'tableName': tableName
    }


def parseCreateIndexStatement(command):
    temp=re.split(
        ' +on +',
        re.sub('^create index +','',command)
    )
    indexName=temp[0]
    temp=re.split(' *\( *',temp[1])
    tableName=temp[0]
    fieldName=re.sub(' *\) *; *$','',temp[1])
    return {
        'indexName': indexName,
        'tableName': tableName,
        'fieldName': fieldName
    }



def parseDropIndexStatement(command):
    indexName=re.sub(
        '^drop index *',
        '',
        re.sub(' *; *$','',command)
    )
    return {
        'indexName': indexName
    }
