let ws = new WebSocket("ws://192.168.1.1:1000")

let nostalgist = undefined

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

ws.addEventListener("open", _ => {
    console.log("connected!")
})

ws.addEventListener("message", async event => {
    let jsonData = JSON.parse(event.data)

    let ping = Date.now() - jsonData.date
    joypad = jsonData.data

    console.clear()
    console.log("Ping: %s", ping)
    console.log(joypad)

    for (let button of Object.keys(joypad))
    {
        let nostalgistButton = button.replace("d_", "")
        if (joypad[button]) await nostalgist.pressDown(nostalgistButton)
        else await nostalgist.pressUp(nostalgistButton)
    }
})

async function startGame(url)
{
    if (url.endsWith(".nes")) nostalgist = await Nostalgist.nes("http://localhost/roms/"+url)
    else if (url.endsWith(".smc")) nostalgist = await Nostalgist.snes("http://localhost/roms/"+url)
}

async function endGame()
{
    await nostalgist.exit()
}
