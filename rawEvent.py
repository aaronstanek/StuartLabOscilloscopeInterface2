class rawEvent:
    def __init__(self):
        self.meta = dict()
        self.data = dict()
    def selfTest(self):
        #checks to see if this is a valid event
        if len(self.data)==0:
            return False
        for x in self.data: #for each channel
            if len(self.data[x])==0:
                return False
            if self.data[x]==b'#9000000000\n':
                return False
        return True
    def __eq__(self,other):
        #only compares data
        #assumes that they have the same channels
        chan = list(self.data)
        for c in chan:
            if self.data[c]!=other.data[c]:
                return False
        return True
    def __ne__(self,other):
        if self==other:
            return False
        return True

class rawDataset:
    def __init__(self):
        self.rawData = [] #list of rawEvent
    def addEvent(self,ev):
        self.rawData.append(ev)
    def removeBadEvents(self):
        hold = []
        for x in self.rawData:
            #for each rawEvent
            if x.selfTest:
                hold.append(x)
        ou = rawDataset()
        for i in range(1,len(hold)):
            if (hold[i-1]!=hold[i]):
                ou.addEvent(hold[i])
        return ou #ou is another rawDataset
