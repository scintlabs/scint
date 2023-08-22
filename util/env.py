import os
from dotenv import load_dotenv

load_dotenv()
envar = lambda var: str(os.environ.get(var))
