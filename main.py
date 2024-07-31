import flask
from os import path, walk
from flask_socketio import send, emit, SocketIO
import logging

import timer


id = ["TwitchT1", "TwitchT2", "TwitchT3", "Bits"]
timerTracker = timer.Timer(timeLeft=10)

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


if __name__ == "__main__":
    extraDirs = [r'.\static', r'.\templates']
    extraFiles = extraDirs[:]
    for extraDir in extraDirs:
        for dirname, dirs, files in walk(extraDir):
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extraFiles.append(filename)
    print(extraFiles)

    # app.run(port=5050, extra_files=extraFiles)
    socketio.run(app=app, port=5050, debug=True, use_reloader=True, allow_unsafe_werkzeug=True, extra_files=extraFiles)