from __future__ import print_function

from pony.orm import *

meta_db = Database("sqlite", 'data/track_metadata.db', create_db=False)

class Song(meta_db.Entity):
    _table_ = "songs"
    track_id = PrimaryKey(str)
    title = Optional(str)
    #song_id = Required(str)
    #release = Required(str)
    #artist_id = Required(str)
    #artist_mbid = Required(str)
    artist_name = Required(str)
    #duration = Required(float)
    #artist_familiarity = Required(float)
    artist_hotttnesss = Required(float)
    year = Required(int)
    #track_7digitalid = Required(int)
    #shs_perf = Required(int)
    #shs_work = Required(int)

sql_debug(False)
meta_db.generate_mapping()

word_db = Database("sqlite", 'data/mxm_dataset.db', create_db=False)

class Word(word_db.Entity):
    _table_ = 'words'
    word = PrimaryKey(str)
    lyrics = Set('Lyrics')

class Lyrics(word_db.Entity):
    _table_ = 'lyrics'
    track_id = PrimaryKey(str)
    mxm_tid = Required(int)
    word = Required(str)
    count = Required(int)
    is_test = Required(int)
    word = Required(Word)

sql_debug(False)
word_db.generate_mapping()

fd = open('./data/mxm_dataset_train.txt')
line = '#'
it = iter(fd)
while line[0] == '#':
    line = next(it)

lookup = dict(enumerate(line[1:].strip().split(',')))
invert = {value:key + 1 for key, value in lookup.items()}

# changed to output_test to figure out missing songs  
filename = 'data/output_test.csv'

@db_session
def main():
    with open(filename, 'w') as fd:
        # Using a slice to grab all objects out of the generator object returned 
        words = select(e for e in Word)[:]

# --------------------------------------------------------------------------------------
# This block looks for the 171 bad key/value pairs in our lookup dict. For whatever reason it is throwing a key error
# anytime it looks up one of these values with: invert[item.word]. I noticed all the strings have '\' in them 
# I'm wondering if this is being counted as an escape character and causing the dict to throw a key error on lookup.

        error_strs = []
        bad_lookups = 0
        good_lookups = 0 

        for idx, item in enumerate(words):
            try: 
                print("item.word: {}, invert[item.word]: {}".format(item.word, invert[item.word]))
                good_lookups += 1
            except Exception:
                bad_lookups += 1
                error_strs.append((idx, item.word))
                continue

        print("Num good: {}, Num bad: {}".format(good_lookups, bad_lookups))
        print(error_strs)

        # used to check for lookup error 
        # print(invert['pr\xe8s'])

# ---------------------------------------------------------------------------------------------------   
# code below used to grab all our songs and their years from meta_db and lyrics_db  

        # songs = [(s.track_id, s.year) for s in select(e for e in Song if e.year)]

        # for track_id, year in songs:
        #     try: 
        #         words = ['{}:{}'.format(invert[w.word], c) for w, c in select((e.word, e.count) for e in Lyrics if e.track_id == track_id)]
           
        #     except Exception:
        #         continue  

        #     if words:
        #         print(','.join([track_id, str(year), ','.join(words)]), file=fd)

main()
