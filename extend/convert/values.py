import re
import numpy as np


def is_float(s: str) -> bool:
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(s)
    if result:
        return True
    else:
        return False
