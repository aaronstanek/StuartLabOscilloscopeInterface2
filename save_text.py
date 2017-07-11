def dumpBinToFile(filename,data): #data is a list of ASCII values
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

def save_basic(ds,passData):
    #saves 4 column data with no header
    #first determine which channels to save
    #don't use passData["channels"] as this might be out of order
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
