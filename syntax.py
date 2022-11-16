from token import result

class syntaxAnalyzer():
    def __init__(self):
        self.i = 0
        self.tokens = result()

    def validate(self):
        if self.start():
            if self.tokens[self.i].type == '$':
                return True
        return False

    def start(self):
        if self.tokens[self.i].type in ['interval','if','vm']:
            if self.sst():
                # if self.sst():
                #     return True
                return True
        return False
    
    def sst(self):
        if self.tokens[self.i].type == 'interval':
            if self.interval():
                return True
        elif self.tokens[self.i].type == 'if':
            if self.if_else():
                return True
        elif self.tokens[self.i].type == 'vm':
            if self.declare():
                return True
        elif self.tokens[self.i].type == 'stop':
            self.i += 1
            if self.tokens[self.i].type == ';':
                self.i += 1
                return True
        elif self.tokens[self.i].type == 'carryon':
            self.i += 1
            if self.tokens[self.i].type == ';':
                self.i += 1
                return True
        elif self.tokens[self.i].type == 'yield':
            self.i += 1
            if self.tokens[self.i].type == ';':
                self.i += 1
                return True
        return False
    
    def interval(self):
        if self.tokens[self.i].type == 'interval':      
            self.i += 1
            if self.tokens[self.i].type == '(':
                self.i += 1
                if self.tokens[self.i].type == ')':
                    self.i += 1
                    if self.body1():
                        return True
        return False
    
    def if_else(self):
        if self.tokens[self.i].type == 'if':
            self.i += 1
            if self.tokens[self.i].type == '(':
                self.i += 1
                if self.tokens[self.i].type == ')':
                    self.i += 1
                    if self.body1():
                        if self.Else():
                            return True
        return False

    def Else(self):
        if self.tokens[self.i].type == 'else':
            self.i += 1
            if self.body1():
                return True
        elif self.tokens[self.i].type in ['interval','if','stop','carryon','yield']:
            return True
        return False

    def body(self):
        if self.tokens[self.i].type == ';':
            self.i += 1
            return True
        elif self.tokens[self.i].type == '{':
            self.i += 1
            if self.mst():
                return True
        return False
    
    def mst(self):
        if self.tokens[self.i].type in ['}',';']: # or self.tokens[self.i].type == ';'
            return True
        elif self.tokens[self.i].type in ['interval','if','vm','stop','carryon','yield']:
            if self.sst():
                if self.mst():
                    return True
        return False

    def body1(self):
        if self.tokens[self.i].type in ['interval','if','vm','stop','carryon','yield']:
            if self.sst():
                return True
        elif self.tokens[self.i].type in  [';','{']:
            if self.body():
                if self.tokens[self.i].type == '}':
                    self.i += 1
                    return True
        return False

    def declare(self):
        # vm and dt are NT as per cfg
        if self.tokens[self.i].type == 'vm':    # vm: let, const
            self.i += 1
            if self.tokens[self.i].type == 'dt':    # dt: bool, int, float, string
                self.i += 1
                if self.tokens[self.i].type == 'id':    
                    self.i += 1
                    if self.initial():
                        if self.list():
                            return True
        return False

    def initial(self):
        if self.tokens[self.i].type == '=':
            self.i += 1
            # oe will be called
            return True
        if self.tokens[self.i].type in [';',',']:
            return True
        return False
    
    def list(self):
        if self.tokens[self.i].type == ';':
            self.i += 1
            return True
        elif self.tokens[self.i].type == ',':
            self.i += 1
            if self.tokens[self.i].type == 'id': 
                self.i += 1
                if self.initial():
                    if self.list():
                        return True
        return False

    

            

s = syntaxAnalyzer()
print(s.validate())

# Match(cfg_word):
#  If tokenlist[self.i] == word:
#      Self.i ++
#       Ret true
#  Ret false