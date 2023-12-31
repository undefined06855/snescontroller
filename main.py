from inputs import get_gamepad

def main():
    """Just print out some event infomation when the gamepad is used."""
    while 1:
        for event in get_gamepad():
            if event.ev_type == "Absolute":
                # dpad movement
                if event.code == "ABS_X":
                    if event.state == 0:
                        print("d-left")
                    elif event.state == 127:
                        print("d-center")
                    elif event.state == 255:
                        print("d-right")
                if event.code == "ABS_Y":
                    if event.state == 0:
                        print("d-up")
                    elif event.state == 127:
                        print("d-center")
                    elif event.state == 255:
                        print("d-down")
                
            if event.ev_type == "Key":
                # face buttons (can also test using Misc, but is a bit misleading)
                if event.code == "BTN_THUMB":
                    print("A")
                elif event.code == "BTN_THUMB2":
                    print("B")
                elif event.code == "BTN_TRIGGER":
                    print("X")
                elif event.code == "BTN_TOP":
                    print("Y")
                
                # bumpers
                elif event.code == "BTN_TOP2":
                    print("L")
                elif event.code == "BTN_PINKIE":
                    print("R")

                # start / select
                elif event.code == "BTN_BASE4":
                    print("Start")
                elif event.code == "BTN_BASE3":
                    print("Select")
            print("                                 ", event.ev_type, event.code, event.state)


if __name__ == "__main__":
    main()