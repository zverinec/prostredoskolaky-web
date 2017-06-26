#!/usr/bin/env python3
# encoding: utf-8

"""
This scripts generates list of activities presented at ks.muni.cz from tsv
file (exported from table of activies at GDrive).
It is not intended to generate whole html!
Instead, this script generates just the list of activities and user may
add html tags & css by outer scripts.
"""

# Usage: content_gen.py [ -i infile.tsv ] [ -o outfile.html ]
# If no input file specified, input is read from stdin.
# If no output file specified, output is generated to stdout.

# Created by Jan Horacek (c) 2017

# TODO: input file may contain newlines, this script will not handle them

import sys

SEPARATOR = '\t'


class ArgOpts(object):
    def __init__(self, ifn="", ofn=""):
        self.ifn = ifn
        self.ofn = ofn


# Parses arguments
def parse_args(argv):
    opts = ArgOpts()

    for i in range(len(argv)):
        if argv[i] == "-i" and i < len(argv)-1:
            opts.ifn = argv[i+1]
        elif argv[i] == "-o" and i < len(argv)-1:
            opts.ofn = argv[i+1]

    return opts


# HTML encode
def he(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


class Activity(object):
    def __init__(self, line):
        self._parse_from_line(line)

    def _parse_from_line(self, l):
        splitted = l.split(SEPARATOR)

        print(splitted)

        self.shortName = splitted[1]
        self.fullName = splitted[2]
        self.field = splitted[3]
        self.type = splitted[4]
        self.date = splitted[5]
        self.tarfet = splitted[6]
        self.web = splitted[7]
        self.price = splitted[8]
        self.place = splitted[9]
        self.contact = splitted[10]
        self.annotation = splitted[14]


# Processes a single line of tsv file and produces instance of Activity
def process_activity(a):
    o = ""

    o += "<h2>{}</h2>\n".format(he(a.fullName))
    o += "<p>{}</p>\n".format(he(a.annotation))

    return o


# Reads file 'f', returns output as string
def process_tsv(f):
    out = ""

    for line in f.readlines()[3:]:
        out += process_activity(Activity(line))

    return out


if __name__ == '__main__':
    args = parse_args(sys.argv)

    if args.ifn != "":
        fi = open(args.ifn, 'r')
    else:
        fi = sys.stdin

    res = process_tsv(fi)

    if args.ofn != "":
        fo = open(args.ofn, 'w')
    else:
        fo = sys.stdout

    fo.write(res)
