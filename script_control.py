import ds1074z_controlPanel

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

def commandChecker(com):
    #checks a command
    #returns True if the command is valid
    #returns False if the command is not valid
    return True #work on this

def execute(com):
    #executes a command

class command:
    def __init__(self,base,param):
        self.base = str(base)
        self.param = str(param)

class commandScript:
    def __init__(self):
        self.cp = ds1074z_controlPanel.ds1074z_controlPanel()
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
    def step(self):
        #increments pos
        #returns True if not done
        #return False if there are no more commands to execute
        self.pos = self.pos+1
        if self.pos>=self.commandCount:
            self.mode = "done"
            return False
        return True
