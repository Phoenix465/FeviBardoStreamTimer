import flask
import os
from pathlib import Path
from flask_socketio import send, emit, SocketIO
import threading
import logging
import json
import time
from math import floor


import timer


conversions = {
    "TwitchT1": [int, 180],
    "TwitchT2": [int, 180],
    "TwitchT3": [int, 180],
    "TwitchBits": [int, 180 / 200],
    "StreamElements": [float, 180 / 2],
    "YTSuperChat": [float, 180 / 1.46],  # in USD btw not won
    "YTMembership": [int, 180],
    "Afreeca": [int, 180 / 200],
    "CHZZK": [int, 180 / 2000]
}

timerTracker = timer.Timer(0)

history = {}
if os.path.isfile("history.json"):
    history = json.load(open("history.json", "r"))
    timerTracker.endTimeReference = history["time"]
else:
    history = {"time": None, "points": 0, "log": []}

app = flask.Flask(__name__)
app.logger.setLevel(logging.INFO)
app.config['TEMPLATES_AUTO_RELOAD'] = True
socketio = SocketIO(app)


@app.route("/")
def base():
    return "Welcome to the Timer"


@app.route("/timer")
def timer():
    return flask.render_template("timer.html")


@app.route("/controller")
def controller():
    return flask.render_template("controller.html")


@socketio.on("connect")
def connectedClient(data):
    print(f'Client Connected {data  }')


@socketio.on("getSeconds")
def getSeconds():
    seconds = timerTracker.getTimeLeft() % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    emit("result", {
        "type": "SecondsLeft",
        "result": f"{hour:02}:{minutes:02}:{seconds:02}",
    })


@socketio.on("addSeconds")
def addSeconds(data):
    print("Adding Seconds", data)
    timerTracker.addSeconds(data["seconds"])


@socketio.on("addTimerInfo")
def addTimerInfo(data):
    print("Adding Timer Info", data)

    subType = data["type"]

    if subType not in conversions:
        emit("result", {
            "type": "add-error",
            "reason": f"SUBSCRIPTION TYPE NOT FOUND"
        })
        return

    castFunction = conversions[subType][0]
    quantityCast = 0
    try:
        quantityCast = castFunction(data["quantity"])
    except ValueError:
        emit("result", {
            "type": "add-error",
            "reason": f"{data['quantity']} should be a {castFunction.__name__}"
        })
        return

    seconds = conversions[subType][1] * quantityCast
    history["log"].insert(0, {
        "#": len(history["log"]) + 1,
        "type": subType,
        "quantity": quantityCast,
        "seconds": seconds,
        "points": seconds / 180,
    })
    timerTracker.addSeconds(seconds)

    history["time"] = timerTracker.endTimeReference
    history["points"] += seconds / 180

    outFile = open("history.json", "w+")
    json.dump(history, outFile)
    outFile.close()

    emit("result", {
        "type": "add-info",
    })

    emit("result", {
        "type": "history-update",
        "history": history["log"][:5]
    })


@socketio.on("getHistory")
def getHistory():
    emit("result", {
        "type": "history-update",
        "history": history["log"][:5]
    })


def updateOBSFiles():
    with open("obs/timer.txt", "w+") as f:
        seconds = timerTracker.getTimeLeft() % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60

        f.seek(0)
        f.write(f"{hour:02}:{minutes:02}:{seconds:02}")
        f.truncate()

    with open("obs/points.txt", "w+") as f:
        f.seek(0)
        f.write(f"{floor(history['points'])}")
        f.truncate()

    # print("UPDATE", seconds, history["points"])


def threadUpdater():
    print("[SYSTEM] THREAD MADE")
    while True:
        updateOBSFiles()
        time.sleep(0.5)


if __name__ == "__main__":
    extraDirs = [r'.\static', r'.\templates']
    extraFiles = extraDirs[:]
    for extraDir in extraDirs:
        for dirname, dirs, files in os.walk(extraDir):
            for filename in files:
                filename = os.path.join(dirname, filename)
                if os.path.isfile(filename):
                    extraFiles.append(filename)
    print(extraFiles)

    Path("obs").mkdir(parents=True, exist_ok=True)

    thread = threading.Thread(target=threadUpdater, daemon=True)
    thread.start()

    # app.run(port=5050, extra_files=extraFiles)
    socketio.run(app=app, port=5050, debug=False, use_reloader=False, allow_unsafe_werkzeug=True, extra_files=extraFiles)