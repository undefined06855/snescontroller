from inputs import get_gamepad

def main():
    """Just print out some event infomation when the gamepad is used."""
    while 1:
        events = get_gamepad()
        for event in events:
            if event.ev_type == "Absolute":
                # dpad movement
                if event.code == "ABS_X":
                    if event.state == 0:
                        print("d-left")
                    elif event.state == 127:
                        print("d-center")
                    elif event.state == 256:
                        print("d-right")
                if event.code == "ABS_Y":
                    if event.state == 0:
                        print("d-up")
                    elif event.state == 127:
                        print("d-center")
                    elif event.state == 256:
                        print("d-down")
            print(event.ev_type, event.code, event.state)


if __name__ == "__main__":
    main()