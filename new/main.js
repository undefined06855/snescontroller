import Joystick from "@hkaspy/joystick-linux"

const stick = new Joystick("/dev/input/js0", { includeInit: true })

stick.on("update", data => {
    console.log("%s %s %s", data.type, data.number, data.value)
})
