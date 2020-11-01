#!/usr/bin/env python3

"""
This file provides functions for SOC parsing.
If executed from command line, it checks for consistency of an input.
"""

# Usage: soc_parser.py [ -i infile.csv ] [ -o outfile.html ]
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


STATES_ORDER = ['volno', 'obsazeno', 'ukončeno']


class SOC(object):
    """Represents single SOC topic"""

    def __init__(self, splitted, column_map):
        self._parse_from_line(splitted, column_map)

    def _parse_from_line(self, splitted, column_map):
        cm = column_map

        self.id = splitted[cm['header']]
        self.name = add_nbsp(splitted[cm['name']])
        self.state = splitted[cm['state']]
        self.garant = add_nbsp(splitted[cm['garant']])
        self.head = splitted[cm['head']]
        self.contact = splitted[cm['contact']]
        self.fields = splitted[cm['fields']].split(',')
        self.fields = list(map(
            lambda s: normalize_text(s.strip()), self.fields
        ))
        self.annotation = add_nbsp(splitted[cm['annotation']])

    def __str__(self):
        return self.id

    def __lt__(self, other):
        # all not-found-states after all found states
        iself = (STATES_ORDER.index(self.state)
                 if self.state in STATES_ORDER else len(STATES_ORDER))
        iother = (STATES_ORDER.index(other.state)
                  if other.state in STATES_ORDER else len(STATES_ORDER))
        if iself != iother:
            return iself < iother
        return self.name < other.name

    __repr__ = __str__


class Garant(object):
    """Represents single SOC garant"""

    def __init__(self, splitted, column_map):
        self._parse_from_line(splitted, column_map)

    def _parse_from_line(self, splitted, column_map):
        cm = column_map

        self.name = add_nbsp(splitted[cm['header']])
        self.intro = add_nbsp(splitted[cm['intro']])

    def __str__(self):
        return self.name

    __repr__ = __str__


def parse_topic_csv(f):
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
            if len(line) < 7:
                logging.warning(f'Not enough columns of SOC #{i+1}')
                continue
            if line[0] == '':
                logging.warning(f'Empty ID of SOC #{i+1} '
                                f'({line[column_map["name"]]})')
                continue
            out.append(SOC(line, column_map))

    return out


def parse_garant_csv(f):
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
            if len(line) < 2:
                logging.warning(f'Not enough columns of SOC garant #{i+1}')
                continue
            if line[0] == '':
                logging.warning(f'Empty name of SOC garant #{i+1}')
                continue
            out.append(Garant(line, column_map))

    return out


if __name__ == '__main__':
    args = parse_args(sys.argv)

    if args.ifn != "":
        fi = open(args.ifn, 'r', encoding='utf-8')
    else:
        fi = sys.stdin

    res = parse_topic_csv(fi)

    if args.ofn != "":
        fo = open(args.ofn, 'w', encoding='utf-8')
    else:
        fo = sys.stdout

    for item in res:
        fo.write(str(item) + '\n')

    # ifn and ofn will be closed automatically here
