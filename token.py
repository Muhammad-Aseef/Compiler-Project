class token:
    def __init__(self, value, type, line):
        self.value = value
        self.type = type
        self.line = line

tokens = []
punct = ['{','}','[',']','(',')',',',':',';']
rel_opr = [['>','ROP'], ['<','ROP'], ['>=','ROP'], ['<=','ROP'], ['==','ROP'], ['!=','ROP']]
airth = [['+','PM'], ['-','PM'], ['*','MDM'], ['/','MDM'], ['%','MDM']]
inc_dec = [['++','inc_dec'], ['--','inc_dec']]
# assign = [['=','AOP']]
log_opr = [['&&','LOP'], ['||','LOP'], ['!','LOP']]
keywords = [
    ['const','VM'], ['let','VM'], ['int','DT'], ['float','DT'], ['string','DT'], ['array','DT'], ['boolean','DT'],['char','DT'],
    ['if','if'], ['else','else'], ['ifthen','ifthen'], ['interval','interval'], ['stop','stop'], ['carryon','carryon'],
    ['func','func'], ['yeild','yield'], ['class','class'],['constructor','constructor'], ['public','AM'], ['private','AM'],
    ]

def checkAll(temp, p):
    c = isPunct(temp)
    if c:
        return tokens.append(token(temp,'punctuator',lineCount))
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
        print("does not match to any function which means it is a identifier:", temp)
        return tokens.append(token(temp,'regex',lineCount))

def isPunct(ch):
    if ch in punct:
        return True
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

# def isAssign(current, next):
#     x = current + next
#     for i in assign:
#         if i[0] == x:
#             return x,i[1]
#     for j in assign:
#         if j[0] == current:
#             return j[1]
#     return False

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

# to read code file
file = open('file.txt','r')

# to write token objects
# t_file = open('E:\\6thSem\\compiler\\myproject\\token.txt','a')

