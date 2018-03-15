#!/usr/bin/env python3
# encoding: utf-8

"""
This file provides functions for evens parsing.
If executed from command line, it checks for consistency of input.
"""

# Usage: parser.py [ -i infile.csv ] [ -o outfile.html ]
# If no input file specified, input is read from stdin.
# If no output file specified, output is generated to stdout.

# Created by Jan Horacek (c) 2017-2018

import sys
import csv


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


class Activity(object):
    """Represents single activity"""

    def __init__(self, splitted):
        self._parse_from_line(splitted)

    def _parse_from_line(self, splitted):
        self.id = splitted[0]
        self.short_name = splitted[1]
        self.full_name = splitted[2]
        self.fields = splitted[3].split(',')
        self.fields = list(map(lambda s: s.strip(), self.fields))
        self.type = splitted[4]
        self.date = splitted[5]
        self.tarfet = splitted[6]
        self.web = splitted[7]
        self.price = splitted[8]
        self.place = splitted[9]
        self.contact = splitted[10]
        self.annotation = splitted[14]

    def __str__(self):
        return self.id

    __repr__ = __str__


def parse_csv(f):
    """Reads file 'f', returns output as string"""
    out = []

    reader = csv.reader(f, delimiter=',', quotechar='"')
    for i, line in enumerate(reader):
        if i < 3:
            continue
        if len(line) < 16 or line[0] == '' or line[0] == '-' or line[0] == '':
            continue

        out.append(Activity(line))

    return out


if __name__ == '__main__':
    args = parse_args(sys.argv)

    if args.ifn != "":
        fi = open(args.ifn, 'r')
    else:
        fi = sys.stdin

    res = parse_csv(fi)

    if args.ofn != "":
        fo = open(args.ofn, 'w')
    else:
        fo = sys.stdout

    for item in res:
        fo.write(str(item) + '\n')

    # ifn and ofn will be closed automatically here
