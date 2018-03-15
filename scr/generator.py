#!/usr/bin/env python3
# encoding: utf-8

"""TODO: add docstring"""

# TODO: describe usage

import parser
import re


def generate_activity(template_fn, activity):
    with open(template_fn, 'r') as inp:
        lines = inp.read()

    lines.replace('{{name}}', activity.short_name)
    lines.replace('{{duration}}', activity.date)
    lines.replace('{{logo}}', 'static/ksi.svg')
    lines.replace('{{image}}', 'static/ksi.svg')
    lines.replace('{{gridder-div-id}}', activity.id)
    lines.replace('{{annotation}}', activity.annotation)
    lines.replace('{{link}}', activity.link)


def generate_html(template_fn, output_fn, activities):
    with open(template_fn, 'r') as inp, open(output_fn, 'w') as out:
        for line in inp:
            out.write(line)


if __name__ == '__main__':
    pass
