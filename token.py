import re

class token:
    def __init__(self, value, type, line):
        self.value = value
        self.type = type
        self.line = line

tokens = []
punct = [['{','{'], ['}','}'], ['[','['], [']',']'], ['(','('], [')',')'], [',',','], [':',':'], [';',';']]
rel_opr = [['>','rop'], ['<','rop'], ['>=','rop'], ['<=','rop'], ['==','rop'], ['!=','rop']]
airth = [['+','pm'], ['-','pm'], ['*','mdm'], ['/','mdm'], ['%','mdm']]
inc_dec = [['++','inc_dec'], ['--','inc_dec']]
assign = [['=','aop'], ['+=','cop'], ['-=','cop'],['*=','cop'], ['/=','cop'],]
log_opr = [['&&','and'], ['||','or'], ['!','not']]
keywords = [
    ['const','vm'], ['let','vm'], ['int','DT'], ['float','DT'], ['string','DT'], ['array','dt'], ['boolean','DT'],['char','DT'],
    ['if','if'], ['else','else'], ['ifthen','ifthen'], ['interval','interval'], ['stop','stop'], ['carryon','carryon'],
    ['func','func'], ['yeild','yield'], ['class','class'],['constructor','constructor'], ['public','am'], ['private','am'],
    ['true','boolconst'], ['false','boolconst']
    ]

def checkAll(temp):
    c = isPunct(temp)
    if c:
        return tokens.append(token(temp,c,lineCount))
    c = isAssign(temp, '0')
    if c:
        return tokens.append(token(temp,c,lineCount))
    c = isAirth(temp)
    if c:
        return tokens.append(token(temp,c,lineCount))
    c = isRelOpr(temp, '0')
    if c:
        return tokens.append(token(temp,c,lineCount))
    c = isLogOpr(temp, '0')
    if c:
        return tokens.append(token(temp,c,lineCount))
    c = isKeyword(temp)
    if c:
        return tokens.append(token(temp,c,lineCount))
    else:
        c = checkRegex(temp)
        # print("does not match to any function which means it is a identifier:", temp)
        return tokens.append(token(temp,c,lineCount))

def isPunct(current):
    for i in punct:
        if i[0] == current:
            return i[1]
    return False

def isRelOpr(current, next):
    x = current + next
    for i in rel_opr:
        if i[0] == x:
            return x,i[1]
    for j in rel_opr:
        if j[0] == current:
            return j[1]
    return False

def isInc_Dec(current, next):
    x = current + next
    for i in inc_dec:
        if i[0] == x:
            return x, i[1]
    return False

def isAirth(current):
    for i in airth:
        if i[0] == current:
            return i[1]
    return False

def isAssign(current, next):
    x = current + next
    for i in assign:
        if i[0] == x:
            return x,i[1]
    for j in assign:
        if j[0] == current:
            return j[1]
    return False

def isLogOpr(current, next):
    x = current + next
    for i in log_opr:
        if i[0] == x:
            return x,i[1]
    for j in log_opr:
        if j[0] == current:
            return j[1]
    return False
            
def isKeyword(current):
    for i in keywords:
        if i[0] == current:
            return i[1]
    return False

def checkRegex(temp):
    id = re.match(r'[_]?[a-zA-Z][_a-zA-Z0-9]*', temp)
    if id and id.group() == temp:
        return 'id'

    digit = re.match(r'[0-9]+', temp)
    if digit and digit.group() == temp:
        return 'digitconst'
    
    return 'false'

# to read code file
file = open('file.txt','r')

lineCount = 0
temp = "" 
oprCheck = False
quotation = False
inline_comment = False
comment = False

