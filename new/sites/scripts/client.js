let ws = new WebSocket("ws://192.168.1.1:1000")

ws.addEventListener("open", _ => {
    console.log("connected!")
})

ws.addEventListener("message", event => {
    let jsonData = JSON.parse(event.data)

    let ping = Date.now() - jsonData.date
    let joypad = jsonData.data

    console.clear()
    console.log("Ping: %s", ping)
    console.log(joypad)
})
