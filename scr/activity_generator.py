#!/usr/bin/env python3

"""
This file generates a single html page. When run multiple times, is can
generate all html files. When no input csv in defined, input is read from
stdin. When no output file is defined, output is written to stdout.

Usage:
activity_generator.py -f field -o output_filename -a csv_filename template_dir
"""

import activity_parser as parser
import os
import sys
import config
import datetime
import util
import re


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
        activity.full_name
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
        template = template.replace('{{image}}', os.path.join(IMAGE_DIR,
                                                              photo))
    else:
        template = template.replace('{{image}}', 'static/no-image.svg')

    template = template.replace('{{id}}', activity.id)
    template = template.replace('{{annotation}}', activity.annotation)
    template = template.replace('{{link}}', activity.link)
    template = template.replace(
        '{{go-text}}',
        'Přejit na web akce'
        if activity.link != '' else 'Web této akce se připravuje'
    )
    template = template.replace(
        '{{go-btn-class}}',
        'disabled' if activity.link == '' else ''
    )
    template = template.replace(
        '{{activity-type}}',
        'activity-highlighted' if activity.highlighted else 'activity-normal'
    )

    text = ''
    for org in activity.orgs:
        text += f'<a href="{org.url}" target="_blank">{org.name}</a>, '
    template = template.replace('{{orgs}}', text[:-2])

    return template


def generate_activities(index_t, output, navbar_t, activity_t, seminars,
                        events, field=''):
    write = True

    activity_text = activity_t.read()

    for line in index_t:
        line = line.replace('{{build_datetime}}',
                            datetime.datetime.now().strftime("%-d. %-m. %Y"))

        if '{{#if events}}' in line:
            write = (bool)(events)

        elif '{{/if}}' in line:
            write = True

        elif '{{#if field' in line:
            match = re.search(r'\{\{#if field=(.*)\}\}', line)
            write = (field == match.group(1))

        elif '{{navbar-fields}}' in line:
            s = navbar_t.read()
            for category in config.categories:
                escaped = util.normalize_text(category.lower())
                output.write(
                    s.
                    replace('{{name}}', category).
                    replace('{{url}}', escaped).
                    replace(
                        '{{class}}',
                        'active' if escaped == field.lower() else '')
                )

        elif '{{seminars}}' in line:
            for activity in seminars:
                output.write(generate_activity(activity_text, activity) + '\n')

        elif '{{events}}' in line:
            for activity in events:
                output.write(generate_activity(activity_text, activity) + '\n')

        elif '{{events_header}}' in line:
            if field == '':
                output.write(line.replace(
                    '{{events_header}}',
                    '<h2>Vlajkové akce</h2>'
                ))

        elif '{{about-id}}' in line:
            if field == '':
                output.write(line.replace('{{about-id}}', 'about-index'))
            else:
                output.write(line.replace('{{about-id}}', 'about-field'))

        elif write:
            output.write(line)


if __name__ == '__main__':
    args = parse_args(sys.argv)

    output = open(args.ofn, 'w', encoding='utf-8') if args.ofn else sys.stdout
    csv = (open(args.activities, 'r', encoding='utf-8')
           if args.activities else sys.stdin)
    template_dir = args.template_dir if args.template_dir else TEMPLATE_DIR

    path_index = os.path.join(template_dir, TEMPLATE_INDEX)
    path_activity = os.path.join(template_dir, TEMPLATE_ACTIVITY)
    path_navbar = os.path.join(template_dir, TEMPLATE_NAVBAR)

    activities = parser.parse_csv(csv)
    activities = list(filter(lambda a: a.id != '-' and a.id != '', activities))

    if args.field:
        field = args.field
        highlighted = list(
            filter(lambda a: field.lower() in a.fields, activities)
        )
        highlighted.sort(key=lambda a: not a.highlighted)
        normal = []
    else:
        field = ''

        highlighted = list(
            filter(lambda a: a.highlighted, activities)
        )
        normal = list(
            filter(lambda a: not a.highlighted, activities)
        )

    with open(path_index, 'r', encoding='utf-8') as index,\
         open(path_activity, 'r', encoding='utf-8') as activity,\
         open(path_navbar, 'r', encoding='utf-8') as navbar:
        generate_activities(
            index, output, navbar, activity, highlighted, normal, field
        )

    # ofn will be closed automatically here
