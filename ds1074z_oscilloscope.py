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
    def query_decode(self,query):
        responce = self.query(query)
        #responce is a \n terminated bytes object
        ou = ""
        for x in responce:
            if x!="\n":
                ou = ou+chr(x)
        return ou
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
        #now put some information in
        ou["DISPLAY_TIMEDIVISION"] = self.query_decode(":WAV:XINC?")
        ou["DISPLAY_VOLTAGEDIVISION"] = self.query_decode(":WAV:YINC?")
        ou["TRIGGER_MODE"] = self.query_decode(":TRIG:MODE?")
        if ou["TRIGGER_MODE"]=="EDGE":
            ou["TRIGGER_CHANNEL"] = self.query_decode(":TRIG:EDG:SOUR?")
            ou["TRIGGER_SLOPE"] = self.query_decode(":TRIG:EDG:SLOP?")
            ou["TRIGGER_LEVEL"] = self.query_decode(":TRIG:EDG:LEV?")
        elif ou["TRIGGER_MODE"]=="DEL":
            ou["TRIGGER_SOURCEA"] = self.query_decode(":TRIG:DEL:SA?")
            ou["TRIGGER_SLOPEA"] = self.query_decode(":TRIG:DEL:SLOPA?")
            ou["TRIGGER_SOURCEB"] = self.query_decode(":TRIG:DEL:SB?")
            ou["TRIGGER_SLOPEB"] = self.query_decode(":TRIG:DEL:SLOPB?")
            ou["TRIGGER_DELAYTYPE"] = self.query_decode(":TRIG:DEL:TYP?")
            ou["TRIGGER_MAXDELAY"] = self.query_decode(":TRIG:DEL:TUPP?")
            ou["TRIGGER_MINDELAY"] = self.query_decode(":TRIG:DEL:TLOW?")
        return ou
