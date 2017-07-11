class event:
    def __init__(self):
        self.meta = dict()
        self.data = dict()

class dataset:
    def __init__(self):
        self.data = []
        self.meta = dict()
    def addEvent(self,ev):
        self.data.append(ev)
