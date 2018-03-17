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
import config


class ArgOpts(object):
    def __init__(self, activities=None, ofn=None, path=None):
        self.activities = activities
        self.ofn = ofn
        self.template_dir = path


def parse_args(argv):
    """Parses arguments"""
    opts = ArgOpts()

    i = 0
    while i < len(argv):
        if argv[i] == '-a' and i < len(argv)-1:
            opts.activities = argv[i+1]
            i += 1
        elif argv[i] == '-o' and i < len(argv)-1:
            opts.ofn = argv[i+1]
            i += 1
        elif i > 0:
            opts.template_dir = argv[i]

        i += 1

    return opts

###############################################################################

def generate_activity(template, activity):
    template = template.replace(
        '{{name}}',
        activity.short_name
        if activity.short_name != '-' and activity.short_name != '--'
        else activity.full_name
    )
    template = template.replace('{{duration}}', activity.date)
    template = template.replace('{{logo}}', 'static/%s.svg' % (activity.id))
    template = template.replace('{{image}}', 'static/%s.svg' % (activity.id))
    template = template.replace('{{gridder-div-id}}', activity.id)
    template = template.replace('{{annotation}}', activity.annotation)
    template = template.replace('{{link}}', activity.link)

    return template


def generate_activities(index_t, output, navbar_t, activity_t, seminars, events):
    last_line_indent = 0

    activity_text = activity_t.read()

    for line in index_t:
        if '{{navbar-fields}}' in line:
            s = navbar_t.read()
            for category in config.categories:
                output.write(
                    s.\
                    replace('{{name}}', category).\
                    replace('{{lower_name}}', category.lower())
                )

        elif '{{seminars}}' in line:
            for activity in seminars:
                output.write(generate_activity(activity_text, activity) + '\n')

        elif '{{events}}' in line:
            for activity in events:
                output.write(generate_activity(activity_text, activity) + '\n')

        else:
            output.write(line)


if __name__ == '__main__':
    args = parse_args(sys.argv)

    output = open(args.ofn, 'w') if args.ofn else sys.stdout
    csv = open(args.activities, 'r') if args.activities else sys.stdin
    template_dir = args.template_dir if args.template_dir else TEMPLATE_DIR

    print('Template dir: ' + template_dir)

    path_index = os.path.join(template_dir, TEMPLATE_INDEX)
    path_activity = os.path.join(template_dir, TEMPLATE_ACTIVITY)
    path_navbar = os.path.join(template_dir, TEMPLATE_NAVBAR)

    activities = parser.parse_csv(csv)

    highlighted = filter(lambda a: a.id in config.highlighted, activities)
    normal = filter(lambda a: a.id not in config.highlighted, activities)

    with open(path_index, 'r') as index, open(path_activity, 'r') as activity, \
         open(path_navbar, 'r') as navbar:
        generate_activities(index, output, navbar, activity, highlighted, normal)

    # ofn will be closed automatically here
