import os
import sys
import signal

sys.path.insert(0, "/Users/kaechle/Developer/projects-active/scint")
from flask import Flask, request, jsonify, send_from_directory
from core.collaborator import Collaborator
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_folder="web")
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
collaborator = Collaborator()


def save_and_exit(signal, frame):
    print("Saving the collaborator's state.")
    collaborator.state.save()
    sys.exit(0)


signal.signal(signal.SIGINT, save_and_exit)
signal.signal(signal.SIGTERM, save_and_exit)


@app.route("/")
def index():
    return send_from_directory(os.path.join(app.root_path, "client/"), "index.html")


@app.route("/message", methods=["POST"])
@cross_origin()
def message():
    user_message = request.json.get("message")
    response = collaborator.chat(user_message)
    return response


if __name__ == "__main__":
    app.run(port=5000)
