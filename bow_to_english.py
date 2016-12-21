#!/usr/bin/env python

from __future__ import print_function, division, absolute_import

import csv
from enchant import Dict
from string import ascii_letters as letters, whitespace, punctuation, digits
from os import remove
import sys
import utility

from tempfile import TemporaryFile


def criteria(func, uniq, threshold=9/10):
    return sum(map(func, uniq))/len(uniq) > threshold


def ascii_check(word):
    score = lambda x: x in letters + whitespace + punctuation + digits
    return all(map(score, word))


D = Dict('en_US')
def word_check(word):
    return  D.check(word)


def interface(inpath, outpath):
    tmpfile = utility.make_resource('bow_english.csv.tmp')
    with open(utility.make_resource('bow_runner.csv')) as src:
        reader = csv.reader((line.replace('\0','') for line in src))
        words_store = set()

        with open(tmpfile, 'w') as dst:
            writer = csv.writer(dst)
            for line in reader:
                line = list(map(lambda s: s.replace(u'\xa0',' '), line))
                # date, title, artist, BOW
                uniq = {w.strip() for w, _ in map(lambda s: s.split(':'), line[3:])}

                if criteria(word_check, uniq, 6/10):
                    writer.writerow(line)
                    words_store = words_store.union(uniq)
                else:
                    print(line)
                    print()

    lookup = [(w,k) for k, w in enumerate(words_store, 1)]
    del words_store

    words  = [w for w, _ in lookup]
    words[0] = '%' + words[0]

    lookup = dict(lookup)

    with open(tmpfile, 'r') as src:
        reader = csv.reader(src)

        with open(utility.make_resource('bow_english.csv'), 'w') as dst:
            writer = csv.writer(dst)
            writer.writerow(words)
            del words
            for line in reader:
                # date, title, artist, BOW
                date, title, artist = line[:3]
                line = ['{}:{}'.format(lookup[w],c) for w, c in map(lambda s: s.split(':'), line[3:])]
                line = [date, title, artist] + line
                writer.writerow(line)
    remove(tmpfile)


def cli_interface():
    """
    by convention it is helpful to have a wrapper_cli method that interfaces
    from commandline to function space.
    """
    try:
        inpath, outpath = sys.argv[1], sys.argv[2]
    except:
        print("usage: {}  <inpath> <outpath>".format(sys.argv[0]))
        sys.exit(1)
    interface(inpath, outpath)


if __name__ == '__main__':
    cli_interface()
