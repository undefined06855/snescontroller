let ws = new WebSocket("ws://192.168.1.1:1000")

ws.addEventListener("open", _ => {
    console.log("connected!")
})

ws.addEventListener("message", event => {
    let jsonData = JSON.parse(event.data)

    console.log(jsonData)
})

ws.addEventListener("close", event => {
    console.log("Connection closed: " + event.reason)
})

