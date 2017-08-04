import json
import os

def dumpStringToFile(filename,data,passData):
    if os.path.isfile(filename):
        if passData["overwrite_ok"]!=True:
            Exception("Failed to overwrite file: "+str(filename)+" File overwriting not enabled.")
    outfile = open(filename,"w")
    outfile.truncate(0)
    outfile.seek(0,0)
    outfile.write(data)
    outfile.close()

def isData(ds):
    if len(ds.data)==0:
        print("Buffer is empty, no data saved.")
        return False
    return True

def save_basic(ds,passData):
    #saves individual files with minimal data
    if isData(ds)==False:
        return
    for x in ds.data:
        #for each event
        try:
            jData = json.dumps(x.data)
            dumpStringToFile(passData["path"]+"event_"+str(passData["eventCount"])+".ord.json",jData,passData)
            passData["eventCount"] = passData["eventCount"]+1
            passData["fileCount"] = passData["fileCount"]+1
        except:
            print("Error while writing to file. Event skipped.")

def save_meta(ds,passData):
    #saves "OSC_META", "EV_META", and "DATA" with each event
    if isData(ds)==False:
        return
    for x in ds.data:
        #for each event
        try:
            pData = dict()
            pData["OSC_META"] = ds.meta
            pData["EV_META"] = x.meta
            pData["DATA"] = x.data
            jData = json.dumps(pData)
            dumpStringToFile(passData["path"]+"event_"+str(passData["eventCount"])+".ord.json",jData,passData)
            passData["eventCount"] = passData["eventCount"]+1
            passData["fileCount"] = passData["fileCount"]+1
        except:
            print("Error while writing to file. Event skipped.")

def save_clump(ds,passData):
    if isData(ds)==False:
        return
    try:
        pData = dict()
        pData["OSC_META"] = ds.meta
        da = []
        for x in ds.data:
            #x is an event
            m = dict()
            m["EV_META"] = x.meta
            m["DATA"] = x.data
            da.append(m)
        pData["EVENTS"] = da
        jData = json.dumps(pData)
        dumpStringToFile(passData["path"]+"clump_"+str(passData["fileCount"])+".ord.json",jData,passData)
        passData["eventCount"] = passData["eventCount"]+len(da)
        passData["fileCount"] = passData["fileCount"]+1
    except:
        print("Error while writing to file. Clump skipped.")
