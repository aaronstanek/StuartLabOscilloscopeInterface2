import script_control

def main():
    cs = script_control.readParse("osc_control.txt")
    cs.execute()

main()
