import only3
import ds1074z_oscilloscope #also brings rawEvent and event

from rawEvent import *
from event import *
import decodeEvents

import save_json
import save_text
import save_ords

class ds1074z_controlPanel:
    def __init__(self):
        self.osc = ds1074z_oscilloscope.ds1074z_oscilloscope()
    def launch(self):
        print("Finding oscilloscope.")
        self.osc.find_device()
        print("Connecting to oscilloscope.")
        self.osc.connect()
    def close(self):
        self.osc.disconnect()
    def saveDataset(self,ds,passData):
        if passData["fmt"]=="json_basic":
            save_json.save_basic(ds,passData)
        elif passData["fmt"]=="json_meta":
            save_json.save_meta(ds,passData)
        elif passData["fmt"]=="json_clump":
            save_json.save_clump(ds,passData)
        elif passData["fmt"]=="text_basic":
            save_text.save_basic(ds,passData)
        elif passData["fmt"]=="text_stuart1":
            save_text.save_stuart1(ds,passData)
        elif passData["fmt"]=="text_stuart2":
            save_text.save_stuart2(ds,passData)
        elif passData["fmt"]=="text_stuart3":
            save_text.save_stuart3(ds,passData)
        elif passData["fmt"]=="ords":
            save_ords.save_ords(ds,passData)
        else:
            raise Exception("The save format ("+str(passData["fmt"])+") is not recognized.")
    def singleCollection(self,passData):
        print("Getting events.")
        raw = self.osc.getRawDataset(passData["channels"],100,passData["delay"])
        print("Filtering events.")
        filtered = raw.removeBadEvents()
        del(raw)
        print("Decoding events.")
        clean = decodeEvents.decodeEvents(filtered)
        del(filtered)
        print("Getting metadata.")
        meta = self.osc.getInfo()
        for x in meta:
            clean.meta[x] = meta[x]
        print("Saving events.")
        self.saveDataset(clean,passData)
    def collector(self,channels,count,delay,path,fmt):
        self.launch()
        print("Setting up.")
        self.osc.readSetup()
        passData = dict()
        passData["channels"] = channels
        passData["count"] = count
        passData["delay"] = delay
        passData["path"] = path
        passData["fmt"] = fmt
        passData["eventCount"] = 0
        passData["fileCount"] = 0
        print("Starting data collection.")
        while passData["eventCount"]<passData["count"]:
            self.singleCollection(passData)
            print("Event Count: "+str(passData["eventCount"]))
            print("File Count: "+str(passData["fileCount"]))
        print("Data collection complete.")
        self.close()
        print("Connection closed.")
