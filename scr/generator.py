#!/usr/bin/env python3
# encoding: utf-8

"""TODO: add docstring"""

# TODO: describe usage

TEMPLATE_ACTIVITY = 'activity.html'
TEMPLATE_INDEX = 'index.html'
TEMPLATE_NAVBAR = 'navbar.html'
TEMPLATE_DIR = 'templates'

import parser
import os
import sys


class ArgOpts(object):
    def __init__(self, ofn=None, path=None):
        self.ofn = ofn
        self.template_dir = path


def parse_args(argv):
    """Parses arguments"""
    opts = ArgOpts()

    for i in range(len(argv)):
        if argv[i] == "-o" and i < len(argv)-1:
            opts.ofn = argv[i+1]
            i += 1
        elif i > 0:
            opts.template_dir = argv[i]

    return opts

###############################################################################

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

    return lines


def generate_activities(index_t, output, navbar_t, activity_t, seminars, events):
    last_line_indent = 0

    for line in index_t:
        if '{{navbar-fields}}' in line:
            for line in navbar_t:
                output.write(line)

        elif '{{seminars}}' in line:
            for activity in seminars:
                output.write(generate_activity(activity_t, activity) + '\n')

        elif '{{events}}' in line:
            for activity in events:
                output.write(generate_activity(activity_t, activity) + '\n')

        else:
            output.write(line)

if __name__ == '__main__':
    args = parse_args(sys.argv)

    output = open(args.ofn, 'w') if args.ofn else sys.stdout
    template_dir = args.template_dir if args.template_dir else TEMPLATE_DIR

    print('Template dir: ' + template_dir)

    path_index = os.path.join(template_dir, TEMPLATE_INDEX)
    path_activity = os.path.join(template_dir, TEMPLATE_ACTIVITY)
    path_navbar = os.path.join(template_dir, TEMPLATE_NAVBAR)

    with open(path_index, 'r') as index, open(path_activity, 'r') as activity, \
         open(path_navbar, 'r') as navbar:
        generate_activities(index, output, navbar, activity, [], [])

    # ofn will be closed automatically here
