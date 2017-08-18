import only3
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
        time.sleep(2) #sleep for 2 seconds
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
                self.run()
                self.query_decode(":WAV:XINC?")
                good = True
            except:
                attempt = attempt+1
                if attempt>=60:
                    raise Exception("Failed to reconnect.")
                time.sleep(10) #sleep for 10 seconds before trying again
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
        if len(responce)<2:
            return ""
        return (responce[:len(responce)-1]).decode("utf8")
    def getRawEvent(self,channels):
        self.stop()
        ou = rawEvent()
        ou.meta["TIME"] = time.strftime("%Y %m %d %H %M %S") #year month day hour minute second
        for chan in channels:
            self.sendCommand(":WAV:SOUR CHAN"+str(chan))
            ou.data[chan] = self.query(":WAV:DATA?")
        self.single()
        return ou
    def getRawEvent_with_vpp(self,channels,vpp):
        while True:
            self.stop()
            m = True
            for chan in vpp:
                if self.measure_vpp(chan)<vpp[chan]:
                    m = False
                    break
            if m:
                break
            self.single()
        ou = rawEvent()
        ou.meta["TIME"] = time.strftime("%Y %m %d %H %M %S") #year month day hour minute second
        for chan in channels:
            self.sendCommand(":WAV:SOUR CHAN"+str(chan))
            ou.data[chan] = self.query(":WAV:DATA?")
        self.single()
        return ou
    def getRawDataset(self,channels,count,delay,options):
        ou = rawDataset()
        gather = count+1
        while len(ou.rawData)<gather:
            try:
                if "vpp" not in options:
                    ou.addEvent(self.getRawEvent(channels))
                else:
                    ou.addEvent(self.getRawEvent_with_vpp(channels,options["vpp"]))
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
##        ou["TRIGGER_POINT"] = self.query_decode(":TRIG:POS?")
        ou["TRIGGER_POINT"] = "TRIGGER_POINT_TESTING_VALUE_REMOVE_LATER"
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
    #now advanced controls
    def setTimeDivision(self,value):
        self.sendCommand(":WAV:XINC "+str(value))
    def setVoltageDivision(self,value):
        self.sendCommand(":WAV:YINC "+str(value))
    def setTriggerMode(self,value):
        self.sendCommand(":TRIG:MODE "+str(value))
    def setEdgeTrigger(self,values):
        self.setTriggerMode("EDGE")
        if "TRIGGER_CHANNEL" in values:
            self.sendCommand(":TRIG:EDG:SOUR "+str(values["TRIGGER_CHANNEL"]))
        if "TRIGGER_SLOPE" in values:
            self.sendCommand(":TRIG:EDG:SLOP "+str(values["TRIGGER_SLOPE"]))
        if "TRIGGER_LEVEL" in values:
            self.sendCommand(":TRIG:EDG:LEV "+str(values["TRIGGER_LEVEL"]))
    def setDelayTrigger(self,values):
        self.setTriggerMode("DEL")
        if "TRIGGER_SOURCEA" in values:
            self.sendCommand(":TRIG:DEL:SA "+str(values["TRIGGER_SOURCEA"]))
        if "TRIGGER_SLOPEA" in values:
            self.sendCommand(":TRIG:DEL:SLOPA "+str(values["TRIGGER_SLOPEA"]))
        if "TRIGGER_SOURCEB" in values:
            self.sendCommand(":TRIG:DEL:SB "+str(values["TRIGGER_SOURCEB"]))
        if "TRIGGER_SLOPEB" in values:
            self.sendCommand(":TRIG:DEL:SLOPB "+str(values["TRIGGER_SLOPEB"]))
        if "TRIGGER_DELAYTYPE" in values:
            self.sendCommand(":TRIG:DEL:TYP "+str(values["TRIGGER_DELAYTYPE"]))
        if "TRIGGER_MAXDELAY" in values:
            self.sendCommand(":TRIG:DEL:TUPP "+str(values["TRIGGER_MAXDELAY"]))
        if "TRIGGER_MINDELAY" in values:
            self.sendCommand(":TRIG:DEL:TLOW "+str(values["TRIGGER_MINDELAY"]))
    def measure_vpp(self,chan):
        return float(self.query_decode(":MEAS:ITEM? VPP "+chan))
