import os
from util.env import envar

APPNAME = "scint"
USER = "Tim"

APPDATA = os.path.join(envar("XDG_DATA_HOME"), APPNAME)
