import os

def dumpBinToFile(filename,data,passData): #data is a list of ASCII values
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

def addHead(ou,ev):
    merge(ou,"HEAD")
    addReturn(ou)
    merge(ou,"MACHINE RIGOL1074Z")
    addReturn(ou)
    merge(ou,"DATETIME "+str(ev.meta["TIME"]))
    addReturn(ou)
    merge(ou,"ROWS 1200")
    addReturn(ou)
    merge(ou,"COLUMNS "+str(len(ev.data)))
    addReturn(ou)
    c = 0
    if 1 in ev.data:
        merge(ou,"COLUMN "+str(c)+" CHANNEL1 V")
        addReturn(ou)
        c = c+1
    if 2 in ev.data:
        merge(ou,"COLUMN "+str(c)+" CHANNEL2 V")
        addReturn(ou)
        c = c+1
    if 3 in ev.data:
        merge(ou,"COLUMN "+str(c)+" CHANNEL3 V")
        addReturn(ou)
        c = c+1
    if 4 in ev.data:
        merge(ou,"COLUMN "+str(c)+" CHANNEL4 V")
        addReturn(ou)
        c = c+1
    merge(ou,"SCALE_X "+str(ds.meta["DISPLAY_TIMEDIVISION"])+" s")
    addReturn(ou)
    merge(ou,"SCALE_Y "+str(ds.meta["DISPLAY_VOLTAGEDIVISION"])+" V")
    addReturn(ou)
    merge(ou,"TRIGGER_MODE "+str(ds.meta["TRIGGER_MODE"]))
    addReturn(ou)
    if ds.meta["TRIGGER_MODE"]=="EDGE":
        merge(ou,"TRIGGER_CHANNEL "+str(ds.meta["TRIGGER_CHANNEL"]))
        addSpace(ou)
        merge(ou,"TRIGGER_SLOPE "+str(ds.meta["TRIGGER_SLOPE"]))
        addSpace(ou)
        merge(ou,"TRIGGER_LEVEL "+str(ds.meta["TRIGGER_LEVEL"]))
        addReturn(ou)

def addData(ou,ds):
    merge(ou,"DATA")
    addReturn(ou)
    chan = []
    for i in range(1,5): #1,2,3,4
        if i in ds.data[0].data:
            chan.append(i)
    #chan now holds the list of channels in order (only those that are present)
    dataLen = len(ds.data[0].data[chan[0]]) #ugly line
    for line in range(dataLen):
        for i in range(len(chan)):
            if i!=0:
                addSpace(ou)
            merge(ou,str(x.data[chan[i]][line]))
        addReturn(ou)

def save_ords(ds,passData):
    if len(ds.data)==0:
        print("Buffer empty, no data saved")
        return
    for x in ds.data:
        #x is an event
        try:
            ou = []
            addHead(ou,ds)
            addData(ou,ds)
            dumpBinToFile(passData["path"]+"event_"+str(passData["eventCount"])+".ords",ouData,passData)
            passData["eventCount"] = passData["eventCount"]+1
            passData["fileCount"] = passData["fileCount"]+1
        except:
            print("Error writing to file.")
            print("Event skipped.")
