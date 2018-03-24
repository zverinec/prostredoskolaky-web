#!/usr/bin/env python3
# encoding: utf-8

"""
This file generates a single html page. When tun multiple times, is can
generate all html files. When to input csv in defined, input is read from
stdin. When no output file is defined, output is written to stdout.

Usage:
generator.py -f field -o output_filename -a csv_filename template_dir
"""

import parser
import os
import sys
import config
import datetime


TEMPLATE_ACTIVITY = 'activity.html'
TEMPLATE_INDEX = 'index.html'
TEMPLATE_NAVBAR = 'navbar.html'
TEMPLATE_DIR = 'templates'
IMAGE_DIR = os.path.join('static', 'drive-data')


class ArgOpts(object):
    def __init__(self, activities=None, ofn=None, path=None, field=None):
        self.activities = activities
        self.ofn = ofn
        self.template_dir = path
        self.field = field


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
        elif argv[i] == '-f' and i < len(argv)-1:
            opts.field = argv[i+1]
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

    # Look for a logo and a photo
    logo = None
    photo = None
    for fn in os.listdir(IMAGE_DIR):
        if fn.startswith(activity.id + '_logo'):
            logo = fn
        elif fn.startswith(activity.id + '_photo'):
            photo = fn

    if logo:
        template = template.replace('{{logo}}', os.path.join(IMAGE_DIR, logo))
    else:
        template = template.replace('{{logo}}', 'static/no-image.svg')

    if photo:
        template = template.replace('{{image}}', os.path.join(IMAGE_DIR, photo))
    else:
        template = template.replace('{{image}}', 'static/no-image.svg')

    template = template.replace('{{gridder-div-id}}', activity.id)
    template = template.replace('{{annotation}}', activity.annotation)
    template = template.replace('{{link}}', activity.link)

    return template


def generate_activities(index_t, output, navbar_t, activity_t, seminars,
                        events, field=''):
    last_line_indent = 0

    activity_text = activity_t.read()

    for line in index_t:
        line = line.replace('{{build_datetime}}',
                            datetime.datetime.now().strftime("%d. %m. %Y %H:%M"))

        if '{{navbar-fields}}' in line:
            s = navbar_t.read()
            for category in config.categories:
                output.write(
                    s.
                    replace('{{name}}', category).
                    replace('{{lower_name}}', category.lower()).
                    replace(
                        '{{class}}',
                        'active' if category.lower() == field.lower() else '')
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

    print('Template dir: %s' % (template_dir))

    path_index = os.path.join(template_dir, TEMPLATE_INDEX)
    path_activity = os.path.join(template_dir, TEMPLATE_ACTIVITY)
    path_navbar = os.path.join(template_dir, TEMPLATE_NAVBAR)

    activities = parser.parse_csv(csv)
    activities = list(filter(lambda a: a.id != '-' and a.id != '', activities))

    if args.field:
        field = args.field
        print('Generating for field: %s' % (field.lower()))
        activities = list(
            filter(lambda a: field.lower() in a.fields, activities)
        )
    else:
        field = ''

    highlighted = list(
        filter(lambda a: a.id in config.highlighted, activities)
    )
    normal = list(
        filter(lambda a: a.id not in config.highlighted, activities)
    )

    with open(path_index, 'r') as index, open(path_activity, 'r') as activity,\
         open(path_navbar, 'r') as navbar:
        generate_activities(
            index, output, navbar, activity, highlighted, normal, field
        )

    # ofn will be closed automatically here
