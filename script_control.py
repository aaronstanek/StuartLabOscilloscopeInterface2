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
    def getValueC(self,name):
        v = self.getValue(name)
        return v.upper()
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
                    extra["TRIGGER_CHANNEL"] = self.vb.getValueC("tr-channel")
                except:
                    pass
                try:
                    extra["TRIGGER_SLOPE"] = self.vb.getValueC("tr-slope")
                except:
                    pass
                try:
                    extra["TRIGGER_LEVEL"] = self.vb.getValueC("tr-level")
                except:
                    pass
                script_control_backend.execute(self.cp,c,self.vb,extra)
            elif c.base=="trigger-delay":
                extra = dict()
                try:
                    extra["TRIGGER_SOURCEA"] = self.vb.getValueC("tr-source-a")
                except:
                    pass
                try:
                    extra["TRIGGER_SOURCEB"] = self.vb.getValueC("tr-source-b")
                except:
                    pass
                try:
                    extra["TRIGGER_SLOPEA"] = self.vb.getValueC("tr-slope-a")
                except:
                    pass
                try:
                    extra["TRIGGER_SLOPEB"] = self.vb.getValueC("tr-slope-b")
                except:
                    pass
                try:
                    extra["TRIGGER_DELAYTIME"] = self.vb.getValueC("tr-delay-time")
                except:
                    pass
                try:
                    extra["TRIGGER_MAXDELAY"] = self.vb.getValueC("tr-delay-max")
                except:
                    pass
                try:
                    extra["TRIGGER_MINDELAY"] = self.vb.getValueC("tr-delay-min")
                except:
                    pass
                script_control_backend.execute(self.cp,c,self.vb,extra)
            elif c.base=="collect-data":
                channels = self.vb.getValue("co-channels")
                channels = channels.split(",")
                for i in range(len(channels)):
                    channels[i] = int(channels[i])
                #channels is set
                extra = dict()
                extra["channels"] = channels
                extra["count"] = int(self.vb.getValue("co-count"))
                extra["delay"] = float(self.vb.getValue("co-delay"))
                extra["path"] = self.vb.getValue("co-path")
                extra["fmt"] = self.vb.getValue("co-format")
                script_control_backend.execute(self.cp,c,self.vb,extra)
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
    for i in range(len(lines)):
        c = ""
        p = ""
        sp = lines[i].decode("utf8")
        sp = sp.split(" ")
        c = sp[0]
        firstNonempty = -1
        for j in range(1,len(sp)):
            if len(sp[j])!=0:
                firstNonempty = j
                break
        if firstNonempty!=-1:
            for j in range(firstNonempty,len(sp)):
                if j!=firstNonempty:
                    p = p+" "
                p = p+sp[j]
        lines[i] = [c,p]
    return lines

def readParse(filename):
    #returns a commandScript object
    raw = readFileRaw(filename)
    lines = parseFile(raw)
    ou = commandScript()
    for x in lines:
        ou.addCommand(x[0],x[1])
    return ou
