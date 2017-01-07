#!/usr/bin/env python2.7

from __future__  import print_function, absolute_import
from collections import defaultdict
import csv

#import utility
import sys




# input looks like: 
# 1924, song title, artist, song vector

# output we want 
# 1st line: %year:bin_value, year:bin_value ----> so you can read from it later to make a dict
# year, bin, song vector 

def window(iterable, size):
    it  = iter(iterable)
    ret = [next(it) for _ in range(size)]

    yield ret
    for elm in it:
        ret = ret[1:] + [elm]
        yield ret


def make_bins_dict(bucket_size):
    """Split group of years into buckets, make a dict year:bucket_of_year, 
    then write string representing dict to first row in csv"""
    start, end = 1920, 2030
    bucket_increment = 0

    range_list = []

    for low, high in window(range(start, end, bucket_size), 2):


        

        
        range_list.append([low, high, bucket_increment]) 
        bucket_increment += 1

    print(range_list)

    bucket_dict = defaultdict()

    for item in range_list: 
        for year in range(item[0], item[1]):
            bucket_dict[year] = item[2]

    test = bucket_dict.items()

    final = ["{}:{}".format(item[0], item[1]) for item in test]
    final_out = '%'+','.join(final)

    print(final_out.split(','))






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
    # cli_interface()
    make_bins_dict(10)






