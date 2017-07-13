class variableBlock:
    def __init__(self):
        self.vars = dict()
    def setValue(self,name,value):
        self.vars[str(name)] = str(value)
    def getValue(self,name):
        sn = str(name)
        if sn in self.vars:
            return self.vars[sn]
        return ""
    def removeValue(self,name):
        sn = str(name)
        if sn in self.vars:
            del(self.vars[sn])
    def exists(self,name):
        sn = str(name)
        if sn in self.vars:
            return True
        return False

class command:
    def __init__(self,base,param):
        self.base = str(base)
        self.param = str(param)

class commandScript:
    def __init__(self):
        self.com = []
        self.vb = variableBlock()
        self.mode = "setup"
    def addCommand(self,name,param):
        self.com.append(command(name,param))
    def readyForValidation(self):
        self.mode = "validation"
        self.pos = 0
        self.comCount = len(self.com)
    def readyForExecution(self):
        self.mode = "execution"
        self.pos = 0
