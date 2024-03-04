#!/usr/bin/env python3

import argparse
import cjkwrap

from itertools import groupby

def paragraph(lines) :
    for group_separator, line_iteration in groupby(lines.splitlines(True),
                                                   key = str.isspace) :
        if not group_separator :
            yield ''.join(line_iteration)


def main():
    parser = argparse.ArgumentParser(description = 'format string vector')
    parser.add_argument('--string', dest='inString', help='input string')
    args = parser.parse_args()

    inString = args.inString.strip(" \n")
    reString = ""

    for p in paragraph(inString):
        p = p.strip(" \n")
        reString = "{0}\n\n{1}".format(reString, cjkwrap.fill(p, 80))

    reString = reString.strip("\n")
    print(reString)

if __name__ == '__main__':
    main()
