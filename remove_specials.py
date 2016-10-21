#!/usr/bin/env python

from __future__ import print_function, division
import csv
from enchant import Dict
from string import ascii_letters as letters, whitespace, punctuation, digits


def criteria(func, uniq, threshold=9/10):    
    return sum(map(func, uniq))/len(uniq) > threshold

def ascii_check(word):
    score = lambda x: x in letters + whitespace + punctuation + digits
    return all(map(score, word))

D = Dict('en_US')
def word_check(word):
    return  D.check(word)

if __name__ == '__main__':
    with open('/media/terra/UndecidedTeam/bow_runner.csv') as src:
        reader = csv.reader(src)
        with open('/media/terra/UndecidedTeam/bow_english.csv', 'w') as dst:
            writer = csv.writer(dst)
            for line in reader:
                # date, title, artist, BOW
                uniq = {w for w, _ in map(lambda s: s.split(':'), line[3:])}

                if criteria(word_check, uniq, 6/10):
                    writer.writerow(line)
                else:
                    print(line)
                    print()
