#!/usr/bin/env python3

"""
This file generates a single html page. When run multiple times, is can
generate all html files. When no input csv in defined, input is read from
stdin. When no output file is defined, output is written to stdout.

Usage:
soc_generator.py -o output_filename -t socs_topics_filename
    -g socs_garants_filename template_dir -s state1,state2,...
    -m path-to-root-template
"""

import soc_parser as parser
import os
import sys
import datetime
import logging


TEMPLATE_DIR = 'templates/soc'
TEMPLATE_TOPIC = 'topic.html'
TEMPLATE_INDEX = 'index.html'
TEMPLATE_NAVBAR = 'navbar.html'
TEMPLATE_GARANT = 'garant.html'
IMAGE_DIR = os.path.join('static', 'soc-icon')


class ArgOpts(object):
    def __init__(self, topics=None, ofn=None, garants=None, states=None,
                 template=os.path.join(TEMPLATE_DIR, TEMPLATE_INDEX)):
        self.topics = topics
        self.ofn = ofn
        self.garants = garants
        if states is None:
            states = []
        self.states = states
        self.template = template


def parse_args(argv):
    """Parses arguments"""
    opts = ArgOpts(states=['volno', 'obsazeno'])  # defaults

    i = 0
    while i < len(argv):
        if argv[i] == '-t' and i < len(argv)-1:
            opts.topics = argv[i+1]
            i += 1
        elif argv[i] == '-o' and i < len(argv)-1:
            opts.ofn = argv[i+1]
            i += 1
        elif argv[i] == '-f' and i < len(argv)-1:
            opts.field = argv[i+1]
            i += 1
        elif argv[i] == '-g' and i < len(argv)-1:
            opts.garants = argv[i+1]
            i += 1
        elif argv[i] == '-s' and i < len(argv)-1:
            opts.states = argv[i+1].split(',')
            i += 1
        elif argv[i] == '-m' and i < len(argv)-1:
            opts.template = argv[i+1]
            i += 1

        i += 1

    return opts


###############################################################################


def generate_soc(template, topic):
    template = template.replace('{{state}}', 'soc-state-'+topic.state)
    template = template.replace('{{id}}', topic.id)

    name = topic.name
    if topic.state == 'obsazeno':
        name = name + ' (obsazeno)'
    elif topic.state == 'ukončeno':
        name = name + ' (ukončeno)'

    template = template.replace('{{name}}', name)
    template = template.replace('{{garant}}', topic.garant)
    template = template.replace('{{head}}', topic.head)
    template = template.replace('{{contact}}', topic.contact)
    template = template.replace('{{annotation}}',
                                topic.annotation.replace('\n', '</p><p>'))

    if '{{field-icons}}' in template:
        icon_text = ''
        for t in topic.fields:
            icon_text += ('<div class="soc-field-image"><img src="/static/'
                          f'soc-icon/{t}.svg" alt="{t}" title="{t}"/></div>')
            svg_path = os.path.join(IMAGE_DIR, f'{t}.svg')
            if not os.path.isfile(svg_path):
                logging.warning(f'Missing file {svg_path} for SOC {topic.id}')
        template = template.replace('{{field-icons}}', icon_text)

    return template


def generate_garant(g_template, s_template, garant, topics, index):
    g_template = g_template.replace('{{name}}', garant.name)
    g_template = g_template.replace('{{color}}',
                                    'blue' if index % 2 == 0 else 'gray')
    g_template = g_template.replace('{{intro}}', garant.intro)

    if '{{topics}}' in g_template:
        top_out = ''
        for topic in topics:
            top_out += generate_soc(s_template, topic)
        g_template = g_template.replace('{{topics}}', top_out)

    return g_template


def generate_garants(index_t, output, topic_t, garant_t, topics, garants):
    topic_text = topic_t.read()
    garant_text = garant_t.read()

    for line in index_t:
        line = line.replace('{{build_datetime}}',
                            datetime.datetime.now().strftime("%-d. %-m. %Y"))

        if '{{garants}}' in line:
            for i, garant in enumerate(garants):
                filtered_topics = filter(
                    lambda x: x.garant == garant.name, topics
                )
                output.write(generate_garant(
                    garant_text, topic_text, garant, filtered_topics, i
                ) + '\n')

        elif '{{about-color}}' in line:
            output.write(line.replace(
                '{{about-color}}',
                'blue' if len(garants) % 2 == 0 else 'gray'
            ))

        else:
            output.write(line)


if __name__ == '__main__':
    args = parse_args(sys.argv)

    if args.garants is None:
        sys.stderr.write('You must provide garants filename!\n')
        sys.exit(1)

    output = open(args.ofn, 'w', encoding='utf-8') if args.ofn else sys.stdout
    topics = (open(args.topics, 'r', encoding='utf-8')
              if args.topics else sys.stdin)
    garants = open(args.garants, 'r', encoding='utf-8')
    template_dir = os.path.dirname(args.template)

    path_index = args.template
    path_topic = os.path.join(template_dir, TEMPLATE_TOPIC)
    path_garant = os.path.join(template_dir, TEMPLATE_GARANT)

    topics = parser.parse_topic_csv(topics)
    topics = list(filter(lambda topic: topic.state in args.states, topics))
    topics.sort()
    garants = parser.parse_garant_csv(garants)

    with open(path_index, 'r', encoding='utf-8') as index,\
         open(path_topic, 'r', encoding='utf-8') as topic,\
         open(path_garant, 'r', encoding='utf-8') as garant:
        generate_garants(index, output, topic, garant, topics, garants)

    # ofn will be closed automatically here
