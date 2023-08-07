import sys, signal, subprocess, asyncio
import core.prompt
import core.definitions.content as content
from core.prompt import Prompt, prompts
from core.generator import generate
from flask import Flask
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)


if __name__ == "__main__":
    app.run(debug=True)
