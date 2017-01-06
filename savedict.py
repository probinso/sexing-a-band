
import utility
import pickle
import sys


def savedict(filename, dstname='word_lookup.pkl'):
    resource = utility.make_resource(filename)
    with open(resource, 'r') as fd:
        it = iter(fd)
        dline = next(it)
        stri = lambda s: s.strip()
        tump = dict(enumerate(map(stri, dline[1:].split(',')), 1))
        d = {word : key for key, word in tump.items()}

    print(len(tump) == len(d))
    return;
    dstpath = utility.make_resource(dstname)
    with open(dstpath, 'wb') as fd:
        pickle.dump(d, fd)
    return dstpath


def cli_interface():
    """
    by convention it is helpful to have a wrapper_cli method that interfaces
    from commandline to function space.
    """
    try:
        ifname, ofpath = sys.argv[1], sys.argv[2]
    except:
        print("usage: {}  <ifname> <ofpath>".format(sys.argv[0]))
        sys.exit(1)
    savedict(ifname, ofpath)


if __name__ == '__main__':
    cli_interface()
