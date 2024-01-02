const WebSocketServer = require("ws").WebSocketServer
const gamepad = require("gamepad")

gamepad.init()

// poll events at a very high rate
setInterval(gamepad.processEvents, 10)
   
// Listen for button up events on all gamepads
gamepad.on("up", function (id, num) {
    console.log("up", {
      id: id,
      num: num,
    });
  });
   
  // Listen for button down events on all gamepads
  gamepad.on("down", function (id, num) {
    console.log("down", {
      id: id,
      num: num,
    });
  });

