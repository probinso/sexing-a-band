#!/usr/bin/env python2.7

from __future__  import print_function, absolute_import
from collections import defaultdict
import csv

import utility
import sys


def make_bins_dict(bucket_size):
    """split group of years into buckets, make a dict year:bucket_of_year, 
    then write string representing dict to first row in csv"""

    # need to go to 2021 to make sure years after 2010 are included in dict 
    start, end = 1920, 2021
    bucket_increment = 0
    bucket_dict = defaultdict()

    for low, high in utility.window(range(start, end, bucket_size), 2): 
        for year in range(low, high):
            bucket_dict[year] = bucket_increment

        bucket_increment += 1

    return bucket_dict


def interface(ifname, ofname):
    """decide how many bins you want the training set broken into by
       entering number in year_bins_dict"""

    year_bins_dict = make_bins_dict(10)

    with open(utility.make_resource(ofname), 'w') as dst:
        writer = csv.writer(dst)
        with open(utility.make_resource(ifname), 'r')  as src:
            reader = csv.reader(src)

            for song in reader:
                # filter out first line with words in corpus, starts with %
                if song[0][0] == '%':
                    continue 
                
                line = song[3:]
                year = int(song[0])
                line.insert(0, year)
                line.insert(1, year_bins_dict[year])

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

 






