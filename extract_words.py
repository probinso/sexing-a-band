#!/usr/bin/env python

from __future__ import print_function, division
import csv

with open('/media/terra/UndecidedTeam/bow_english.csv', 'w') as songs_fd:
    reader = csv.reader(songs_fd)
    words = set()
    for line in reader:
        d = dict(map(lambda s: s.split(':'), line[3:]))
        _ = map(words.add, d)
    print(words)
