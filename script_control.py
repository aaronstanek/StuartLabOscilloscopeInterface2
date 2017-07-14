import ds1074z_controlPanel
import script_control_backend

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
    def execute(self):
        for c in self.com:
            #c is a command
            if c.base=="trigger-edge":
                extra = dict()
                try:
                    extra["TRIGGER_CHANNEL"] = self.vb.getValue("tr-channel")
                except:
                    pass
                try:
                    extra["TRIGGER_SLOPE"] = self.vb.getValue("tr-slope")
                except:
                    pass
                try:
                    extra["TRIGGER_LEVEL"] = self.vb.getValue("tr-level")
                except:
                    pass
                script_control_backend.execute(self.cp,c,self.vb,extra)
            elif c.base=="trigger-delay":
                extra = dict()
                try:
                    extra["TRIGGER_SOURCEA"] = self.vb.getValue("tr-source-a")
                except:
                    pass
                try:
                    extra["TRIGGER_SOURCEB"] = self.vb.getValue("tr-source-b")
                except:
                    pass
                try:
                    extra["TRIGGER_SLOPEA"] = self.vb.getValue("tr-slope-a")
                except:
                    pass
                try:
                    extra["TRIGGER_SLOPEB"] = self.vb.getValue("tr-slope-b")
                except:
                    pass
                try:
                    extra["TRIGGER_DELAYTIME"] = self.vb.getValue("tr-delay-time")
                except:
                    pass
                try:
                    extra["TRIGGER_MAXDELAY"] = self.vb.getValue("tr-delay-max")
                except:
                    pass
                try:
                    extra["TRIGGER_MINDELAY"] = self.vb.getValue("tr-delay-min")
                except:
                    pass
                script_control_backend.execute(self.cp,c,self.vb,extra)
            elif c.base=="collect-data":
                pass
            else:
                script_control_backend.execute(self.cp,c,self.vb,dict())

def readFileRaw(filename):
    infile = open(filename,"rb")
    indata = infile.read()
    infile.close()
    return indata

def polysplit(bdata,splitc):
    #bdata is a bytearray
    #splitc is a list of byte arrays to split along
    last = 0
    foundLen = 0
    ou = []
    for i in range(len(bdata)):
        found = False
        for x in splitc:
            if x==bdata[i:i+len(x)]:
                found = True
                foundLen = len(x)
                break
        if found:
            ou.append(bdata[last:i])
            last = i+foundLen
    ou.append(bdata[last:len(bdata)])
    return ou

def parseFile(bdata):
    lines = polysplit(bdata,[b'\r',b'\n'])
    no_empty_lines = []
    for x in lines:
        if len(x)!=0:
            no_empty_lines.append(x)
    lines = no_empty_lines
    del(no_empty_lines)
    for lin in range(len(lines)):
        x = (lines[lin]).decode("utf-8")
        c = ""
        p = ""
        mode = "c"
        for i in range(len(x)):
            if mode==c:
                if x==" ":
                    c = x[:i]
                    mode = "s"
            elif mode=="s":
                if x!=" ":
                    p = x[i:]
                    mode = "d"
        if mode=="c":
            lines[lin] = [c,""]
        elif mdoe=="s":
            lines[lin] = [c,""]
        else:
            lines[lin] = [c,p]
    return lines

def readParse(filename):
    #returns a commandScript object
    raw = readFileRaw(filename)
    lines = parseFile(raw)
    ou = commandScript()
    for x in lines:
        ou.addCommand(x[0],x[1])
    return ou
