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

@db_session
def main():
    words = select(e for e in Word)
    songs = [(s.track_id, s.year) for s in select(e for e in Song if e.year)]
    for track_id, year in songs:
        words = ['{}:{}'.format(invert[w.word], c) for w, c in select((e.word, e.count) for e in Lyrics if e.track_id == track_id)]
        if words:
            print(','.join([track_id, str(year), ','.join(words)]))

main()
