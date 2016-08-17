
fd = open('./data/mxm_dataset_train.txt')
line = '#'
it = iter(fd)
while line[0] == '#':
    line = next(it)

lookup = dict(enumerate(line[1:].strip().split(',')))

import pandas as pd

songs = pd.read_csv('./data/mxm_779k_matches.txt', sep='<SEP>', comment='#', engine='python')
songs.columns = 'tid|artist name|title|mxm tid|artist_name|title'.split('|')
print(songs['tid'])

for line in it:
    song_id, _, *words = line.split(',')
    stmnt = {lookup[int(key)-1]:int(value) for key, value in dict(map(lambda x: x.split(':'), words)).items()}
    print(songs[songs['tid']==song_id]['artist name'].iloc[0])
    for word in stmnt:
        print("    :: {:10} :: {}".format(word, stmnt[word]))
    print()
