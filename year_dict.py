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


with open('/media/terra/UndecidedTeam/bow_english_year.csv', 'w') as dst:
    writer = csv.writer(dst)
    with open('/media/terra/UndecidedTeam/bow_english.csv', 'r')  as src:
        reader = csv.reader(src)
        for year, counts in group_years(reader):
            line = ['{}:{}'.format(w, counts[w]) for w in counts]
            line.insert(0, year)

            writer.writerow(line)