for f in file:
    if not f.strip():
        print("empty")
        lineCount += 1
        continue
    lineCount +=  1
    f = f.strip()
    for i in range(len(f)):
        # means double operator occurs
        if oprCheck:
            oprCheck = False
        elif quotation:
            temp += f[i]
            if i == len(f)-1 or f[i] == '"':
                quotation = False
                # token will be generated for str 
                tokens.append(token(temp,'string',lineCount))
                temp = ""
        elif inline_comment:
            temp += f[i]
            if i == len(f)-1:
                inline_comment = False
                # token will be generated for inline_comment str
                tokens.append(token(temp,'inline_comment',lineCount))
                temp = ""
        elif comment:
            temp += f[i]
            if f[i] == '~':
                comment = False
                # token will be generated for inline_comment str
                tokens.append(token(temp,'comment',lineCount))
                temp = ""
        else:
            # if coming is space that means it's breakpoint
            # it can be multiple spaces 
            if not f[i] == " ":
                if i == len(f)-1:
                    # temp empty at last
                    if not temp:
                        temp += f[i]
                        if temp == '"':
                            # token for " because it is at last position
                            tokens.append(token(temp,'string',lineCount))
                            temp = ""
                            continue
                        if temp == '#':
                            # token for " because it is at last position
                            tokens.append(token(temp,'inline_comment',lineCount))
                            temp = ""
                            continue
                        if temp == '~':
                            print("comment starts", temp)
                            comment = True
                            continue
                        checkAll(temp)
                        temp = ""
                        continue
                    else:
                        if f[i] == '"':
                            # token for temp
                            z = checkRegex(temp)
                            tokens.append(token(temp,z,lineCount))
                            # token for "
                            tokens.append(token(f[i],'string',lineCount))
                            temp = ""
                            continue
                        if f[i] == '#':
                            # token for temp
                            z = checkRegex(temp)
                            tokens.append(token(temp,z,lineCount))
                            # token for #
                            tokens.append(token(f[i],'inline_comment',lineCount))
                            temp = ""
                            continue
                        if f[i] == '~':
                            # token for temp
                            z = checkRegex(temp)
                            tokens.append(token(temp,z,lineCount))
                            temp = f[i]
                            comment = True
                            continue
                        temp += f[i]
                        checkAll(temp)
                        temp = ""
                        continue
                    
                # if temp is empty
                if not temp:
                    # for coming 
                    temp += f[i]
                    if temp == '"':
                        quotation = True
                        continue
                    if temp == '#':
                        inline_comment = True
                        continue
                    if temp == '~':
                        comment = True
                        continue
                    y = isPunct(temp)
                    if y:
                        tokens.append(token(temp,y,lineCount))
                        temp = ""
                        continue
                    y = isInc_Dec(temp, f[i+1])
                    if y:
                        tokens.append(token(y[0],y[1],lineCount))
                        oprCheck = True
                        temp = ""
                        continue
                    y = isRelOpr(temp, f[i+1])
                    if y:
                        if len(y) == 2:
                            tokens.append(token(y[0],y[1],lineCount))
                            oprCheck = True
                        else:
                            tokens.append(token(temp,y,lineCount))
                        temp = ""
                        continue
                    y = isAssign(temp, f[i+1])
                    if y:
                        if len(y) == 2:
                            tokens.append(token(y[0],y[1],lineCount))
                            oprCheck = True
                        else:
                            tokens.append(token(temp,y,lineCount))
                        temp = ""
                        continue
                    y = isAirth(temp)
                    if y:
                        tokens.append(token(temp,y,lineCount))
                        temp = ""
                        continue    
                    y = isLogOpr(temp, f[i+1])
                    if y:
                        if len(y) == 2:
                            tokens.append(token(y[0],y[1],lineCount))
                            oprCheck = True
                        else:
                            tokens.append(token(temp,y,lineCount))
                        temp = ""
                        continue
                    # for next 
                    # regex will be applied to temp
                    if isPunct(f[i+1]):
                        # token for identifier or digit because coming value is of length 1 and is not punct or opr
                        z = checkRegex(temp)
                        tokens.append(token(temp,z,lineCount))
                        temp = ""
                        continue
                    if isRelOpr(f[i+1], '0'):
                        tokens.append(token(temp,z,lineCount))
                        temp = ""
                        continue
                    if isAirth(f[i+1]):
                        tokens.append(token(temp,z,lineCount))
                        temp = ""
                        continue                    
                    if isLogOpr(f[i+1], '0'):
                        tokens.append(token(temp,z,lineCount))
                        temp = ""
                        continue
                # if temp is not empty
                else:
                    if f[i] == '"':
                        checkAll(temp) # token for temp
                        temp = f[i] # temp is used for token now " will over write temp
                        quotation = True
                        continue
                    if f[i] == '#':
                        checkAll(temp) # token for temp
                        temp = f[i] # temp is used for token now # will over write temp
                        inline_comment = True
                        continue
                    if f[i] == '~':
                        checkAll(temp) # token for temp
                        temp = f[i] # temp is used for token now ~ will over write temp
                        comment = True
                        continue
                    
                    temp += f[i]
                    # checking next to be punct or opr
                    # here checkall is called for temp to be keyword / dt / identifier
                    if isPunct(f[i+1]):
                        checkAll(temp)
                        temp = ""
                        continue
                    if isRelOpr(f[i+1], '0'):
                        checkAll(temp)
                        temp = ""
                        continue
                    if isAirth(f[i+1]):
                        checkAll(temp)
                        temp = ""
                        continue
                    if isLogOpr(f[i+1], '0'):
                        checkAll(temp)
                        temp = ""
                        continue
            else:
                if temp == "":
                    continue
                else:
                    checkAll(temp)
                    temp = ""
                    continue


print("line count: ", lineCount)

t_file = open('token.txt','w')
data = ""
for i in tokens:
    print(i.type , i.value)
    data += i.type + ", " + i.value + ", " + str(i.line) + "\n"
t_file.write(data)