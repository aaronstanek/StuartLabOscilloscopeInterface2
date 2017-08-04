import os

def dumpBinToFile(filename,data): #data is a list of ASCII values
    if os.path.isfile(filename):
        if passData["overwrite_ok"]!=True:
            Exception("Failed to overwrite file: "+str(filename)+" File overwriting not enabled.")
    bdata = bytes(data)
    outfile = open(filename,"wb")
    outfile.truncate(0)
    outfile.seek(0,0)
    outfile.write(bdata)
    outfile.close()

def merge(data,s):
    #data is a list of ASCII values
    #s is a string
    for x in s:
        data.append(ord(x))

def addSpace(data):
    data.append(32)

def addReturn(data):
    data.append(13)
    data.append(10)

def isData(ds):
    if len(ds.data)==0:
        print("Buffer is empty, no data saved.")
        return False
    return True

def save_basic(ds,passData):
    #saves 4 column data with no header
    #first determine which channels to save
    #don't use passData["channels"] as this might be out of order
    if isData(ds)==False:
        return
    chan = []
    for i in range(1,5): #1,2,3,4
        if i in ds.data[0].data:
            chan.append(i)
    #chan now holds the list of channels in order (only those that are present)
    dataLen = len(ds.data[0].data[chan[0]]) #ugly line
    for x in ds.data:
        #for each event
        try:
            ouData = []
            for line in range(dataLen):
                for i in range(len(chan)):
                    if i!=0:
                        addSpace(ouData)
                    merge(ouData,str(x.data[chan[i]][line]))
                addReturn(ouData)
            dumpBinToFile(passData["path"]+"event_"+str(passData["eventCount"])+".ord.txt",ouData)
            passData["eventCount"] = passData["eventCount"]+1
            passData["fileCount"] = passData["fileCount"]+1
        except:
            print("Error while writing to file. Event skipped.")

def save_stuart1(ds,passData):
    if isData(ds)==False:
        return
    chan = []
    for i in range(1,5): #1,2,3,4
        if i in ds.data[0].data:
            chan.append(i)
    #chan now holds the list of channels in order (only those that are present)
    dataLen = len(ds.data[0].data[chan[0]]) #ugly line
    for x in ds.data:
        #for each event
        try:
            ouData = []
            #header
            merge(ouData,"RIGOL1074Z")
            addSpace(ouData)
            merge(ouData,str(x.meta["TIME"]))
            addSpace(ouData)
            merge(ouData,str(dataLen))
            addSpace(ouData)
            merge(ouData,str(len(chan)))
            addSpace(ouData)
            merge(ouData,str(ds.meta["DISPLAY_TIMEDIVISION"]))
            addSpace(ouData)
            merge(ouData,str(ds.meta["DISPLAY_VOLTAGEDIVISION"]))
            addReturn(ouData)
            merge(ouData,str(ds.meta["TRIGGER_MODE"]))
            addSpace(ouData)
            merge(ouData,str(ds.meta["TRIGGER_POINT"]))
            addReturn(ouData)
            if ds.meta["TRIGGER_MODE"]=="EDGE":
                merge(ouData,str(ds.meta["TRIGGER_CHANNEL"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_SLOPE"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_LEVEL"]))
                addReturn(ouData)
            elif ds.meta["TRIGGER_MODE"]=="DEL":
                merge(ouData,str(ds.meta["TRIGGER_SOURCEA"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_SLOPEA"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_SOURCEB"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_SLOPEB"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_DELAYTYPE"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_MAXDELAY"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_MINDELAY"]))
                addReturn(ouData)
            else:
                merge(ouData,"-----")
                addReturn(ouData)
            #data
            for line in range(dataLen):
                for i in range(len(chan)):
                    if i!=0:
                        addSpace(ouData)
                    merge(ouData,str(x.data[chan[i]][line]))
                addReturn(ouData)
            dumpBinToFile(passData["path"]+"event_"+str(passData["eventCount"])+".ord.txt",ouData,passData)
            passData["eventCount"] = passData["eventCount"]+1
            passData["fileCount"] = passData["fileCount"]+1
        except:
            print("Error while writing to file. Event skipped.")

