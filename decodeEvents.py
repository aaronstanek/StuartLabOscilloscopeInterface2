from rawEvent import *
from event import *

def decodeList(raw):
    k = ""
    ou = []
    for i in range(11,len(raw)): #skips over the header
        if ((raw[i]==44) or (raw[i]==10)): # , or \n
            ou.append(float(k))
            k = ""
        else:
            k = k+chr(raw[i])
    return ou #ou is a list of values

def decodeSingularEvent(ev):
    ou = event()
    ou.meta = ev.meta
    for x in ev.data:
        ou.data[x] = decodeList(ev.data[x])
    return ou #ou is an event

def decodeEvents(raw): #raw is a rawDataset
    ou = dataset()
    for x in raw.rawData:
        #for each event
        ou.addEvent(decodeSingularEvent(x))
    return ou #ou is a dataset
