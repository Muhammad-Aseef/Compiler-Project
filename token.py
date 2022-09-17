
punct = ['{','}','[',']','(',')',',',':',]
opr = ['=','<','>']
datatype = ['int', 'float', 'string', 'arr']
keywords = ['if', 'else', 'while', 'for', 'print']

def checkAll(temp, p):
        if isPunct(temp):
            print(f"{p}: punctuator {temp}")
        elif isOpr(temp, 0):
            print(f"{p}: operator {temp}")
        elif isKeyword(temp):
            print(f"{p}: keyword {temp}")
        elif isDatatype(temp):
            print(f"{p}: datatype {temp}")
        else:
            print(f"{p}: does not match to any function which means it is a identifier: {temp}")

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

def isDatatype(ch):
    if ch in datatype:
        return True
    return False
    
def isKeyword(ch):
    if ch in keywords:
        return True
    return False

file = open('E:\\6thSem\\compiler\\myproject\\file.txt','r')
lineCount = 0
for f in file:
    if not f.strip():
        print("empty")
        lineCount += 1
        continue
    lineCount +=  1
    f = f.strip()
    temp = "" 
    oprCheck = False
    quotation = False
    for i in range(len(f)):
        # means double operator occurs
        if oprCheck:
            oprCheck = False
            continue
        while quotation:
            temp += f[i]
            if i == len(f)-1 or f[i] == '"':
                quotation = False
                print("in Quotes:",temp)  # token will be generated for str
                temp = ""
            break
        else:
            # if coming is space that means it's breakpoint
            # it can be multiple spaces 
            if not f[i] == " ":
                if i == len(f)-1:
                    # temp empty at last
                    if not temp:
                        if f[i] == '"':
                            temp += f[i]
                            print("\" last occurs:", temp) # token for " because it is at last position
                            continue
                        temp += f[i]
                        checkAll(temp, 'e-l')
                        continue
                    else:
                        if f[i] == '"':
                            print("\" last not empty occurs:", temp) # token for temp
                            print(f[i]) # token for "
                            continue
                        temp += f[i]
                        checkAll(temp, 'n-l')
                        continue
                    
                # if temp is empty
                if not temp:
                    temp += f[i]
                    if f[i] == '"':
                        print("\" occurs:", temp)
                        quotation = True
                        continue
                    # for coming 
                    if isPunct(temp):
                        print("punctuator", temp)
                        temp = ""
                        continue
                    isOp = isOpr(temp, f[i+1])
                    if isOp:
                        print("operator:", isOp)
                        if len(isOp) == 2:
                            oprCheck = True
                        temp = ""
                        continue
                    # for next 
                    if isPunct(f[i+1]):
                        # token for identifier because coming value is of length 1 and is not punct or opr
                        print("next punctuator", temp)
                        temp = ""
                        continue
                    if isOpr(f[i+1], 0):
                        print("next operator", temp)
                        temp = ""
                        continue
                # if temp is not empty
                else:
                    if f[i] == '"':
                        checkAll(temp, 'n-q') # token for temp
                        temp = f[i] # temp is used for token now " will over write temp
                        quotation = True
                        continue
                    temp += f[i]
                    # checking next to be punct or opr
                    if isPunct(f[i+1]):
                        checkAll(temp, 'n-n-p')
                        temp = ""
                        continue
                    if isOpr(f[i+1], 0):
                        checkAll(temp, 'n-n-o')
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

'''
# last
if isKeyword(temp):
    print("last keyword", temp)
elif isDatatype(temp):
    print("last datatype", temp)
else:
    print("not empty (last) does not match to any function which means it is a identifier:", temp)

if isPunct(temp):
    print("last punctuator", temp)
elif isOpr(temp, 0):
    print("last operator", temp)
else:
    print("empty temp (last): does not match to any function which means it is a identifier:", temp)


# not empty
print("\" not empty occurs:", temp) # token for temp
if isDatatype(temp):
    print("not empty Data type", temp) # token
elif isKeyword(temp):
    print("not empty keyword", temp) # token
else:
    print("not empty does not match to any function which means it is a identifier:", temp)

print("not empty next punctuator", temp)
if isDatatype(temp):
    print("not empty Data type", temp) # token
elif isKeyword(temp):
    print("not empty keyword", temp) # token
else:
    print("not empty does not match to any function which means it is a identifier:", temp)

print("not empty next operator", temp)
if isDatatype(temp):
    print("not empty Data type", temp) # token
elif isKeyword(temp):
    print("not empty keyword", temp) # token
else:
    print("not empty does not match to any function which means it is a identifier", temp)


# space
if isDatatype(temp):
    print("space", temp)
    temp = ""
    continue
if isKeyword(temp):
    print("space keyword", temp)
    temp = ""
    continue
print("space, does not match to any function which means it is a identifier", temp)
temp = ""
continue
'''