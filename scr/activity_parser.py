#!/usr/bin/env python3

"""
This file provides functions for events parsing.
If executed from command line, it checks for consistency of an input.
"""

# Usage: activity_parser.py [ -i infile.csv ] [ -o outfile.html ]
# If no input file specified, input is read from stdin.
# If no output file specified, output is generated to stdout.

import sys
import csv
import logging
from util import add_nbsp, normalize_text


class ArgOpts(object):
    def __init__(self, ifn="", ofn=""):
        self.ifn = ifn
        self.ofn = ofn


def parse_args(argv):
    """Parses arguments"""
    opts = ArgOpts()

    for i in range(len(argv)):
        if argv[i] == "-i" and i < len(argv)-1:
            opts.ifn = argv[i+1]
        elif argv[i] == "-o" and i < len(argv)-1:
            opts.ofn = argv[i+1]

    return opts


class Org(object):
    """Represents a single oganisator of an activity"""

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __str__(self):
        return self.name + ', ' + self.url

    __repr__ = __str__


def parse_orgs(orgs):
    res = []
    for org in orgs.split('; '):
        org_splitted = org.split(': ')
        if len(org_splitted) == 2:
            res.append(Org(add_nbsp(org_splitted[0]), org_splitted[1]))

    return res


class Activity(object):
    """Represents single activity"""

    def __init__(self, splitted, column_map):
        self._parse_from_line(splitted, column_map)

    def _parse_from_line(self, splitted, column_map):
        cm = column_map

        self.id = splitted[cm['header']]
        self.short_name = splitted[cm['short-name']]
        self.full_name = add_nbsp(splitted[cm['full-name']])
        self.orgs = parse_orgs(splitted[cm['orgs']])
        self.fields = splitted[cm['fields']].split(',')
        self.fields = list(map(
            lambda s: normalize_text(s.strip()), self.fields
        ))
        self.type = splitted[cm['type']]
        self.date = splitted[cm['date']]
        self.target = add_nbsp(splitted[cm['target']])
        self.link = splitted[cm['link']]
        self.price = add_nbsp(splitted[cm['price']])
        self.place = add_nbsp(splitted[cm['place']])
        self.contact = splitted[cm['contact']]
        self.highlighted = (splitted[cm['highlighted']].lower() == 'ano')
        self.annotation = add_nbsp(splitted[cm['annotation']])

    def __str__(self):
        return self.id

    __repr__ = __str__


def parse_csv(f):
    """Reads file 'f', returns output as string"""
    out = []

    reader = csv.reader(f, delimiter=',', quotechar='"')
    column_map = {}
    header_loaded = False

    for i, line in enumerate(reader):
        if line[0].lower() == 'header':
            for coli, name in enumerate(line):
                column_map[name.lower()] = coli
            header_loaded = True
        else:
            if not header_loaded or line[0] == '-':
                continue
            if len(line) < 16:
                logging.warning(f'Not enough columns of activity #{i+1}')
                continue
            if line[0] == '':
                logging.warning(f'Empty ID of activity #{i+1} '
                                f'({line[column_map["full-name"]]})')
                continue
            out.append(Activity(line, column_map))

    return out


def parse_file(fn):
    with open(fn, 'r', encoding='utf-8') as f:
        return parse_csv(f)


if __name__ == '__main__':
    args = parse_args(sys.argv)

    if args.ifn != "":
        fi = open(args.ifn, 'r', encoding='utf-8')
    else:
        fi = sys.stdin

    res = parse_csv(fi)

    if args.ofn != "":
        fo = open(args.ofn, 'w', encoding='utf-8')
    else:
        fo = sys.stdout

    for item in res:
        fo.write(str(item) + '\n')

    # ifn and ofn will be closed automatically here
