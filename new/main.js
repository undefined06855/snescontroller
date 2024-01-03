import Joystick from "@hkaspy/joystick-linux"
const stick = new Joystick("/dev/input/js0", { includeInit: true })

let joypad = {
    "a": false,
    "b": false,
    "x": false,
    "y": false,
    "l": false,
    "r": false,
    "start": false,
    "select": false,
    "d_up": false,
    "d_down": false,
    "d_left": false,
    "d_right": false
}

const stickDataMap = {
    "0": {
        "-32767": "d_left",
        "32767": "d_right"
    },
    "1": {
        "-32767": "d_up",
        "32767": "d_down"
    }
}

const buttonDataMap = {
    "0": "x",
    "1": "a",
    "2": "b",
    "3": "y",
    "4": "l",
    "5": "r",
    "8": "select",
    "9": "start"
}

function setButton(button, state)
{
    if (state !== undefined)
        joypad[button] = state
}

stick.on("update", data => {
    //console.log("%s %s %s", button, data.value)

    let direction = "unknown"
    if (data.type == "BUTTON")
    {
        // button events are normal, a down and an up event
        direction = buttonDataMap[data.number]
        let buttonWasPressed = data.value == 1
        setButton(direction, buttonWasPressed)
    }
    else if (data.type == "AXIS")
    {
        // d-pad events aren't normal, so we have to do this workaround

        // reset other values (e.g: if the button was left, right can't also be pressed)
        if (data.number == 0)
        {
            // x axis
            setButton("d_left", false)
            setButton("d_right", false)
        }
        else
        {
            // y axis
            setButton("d_up", false)
            setButton("d_down", false)
        }

        if (data.value != 0)
        {
            // if it isn't moved to the center, set the direction to true
            direction = stickDataMap[data.number][data.value]
            setButton(direction, true)
        }
    }
    else console.warn("unknown!")

    console.clear()
    console.log(joypad)
})
