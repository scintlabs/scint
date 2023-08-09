import sys, signal, subprocess, asyncio
import core.prompt
import core.definitions.types as types
from core.prompt import Prompt, meta_prompts
from core.generator import generate
from flask import Flask
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)


if __name__ == "__main__":
    app.run(debug=True)
