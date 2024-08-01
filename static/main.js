const socket = io();
socket.on('connect', function () {
    console.log("Connected");
});

const timerEl = document.getElementById('timer');

function updateTimer() {
    socket.emit("getSeconds");
}

socket.on("result", function (data) {
    const resultType = data.type;
    const result = data["result"];

    if (resultType === "SecondsLeft") {
        timerEl.innerText = result;
    }
})

setInterval(updateTimer, 100);
