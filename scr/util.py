"""This file contains helper function for whole project."""

import re

def add_nbsp(text):
    return re.sub(r' ([AIKOSUVZaikosuvz]) ([\w\d])', r' \1 \2', text)
