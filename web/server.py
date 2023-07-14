import os
import sys
import signal

sys.path.insert(0, "/Users/kaechle/Developer/projects/scint")
from flask import Flask, request, jsonify, send_from_directory
from core.assistant import Assistant
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_folder="web")
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
keanu = "keanu"
assistant = Assistant(keanu)


def save_and_exit(signal, frame):
    print("Saving the assistant's state.")
    assistant.save()
    sys.exit(0)


signal.signal(signal.SIGINT, save_and_exit)
signal.signal(signal.SIGTERM, save_and_exit)


@app.route("/")
def index():
    return send_from_directory(os.path.join(app.root_path, ""), "index.html")


@app.route("/message", methods=["POST"])
@cross_origin()
def message():
    user_input = request.json.get("message")
    response = assistant.chat(user_input)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(port=5000)
