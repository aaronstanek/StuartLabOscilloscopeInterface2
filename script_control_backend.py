def setVariable(p,vb):
    g = p.split("=")
    if len(g)!=2:
        raise Exception("set command coud not be parsed: "+"set "+p)
    vb.setValue(g[0],g[1])

def execute(cp,com,vb,extra):
    #cp is a controlPanel object
    #com is command object
    #vb is variable block object
    #extra is a dictionary containing whatever
    osc = cp.osc
    #osc is an oscilloscope object
    b = com.base
    p = com.param
    if b=="set":
        setVariable(p,vb)
    elif b=="send":
        osc.sendCommand(p)
    elif b=="find":
        osc.find_device()
    elif b=="connect":
        osc.connect()
    elif b=="disconnect":
        osc.disconnect()
    elif b=="reconnect":
        osc.reconnect()
    elif b=="run":
        osc.run()
    elif b=="stop":
        osc.stop()
    elif b=="single":
        osc.single()
    elif b=="readsetup":
        osc.readSetup()
    elif b=="time-division":
        osc.setTimeDivision(p)
    elif b=="voltage-division":
        osc.setVoltageDivision(p)
    elif b=="trigger-mode":
        osc.setTriggerMode(p.upper())
    elif b=="trigger-edge":
        osc.setEdgeTrigger(extra)
    elif b=="trigger-delay":
        osc.setDelayTrigger(extra)
    elif b=="collect-data":
        cp.collector(extra["channels"],extra["count"],extra["delay"],extra["path"],extra["fmt"])
    else:
        raise Exception("Command not recognized. Error was caught in runtime and not by language checker.")
