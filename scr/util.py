"""This file contains helper function for whole project."""

import re
import unicodedata


def add_nbsp(text: str) -> str:
    return re.sub(r' ([AIKOSUVZaikosuvz]) ([\w\d])', r' \1 \2', text)


def escape_field(text: str) -> str:
    nfkd_form = unicodedata.normalize('NFKD', text)
    only_ascii = nfkd_form.encode('ASCII', 'ignore').decode('utf-8')
    non_space = only_ascii.replace(' ', '-')
    return non_space.lower()
