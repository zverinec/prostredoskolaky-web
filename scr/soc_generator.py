#!/usr/bin/env python3
# encoding: utf-8

"""
This file generates a single html page. When run multiple times, is can
generate all html files. When no input csv in defined, input is read from
stdin. When no output file is defined, output is written to stdout.

Usage:
soc_generator.py -o output_filename -t socs_topics_filename template_dir
"""

import soc_parser as parser
import os
import sys
import config
import datetime


TEMPLATE_TOPIC = 'topic.html'
TEMPLATE_INDEX = 'index.html'
TEMPLATE_NAVBAR = 'navbar.html'
TEMPLATE_DIR = 'templates/soc'
IMAGE_DIR = os.path.join('static', 'drive-data')


class ArgOpts(object):
    def __init__(self, topics=None, ofn=None, path=None):
        self.topics = topics
        self.ofn = ofn
        self.template_dir = path


def parse_args(argv):
    """Parses arguments"""
    opts = ArgOpts()

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
        elif i > 0:
            opts.template_dir = argv[i]

        i += 1

    return opts


###############################################################################


def generate_soc(template, topic):
    template = template.replace('{{name}}',topic.name)
    template = template.replace('{{garant}}', topic.garant)
    template = template.replace('{{head}}', topic.head)
    template = template.replace('{{contact}}', topic.contact)
    template = template.replace('{{annotation}}', topic.annotation)

    return template


def generate_socs(index_t, output, topic_t, topics):
    last_line_indent = 0

    topic_text = topic_t.read()

    for line in index_t:
        line = line.replace('{{build_datetime}}',
                            datetime.datetime.now().strftime("%-d. %-m. %Y"))

        if '{{topics}}' in line:
            for topic in topics:
                output.write(generate_soc(topic_text, topic) + '\n')

        else:
            output.write(line)


if __name__ == '__main__':
    args = parse_args(sys.argv)

    output = open(args.ofn, 'w', encoding='utf-8') if args.ofn else sys.stdout
    topics = open(args.topics, 'r', encoding='utf-8') \
             if args.topics else sys.stdin
    template_dir = args.template_dir if args.template_dir else TEMPLATE_DIR

    print('Template dir: %s' % (template_dir))

    path_index = os.path.join(template_dir, TEMPLATE_INDEX)
    path_topic = os.path.join(template_dir, TEMPLATE_TOPIC)

    topics = parser.parse_csv(topics)
    # topics = list(filter(lambda a: a.id != '-' and a.id != '', topics))

    with open(path_index, 'r', encoding='utf-8') as index,\
         open(path_topic, 'r', encoding='utf-8') as topic:
        generate_socs(index, output, topic, topics)

    # ofn will be closed automatically here
