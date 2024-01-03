import { WebSocketServer } from "ws"
// i cant get these to work with es6 formatting
const http = require("http")
const fs = require("fs")

// ----------------------------------------------------------------------------
// normal server setup
const indexhtml = fs.readFileSync("./sites/index.html")
console.log(indexhtml)

const server = http.createServer((req, res) => {
    let url = req.url
    
    switch(url)
    {
        case "/":
            serverEndRequest(res, indexhtml)
            return
    }

    serverEndRequest(res, "404 :(")
})
// ----------------------------------------------------------------------------
// websocket server setup
/**
 * @type Array<WebSocket>
 */
let connections = []

// ----------------------------------------------------------------------------


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
export function startServer()
{
    server.listen(80, "192.168.1.1", () => {
        console.log("Server started!")
    })

    const wss = new WebSocketServer({
        port: 1000,
        host: "192.168.1.1"
    })
    
    wss.on("connection", async client => {
        let indexOfThis = connections.push(client) - 1
    
        client.on("close", _ => {
            connections.splice(indexOfThis, 1)
        })
    })
}

function serverEndRequest(res, data="", filetype="text/html")
{
    // the access control allow origin actually doesn't matter, since this is
    // the only webpage being served on this network
    res.setHeader("Access-Control-Allow-Origin", "192.168.1.1")
    res.setHeader("Content-Type", filetype)
    res.write(data)
    res.end()
}