lineCount = 0
temp = "" 
oprCheck = False # checking for both airthmatic and relational operators
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
                print("in Quotes:",temp)  # token will be generated for str 
                tokens.append(token(temp,'quotation',lineCount))
                temp = ""
        elif inline_comment:
            temp += f[i]
            if i == len(f)-1:
                inline_comment = False
                print("line ends",temp)  # token will be generated for inline_comment str
                tokens.append(token(temp,'inline comment',lineCount))
                temp = ""
        elif comment:
            temp += f[i]
            if f[i] == '~':
                comment = False
                print("comment end",temp)  # token will be generated for inline_comment str
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
                            print("\" last occurs:", temp) # token for " because it is at last position
                            tokens.append(token(temp,'quotation',lineCount))
                            temp = ""
                            continue
                        if temp == '#':
                            print("# last occurs:", temp) # token for " because it is at last position
                            tokens.append(token(temp,'inline comment',lineCount))
                            temp = ""
                            continue
                        if temp == '~':
                            print("comment starts", temp)
                            comment = True
                        checkAll(temp, 'e-l')
                        temp = ""
                        continue
                    else:
                        if f[i] == '"':
                            print("\" last not empty occurs:", temp) # token for temp
                            tokens.append(token(temp,'regex',lineCount))
                            print(f[i]) # token for "
                            tokens.append(token(f[i],'quotation',lineCount))
                            temp = ""
                            continue
                        if f[i] == '#':
                            print("# last not empty occurs:", temp) # token for temp
                            tokens.append(token(temp,'regex',lineCount))
                            print(f[i]) # token for #
                            tokens.append(token(f[i],'inline comment',lineCount))
                            temp = ""
                            continue
                        if f[i] == '~':
                            print("comment starts", temp) # token for temp
                            tokens.append(token(temp,'regex',lineCount))
                            temp = f[i]
                            comment = True
                        if f[i] == '!':
                            print("not operator", temp) #token for temp
                            tokens.append(token(temp,'regex',lineCount))
                            print(f[i]) # token for !
                            tokens.append(token(f[i],'logical operator',lineCount))
                            temp = ""
                            continue
                        temp += f[i]
                        checkAll(temp, 'n-l')
                        temp = ""
                        continue
                    
                # if temp is empty
                if not temp:
                    # for coming 
                    temp += f[i]
                    if temp == '"':
                        print("\" occurs:", temp)
                        quotation = True
                        continue
                    if temp == '#':
                        print("inline_comment starts", temp)
                        inline_comment = True
                        continue
                    if temp == '~':
                        print("comment starts", temp)
                        comment = True
                        continue
                    if isPunct(temp):
                        tokens.append(token(temp,"punctuator",lineCount))
                        temp = ""
                        continue
                    y = isInc_Dec(temp, f[i+1])
                    if y:
                        tokens.append(token(y[0],y[1],lineCount))
                        oprCheck = True
                        temp = ""
                        continue
                    y = isAirth(temp)
                    if y:
                        tokens.append(token(temp,y,lineCount))
                        temp = ""
                        continue
                    # y = isAssign(temp)
                    # if y:
                    #     print("assign:", y)
                    #     tokens.append(token(temp,y,lineCount))
                    #     temp = ""
                    #     continue   
                    y = isRelOpr(temp, f[i+1])
                    if y:
                        tokens.append(token(y[0],y[1],lineCount))
                        if len(y) == 2:
                            oprCheck = True
                        temp = ""
                        continue
                    y = isLogOpr(temp, f[i+1])
                    if y:
                        tokens.append(token(y[0],y[1],lineCount))
                        if len(y) == 2:
                            oprCheck = True
                        temp = ""
                        continue
                    # for next 
                    # regex will be applied to temp
                    if isPunct(f[i+1]):
                        # token for identifier or digit because coming value is of length 1 and is not punct or opr
                        tokens.append(token(temp,'regex',lineCount))
                        temp = ""
                        continue
                    if isAirth(f[i+1]):
                        tokens.append(token(temp,'regex',lineCount))
                        temp = ""
                        continue
                    if isRelOpr(f[i+1], '0'):
                        tokens.append(token(temp,'regex',lineCount))
                        temp = ""
                        continue
                    if isLogOpr(f[i+1], '0'):
                        tokens.append(token(temp,'regex',lineCount))
                        temp = ""
                        continue
                # if temp is not empty
                else:
                    if f[i] == '"':
                        checkAll(temp, 'n-q') # token for temp
                        temp = f[i] # temp is used for token now " will over write temp
                        quotation = True
                        continue
                    if f[i] == '#':
                        checkAll(temp, 'n-ic') # token for temp
                        temp = f[i] # temp is used for token now # will over write temp
                        inline_comment = True
                        continue
                    if f[i] == '~':
                        checkAll(temp, 'n-c') # token for temp
                        temp = f[i] # temp is used for token now ~ will over write temp
                        comment = True
                        continue
                    
                    temp += f[i]
                    # checking next to be punct or opr
                    # here checkall is called for temp to be keyword / dt / identifier
                    if isPunct(f[i+1]):
                        checkAll(temp, 'n-n-p')
                        temp = ""
                        continue
                    if isRelOpr(f[i+1], '0'):
                        checkAll(temp, 'n-n-o')
                        temp = ""
                        continue
                    if isAirth(f[i+1]):
                        checkAll(temp, 'n-n-a/i_d')
                        temp = ""
                        continue
                    if isLogOpr(f[i+1], '0'):
                        checkAll(temp, 'n-n-lo')
                        temp = ""
                        continue
            else:
                if temp == "":
                    continue
                else:
                    checkAll(temp, 's')
                    temp = ""
                    continue


print("line count: ", lineCount)

t_file = open('token.txt','w')
data = ""
for i in tokens:
    print(i.type , i.value)
    data += i.type + ", " + i.value + ", " + str(i.line) + "\n"
t_file.write(data)