def dumpBinToFile(filename,data): #data is a list of ASCII values
    bdata = bytes(data)
    outfile = open(filename,"wb")
    outfile.truncate(0)
    outfile.seek(0,0)
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