def save_stuart2(ds,passData):
    if isData(ds)==False:
        return
    chan = []
    for i in range(1,5): #1,2,3,4
        if i in ds.data[0].data:
            chan.append(i)
    #chan now holds the list of channels in order (only those that are present)
    dataLen = len(ds.data[0].data[chan[0]]) #ugly line
    ouData = []
    for x in ds.data:
        #for each event
        try:
            merge(ouData,"EVENT ")
            merge(ouData,str(passData["eventCount"]))
            addReturn(ouData)
            merge(ouData,"RIGOL1074Z")
            addSpace(ouData)
            merge(ouData,str(x.meta["TIME"]))
            addSpace(ouData)
            merge(ouData,str(dataLen))
            addSpace(ouData)
            merge(ouData,str(len(chan)))
            addSpace(ouData)
            merge(ouData,str(ds.meta["DISPLAY_TIMEDIVISION"]))
            addSpace(ouData)
            merge(ouData,str(ds.meta["DISPLAY_VOLTAGEDIVISION"]))
            addReturn(ouData)
            merge(ouData,str(ds.meta["TRIGGER_MODE"]))
            addSpace(ouData)
            merge(ouData,str(ds.meta["TRIGGER_POINT"]))
            addReturn(ouData)
            if ds.meta["TRIGGER_MODE"]=="EDGE":
                merge(ouData,str(ds.meta["TRIGGER_CHANNEL"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_SLOPE"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_LEVEL"]))
                addReturn(ouData)
            elif ds.meta["TRIGGER_MODE"]=="DEL":
                merge(ouData,str(ds.meta["TRIGGER_SOURCEA"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_SLOPEA"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_SOURCEB"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_SLOPEB"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_DELAYTYPE"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_MAXDELAY"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_MINDELAY"]))
                addReturn(ouData)
            else:
                merge(ouData,"-----")
                addReturn(ouData)
            #data
            for line in range(dataLen):
                for i in range(len(chan)):
                    if i!=0:
                        addSpace(ouData)
                    merge(ouData,str(x.data[chan[i]][line]))
                addReturn(ouData)
            passData["eventCount"] = passData["eventCount"]+1
        except:
            print("Error while generating data to be written to file. Event skipped.")
        try:
            dumpBinToFile(passData["path"]+"clump_"+str(passData["fileCount"])+".ord.txt",ouData,passData)
            passData["fileCount"] = passData["fileCount"]+1
        except:
            raise Exception("Error while writing to file. Clump skipped.")

def save_stuart3(ds,passData):
    #exactly the same as stuart1, except this saves time on each line (10s of picoseconds)
    #and voltage is now stored as nanovolts
    if isData(ds)==False:
        return
    chan = []
    for i in range(1,5): #1,2,3,4
        if i in ds.data[0].data:
            chan.append(i)
    #chan now holds the list of channels in order (only those that are present)
    dataLen = len(ds.data[0].data[chan[0]]) #ugly line
    for x in ds.data:
        #for each event
        try:
            ouData = []
            #header
            merge(ouData,"RIGOL1074Z")
            addSpace(ouData)
            merge(ouData,str(x.meta["TIME"]))
            addSpace(ouData)
            merge(ouData,str(dataLen))
            addSpace(ouData)
            merge(ouData,str(len(chan)))
            addSpace(ouData)
            merge(ouData,str(ds.meta["DISPLAY_TIMEDIVISION"]))
            addSpace(ouData)
            merge(ouData,str(ds.meta["DISPLAY_VOLTAGEDIVISION"]))
            addReturn(ouData)
            merge(ouData,str(ds.meta["TRIGGER_MODE"]))
            addSpace(ouData)
            merge(ouData,str(ds.meta["TRIGGER_POINT"]))
            addReturn(ouData)
            if ds.meta["TRIGGER_MODE"]=="EDGE":
                merge(ouData,str(ds.meta["TRIGGER_CHANNEL"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_SLOPE"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_LEVEL"]))
                addReturn(ouData)
            elif ds.meta["TRIGGER_MODE"]=="DEL":
                merge(ouData,str(ds.meta["TRIGGER_SOURCEA"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_SLOPEA"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_SOURCEB"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_SLOPEB"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_DELAYTYPE"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_MAXDELAY"]))
                addSpace(ouData)
                merge(ouData,str(ds.meta["TRIGGER_MINDELAY"]))
                addReturn(ouData)
            else:
                merge(ouData,"-----")
                addReturn(ouData)
            #data
            baseTime = float(ds.meta["DISPLAY_TIMEDIVISION"]) / float((10)**(-11)) #converts to 10s of picoseconds
            for line in range(dataLen):
                merge(ouData,str(int(baseTime*line)))
                for i in range(len(chan)):
                    addSpace(ouData)
                    vol = float(x.data[chan[i]][line])
                    vol = vol / float((10)**(-9)) #converts to nanovolts
                    merge(ouData,str(int(vol)))
                addReturn(ouData)
            dumpBinToFile(passData["path"]+"event_"+str(passData["eventCount"])+".ord.txt",ouData,passData)
            passData["eventCount"] = passData["eventCount"]+1
            passData["fileCount"] = passData["fileCount"]+1
        except:
            print("Error while writing to file. Event skipped.")
