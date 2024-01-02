const WebSocketServer = require("ws").WebSocketServer
const joypad = require("joypad.js")

joypad.on("button_press", (e) => {
    const { buttonName } = e.detail
  
    console.log(`${buttonName} was pressed!`)
})


joypad.on("button_release", (e) => {
    const { buttonName } = e.detail
  
    console.log(`${buttonName} was released!`)
})
