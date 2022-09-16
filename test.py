

opr = ['=','<','>']

def isOpr(current,next):
    if current in opr and next in opr:
        current += next
        return current