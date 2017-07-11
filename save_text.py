def dumpBinToFile(filename,data): #data is a list of ASCII values
    bdata = bytes(data)
    outfile = open(filename,"wb")
    outfile.truncate(0)
    outfile.seek(0,0)
    outfile.close()
