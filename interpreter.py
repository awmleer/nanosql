import re

def interpret(command):
    command=removeFrontSpaces(command)
    if re.match('^select',command):
        command=re.sub('^select','',command)
        return {
            'operation': 'select',
            'data': parseSelectStatement(command)
        }
    elif re.match('insert',command):
        return {
            'operation': 'insert',
            'data': None
        }
    print(command)
    return re.sub('^ +','1','  aaa')



def removeFrontSpaces(text):
    return re.sub('^ +','',text)

def removeRearSpaces(text):
    return re.sub(' +$','',text)

def removeEndsSpaces(text):
    return removeRearSpaces(removeFrontSpaces(text))


def parseSelectStatement(command):
    # command=removeFrontSpaces(command)
    strings=re.split(' from ',command)
    fieldString=strings[0]
    strings=re.split(' where ',strings[1])
    fromString=strings[0]
    whereString=strings[1]

    rawFields=re.split(',',fieldString)
    fields=[]
    for rawField in rawFields:
        fields.append(removeEndsSpaces(rawField))

    rawWheres=re.split(' and ',whereString)
    wheres=[]
    for rawWhere in rawWheres:
        operand=''
        if re.search('=',rawWhere):
            operand='='
        elif re.search('<>',rawWhere):
            operand='<>'
        elif re.search('>',rawWhere):
            operand='>'
        elif re.search('<',rawWhere):
            operand='<'
        elif re.search('>=',rawWhere):
            operand='>='
        elif re.search('<=',rawWhere):
            operand='<='
        if operand=='':
            return "error" # TODO raise error
        operators=re.split(operand,rawWhere)
        wheres.append({
            'operand':'=',
            'operatorA':removeEndsSpaces(operators[0]),
            'operatorB':removeEndsSpaces(operators[1])
        })

    return {
        'fields':fields,
        'from':removeEndsSpaces(fromString),
        'where':wheres
    }
