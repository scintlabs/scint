from collections import defaultdict
from collections.abc import Set
from functools import reduce
from typing import Dict
from uuid import uuid4

import numpy as np

from scint.data import Collection, Block, Messages
from scint.core.containers.blocks import Embedding
from scint.support.logging import log
from scint.support.types import List, Union
from scint.support.utils import cosine_similarity
