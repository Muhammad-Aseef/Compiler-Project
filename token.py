import pickle


class token:
    def __init__(self, value, type, line):
        self.value = value
        self.type = type
        self.line = line


tokens = []
punct = ['{','}','[',']','(',')',',',':']
opr = ['=','<','>']
airth = ['+', '-', '*', '/']
inc_dec = ['++', '--']
log_opr = ['&&', '||','!']
datatype = ['int', 'float', 'string', 'arr']
keywords = ['if', 'else', 'while', 'for', 'print']

def checkAll(temp, p):
        if isPunct(temp):
            print(f"{p}: punctuator {temp}")
            tokens.append(token(temp,'punctuator',lineCount))
        elif isOpr(temp, 0):
            print(f"{p}: operator {temp}")
            tokens.append(token(temp,'operator',lineCount))
        elif isAirth(temp, 0):
            print(f"{p}: airthmatic {temp}")
            tokens.append(token(temp,'airthmatic operator',lineCount))
        elif isLogOpr(temp, 0):
            print(f"{p}: logical {temp}")
            tokens.append(token(temp,'logical operator',lineCount))
        elif isKeyword(temp):
            print(f"{p}: keyword {temp}")
            tokens.append(token(temp,'keyword',lineCount))
        elif isDatatype(temp):
            print(f"{p}: datatype {temp}")
            tokens.append(token(temp,'data type',lineCount))
        else:
            print(f"{p}: does not match to any function which means it is a identifier: {temp}")
            tokens.append(token(temp,'regex',lineCount))

def isPunct(ch):
    if ch in punct:
        return True
    return False
    
def isOpr(current, next):
    if current in opr and next in opr:
        if next == '=':
            current += next
            return current
        else:
            return current
    else:
        if current in opr:
            return current
        return False

def isAirth(current, next):
    if current in airth and next in airth:
        x = current + next
        if x in inc_dec:
            return x
        return current
    else:
        if current in airth:
            return current
        return False

def isLogOpr(current, next):
    if current == '&' or current == '|':
        x = current + next
        if x in log_opr:
            return x
        return False
    else:
        if current in log_opr:
            return current
            

def isDatatype(ch):
    if ch in datatype:
        return True
    return False
    
def isKeyword(ch):
    if ch in keywords:
        return True
    return False

# to read code file
file = open('E:\\6thSem\\compiler\\myproject\\file.txt','r')

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
                    if temp == '!' and f[i+1] == '=':
                        temp += f[i+1]
                        print("not equal operator: ", temp)
                        tokens.append(token(temp,'not equal',lineCount))
                        oprCheck = True
                        temp = ""
                        continue
                    if isPunct(temp):
                        print("punctuator", temp)
                        tokens.append(token(temp,"punctuator",lineCount))
                        temp = ""
                        continue
                    isOp = isOpr(temp, f[i+1])
                    if isOp:
                        print("operator:", isOp)
                        tokens.append(token(isOp,'operator',lineCount))
                        if len(isOp) == 2:
                            oprCheck = True
                        temp = ""
                        continue
                    isLogop = isLogOpr(temp, f[i+1])
                    if isLogop:
                        print("logicl operator:", isLogop)
                        tokens.append(token(isLogop,'logical operator',lineCount))
                        if len(isLogop) == 2:
                            oprCheck = True
                        temp = ""
                        continue
                    isAir = isAirth(temp, f[i+1])
                    if isAir:
                        if len(isAir) == 1:
                            print("airthmatic operator:", isAir)
                            tokens.append(token(isAir,'airthmatic operator',lineCount))
                        else:
                            print("inc_dec:", isAir)
                            tokens.append(token(isAir,'inc_dec',lineCount))
                            oprCheck = True   
                        temp = ""
                        continue
                    # for next 
                    # regex will be applied to temp
                    if f[i+1] == '!' and f[i+2] == '=':
                        print("next not equal operator: ", temp)
                        tokens.append(token(temp,'regex',lineCount))
                        temp = ""
                        continue
                    if isPunct(f[i+1]):
                        # token for identifier because coming value is of length 1 and is not punct or opr
                        print("next punctuator", temp)
                        tokens.append(token(temp,'regex',lineCount))
                        temp = ""
                        continue
                    if isOpr(f[i+1], 0):
                        print("next operator", temp)
                        tokens.append(token(temp,'regex',lineCount))
                        temp = ""
                        continue
                    if isAirth(f[i+1], 0):
                        print("next airthmatic operator", temp)
                        tokens.append(token(temp,'regex',lineCount))
                        temp = ""
                        continue
                    if isLogOpr(f[i+1], 0):
                        print("next logical operator", temp)
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
                    if f[i+1] == '!' and i != len(f)-2 and f[i+2] == '=':
                        print("not empty next not equal operator: ", temp)
                        tokens.append(token(temp,'regex',lineCount))
                        temp = ""
                        continue
                    if isPunct(f[i+1]):
                        checkAll(temp, 'n-n-p')
                        temp = ""
                        continue
                    if isOpr(f[i+1], 0):
                        checkAll(temp, 'n-n-o')
                        temp = ""
                        continue
                    if isAirth(f[i+1], 0):
                        checkAll(temp, 'n-n-a')
                        temp = ""
                        continue
                    if isLogOpr(f[i+1], 0):
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
for i in tokens:
    print(i.type , i.value)

# token file
# t_file = open('test.pkl','wb')
# for j in tokens:
#     pickle.dump(j, t_file, pickle.HIGHEST_PROTOCOL)

# read_file = open('test.pkl','rb')
# c = pickle.load(read_file)
# print(c.type)
