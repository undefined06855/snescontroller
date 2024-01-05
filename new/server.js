import { WebSocketServer } from "ws"
import { ServerResponse, createServer } from "http"
import { readFileSync, createReadStream } from "fs"

// -----------------------------------------------------------------------------
// normal server setup
const indexhtml = readFileSync("./sites/index.html")
const clientjs = readFileSync("./sites/scripts/client.js")
const nostalgistjs = readFileSync("./sites/scripts/nostalgist.js")
const rommapjs = readFileSync("./sites/scripts/rom_map.js")
const css = readFileSync("sites/style.css")

const fceummjs = readFileSync("sites/cores/fceumm_libretro.js")
const snes9xjs = readFileSync("sites/cores/snes9x_libretro.js")

const server = createServer((req, res) => {
    let url = req.url
    
    switch(url)
    {
        case "/":
            serverEndRequest(res, indexhtml)
            return

        case "/scripts/client.js":
            serverEndRequest(res, clientjs, "text/javascript")
            return

        case "/scripts/rom_map.js":
            serverEndRequest(res, rommapjs, "text/javascript")
            return

        case "/scripts/nostalgist.js":
            serverEndRequest(res, nostalgistjs, "text/javascript")
            return

        case "/style.css":
            serverEndRequest(res, css, "text/css")
            return
        
        case "/cores/fceumm_libretro.js":
            serverEndRequest(res, fceummjs, "text/javascript")
            return

        case "/cores/snes9x_libretro.js":
            serverEndRequest(res, snes9xjs, "text/javascript")
            return


        default:
            // either doesnt exist or just a rom binary file / wasm file that
            // doesn't need to be cached
            let failed = false
            try { readAndSendBinaryData(res, "./sites"+url) }
            catch(_) { failed = true }
            if (!failed) return
            // if it failed it goes down to the 404
            // but actually breaks a lot of http stuff
            // oh well ¯\_(ツ)_/¯ shouldn't be accessing that stuff anyway
    }

    serverEndRequest(res, "404 :(")
})
// -----------------------------------------------------------------------------
// websocket server setup
/**
 * @type Array<WebSocket>
 */
let connections = []
// -----------------------------------------------------------------------------




/**
 * Sends something to every websocket client connected.
 * @param {Object} data JSON data to send.
 */
export function sendToClients(data)
// this is used in `joypad.js`
{
    for (let connection of connections)
    {
        connection.send(JSON.stringify(data))
    }
}

/**
 * Starts the http server, and sets up the websocket server
 */
export async function startServer()
{
    server.listen(80, "192.168.1.1", () => {
        console.log("Server started!")
    })

    const wss = new WebSocketServer({
        port: 1000,
        host: "192.168.1.1"
    })

    wss.on("listening", _ => {
        console.log("Websocket started!")
    })
    
    wss.on("connection", async client => {
        let indexOfThis = connections.push(client) - 1
    
        client.on("close", _ => {
            connections.splice(indexOfThis, 1)
        })
    })
}

/**
 * @param {ServerResponse} res 
 * @param {Object} data 
 * @param {string} filetype 
 */
function serverEndRequest(res, data="", filetype="text/html")
{
    // the access control allow origin actually doesn't matter, since this is
    // the only webpage being served on this network
    res.setHeader("Access-Control-Allow-Origin", "192.168.1.1")
    res.setHeader("Content-Type", filetype)
    res.write(data)
    res.end()
}

/**
 * @param {ServerResponse} res 
 * @param {string} path 
 */
function readAndSendBinaryData(res, path)
{
    const fileStream = createReadStream(decodeURI(path))

    res.setHeader("Content-Type", "application/octet-stream")
    res.setHeader("Content-Disposition", "attachment")

    fileStream.pipe(res)

    // Handle any errors during the streaming
    fileStream.on("error", (error) => {
        // this actuallt returns a ERR_INVALID_RESPONSE on chrome, but oh well
        // also you will never see this console.error 
        console.error(`Error reading and sending binary data: ${error.message}`)
        res.statusCode = 500
        res.end("500 Internal Server Error")
    })
}

