#!/usr/bin/env python2.7

from __future__  import print_function, absolute_import
from collections import defaultdict
import csv

import utility

def window(iterable, size):
    it  = iter(iterable)
    ret = [next(it) for _ in range(size)]

    yield ret
    for elm in it:
        ret = ret[1:] + [elm]
        yield ret


def group_years(reader):
    d = defaultdict(int)
    for A, B in window(reader, 2):
        year, title, artist = A[:3]
        if year[0] == '%':
            continue
        line = A[3:]

        next_year = B[0]
        for w, c in map(lambda s: s.split(':'), line[3:]):
            d[w] += int(c)

        if next_year != year:
            yield year, d
            d = defaultdict(int)

    yield year, d


def interface(ifname, ofname):
    with open(utility.make_resource(ofname), 'w') as dst:
        writer = csv.writer(dst)
        with open(utility.make_resource(ifname), 'r')  as src:
            reader = csv.reader(src)
            for year, counts in group_years(reader):
                line = ['{}:{}'.format(w, counts[w]) for w in counts]
                line.insert(0, year)

                writer.writerow(line)


def cli_interface():
    """
    by convention it is helpful to have a wrapper_cli method that interfaces
    from commandline to function space.
    """
    try:
        ifname, ofname = sys.argv[1], sys.argv[2]
    except:
        print("usage: {}  <inpath> <outpath>".format(sys.argv[0]))
        sys.exit(1)
    interface(ifname, ofname)


if __name__ == '__main__':
    cli_interface()
