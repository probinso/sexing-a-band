from pony.orm import *

meta_db = Database("sqlite", 'data/track_metadata.db', create_db=False)

class Song(meta_db.Entity):
    _table_ = "songs"
    track_id = PrimaryKey(str)
    title = Required(str)
    song_id = Required(str)
    release = Required(str)
    artist_id = Required(str)
    artist_mbid = Required(str)
    artist_name = Required(str)
    duration = Required(float)
    artist_familiarity = Required(float)
    artist_hotttnesss = Required(float)
    year = Required(int)
    track_7digitalid = Required(int)
    shs_perf = Required(int)
    shs_work = Required(int)

sql_debug(False)
meta_db.generate_mapping()



