import os
import sys
sys.path.insert(0, '/Users/kaechle/Developer/projects/scint')
from flask import Flask, request, jsonify, send_from_directory
from core.assistant import Assistant
from core.definitions.assistants import keanu
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_folder='static')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
assistant = Assistant(keanu)

@app.route('/')
def index():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'index.html')

@app.route('/message', methods=['POST'])
@cross_origin()
def message():
    user_input = request.json.get('message')
    response = assistant.message(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(port=5000)
