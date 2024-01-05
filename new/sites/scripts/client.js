let ws = new WebSocket("ws://192.168.1.1:1000")

let nostalgist = undefined

const createNostalgistSettings = url => {
    return {
        rom: [url],

        resolveCoreJs(core) {
            return `http://192.168.1.1/cores/${core}_libretro.js`
        },

        resolveCoreWasm(core) {
            return `http://192.168.1.1/cores/${core}_libretro.wasm`
        },

        resolveRom(file) {
            return `http://192.168.1.1/roms/${file}`
        }
    }
}

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

let prevJoypad = {
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
    // loop through all and see what's changed
    let changed
    for (let [b, v] of Object.entries(joypad))
    {
        // button, value
        if (prevJoypad[b] != v)
        {
            changed = b
            break
        }
    }
    prevJoypad = joypad

    // these lag the game more than you'd think... or maybe that's just me
    //console.clear()
    //console.log("Ping: %s", ping)
    //console.log(joypad)

    let nostalgistButton = button.replace("d_", "")
    if (joypad[changed])
        nostalgist.pressDown(nostalgistButton)
    else
        nostalgist.pressUp(nostalgistButton)
})

async function startGame(url)
{
    if (url.endsWith(".nes"))
    {
        nostalgist = await Nostalgist.launch({
            core: "fceumm",
            ...createNostalgistSettings(url)
        })
    }
    else if (url.endsWith(".smc"))
    {
        nostalgist = await Nostalgist.launch({
            core: "snes9x",
            ...createNostalgistSettings(url)
        })
    }
}

async function endGame()
{
    await nostalgist.exit()
}
