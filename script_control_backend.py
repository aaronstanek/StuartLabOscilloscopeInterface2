def execute(cp,com,vb,extra):
    #cp is a controlPanel object
    #com is command object
    #vb is variable block object
    #extra is a dictionary containing whatever
    osc = cp.osc
    #osc is an oscilloscope object
    b = com.base
    p = com.param
    if b=="send":
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
        osc.setTriggerMode(p)
    elif b=="trigger-edge":
        osc.setEdgeTrigger(extra)
    elif b=="trigger-delay":
        osc.setDelayTrigger(extra)
    elif b=="collect-data":
        cp.collector(extra["channels"],extra["count"],extra["delay"],extra["path"],extra["fmt"])
    else:
        raise Exception("Command not recognized. Error was caught in runtime and not by language checker.")
