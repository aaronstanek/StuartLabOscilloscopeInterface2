import visa
import time

from rawEvent import *
from event import *

class ds1074z_oscilloscope:
    def __init__(self):
        self.rm = visa.ResourceManager()
    #first the connection stuff
    def find_device(self):
        dev = []
        rl = self.rm.list_resources("?*")
        for x in rl:
            try:
                r = self.rm.open_resource(x)
                r.query("*IDN?")
                r.close()
                dev.append(x)
            except:
                pass
        if len(dev)==0:
            raise Exception("No visa compatible devices found.")
        if len(dev)>1:
            raise Exception("More than one visa compatible device has been found. Please set visaName manually.")
        self.visaName = dev[0]
    def connect(self):
        try:
            self.res = self.rm.open_resource(self.visaName)
        except:
            raise Exception("Failed to connect.")
    def disconnect(self):
        try:
            self.res.close()
        except:
            pass
    def reconnect(self):
        good = False
        attempt = 0
        while good==False:
            try:
                self.disconnect()
            except:
                pass
            try:
                self.connect()
            except:
                pass
            try:
                self.res.query("*IDN?")
                good = True
            except:
                attempt = attempt+1
                if attempt>=10:
                    raise Exception("Failed to reconnect.")
    #now basic controls
    def sendCommand(self,command):
        self.res.write(command)
        time.sleep(0.01)
    def run(self):
        self.sendCommand("RUN")
    def stop(self):
        self.sendCommand("STOP")
    def single(self):
        self.sendCommand("SING")
    #now querying
    def readSetup(self):
        self.res.timeout = 2000 #2 seconds
        self.sendCommand(":WAV:MODE NORM")
        self.sendCommand(":WAV:FORM ASC")
        self.sendCommand(":WAV:STAR 1")
        self.sendCommand(":WAV:STOP 1200")
    def query(self,query):
        self.sendCommand(query)
        responce = self.res.read_raw()
        return responce
    def getRawEvent(self,channels):
        self.stop()
        ou = rawEvent()
        ou.meta["TIME"] = time.strftime("%Y %m %d %H %M %S") #year month day hour minute second
        for chan in channels:
            self.sendCommand(":WAV:SOUR CHAN"+str(chan))
            ou.data[chan] = self.query(":WAV:DATA?")
        self.single()
        return ou
    def getRawDataset(self,channels,count,delay):
        ou = rawDataset()
        gather = count+1
        while len(ou.rawData)<gather:
            try:
                ou.addEvent(self.getRawEvent(channels))
                time.sleep(delay)
            except:
                print("Something went wrong, now reconnecting to oscilloscope.")
                self.reconnect()
        return ou
    def getInfo(self):
        ou = dict()
        ou["DISPLAY"] = dict()
        ou["TRIGGER"] = dict()
        #now put some information in
        ou["DISPLAY"]["TIMEDIVISION"] = self.query(":WAV:XINC?")
        ou["DISPLAY"]["VOLTAGEDIVISION"] = self.query(":WAV:YINC?")
        ou["TRIGGER"]["MODE"] = self.query(":TRIG:MODE?")
        if ou["TRIGGER"]["MODE"]=="EDGE":
            ou["TRIGGER"]["CHANNEL"] = self.query(":TRIG:EDG:SOUR?")
            ou["TRIGGER"]["SLOPE"] = self.query(":TRIG:EDG:SLOP?")
            ou["TRIGGER"]["LEVEL"] = self.query(":TRIG:EDG:LEV?")
        elif ou["TRIGGER"]["MODE"]=="DEL":
            ou["TRIGGER"]["SOURCEA"] = self.query(":TRIG:DEL:SA?")
            ou["TRIGGER"]["SLOPEA"] = self.query(":TRIG:DEL:SLOPA?")
            ou["TRIGGER"]["SOURCEB"] = self.query(":TRIG:DEL:SB?")
            ou["TRIGGER"]["SLOPEB"] = self.query(":TRIG:DEL:SLOPB?")
            ou["TRIGGER"]["DELAYTYPE"] = self.query(":TRIG:DEL:TYP?")
            ou["TRIGGER"]["MAXDELAY"] = self.query(":TRIG:DEL:TUPP?")
            ou["TRIGGER"]["MINDELAY"] = self.query(":TRIG:DEL:TLOW?")
        return ou
