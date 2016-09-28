from __future__ import print_function
import sqlite3

# meta DB connection stuff ------------------------------------------------------
conn_tmdb = sqlite3.connect('data/track_metadata.db')

# returns the value at each row and sidesteps data type changing issues with sqlite3 later on
conn_tmdb.row_factory = lambda cursor, row: row[0]
cur = conn_tmdb.cursor()
# -------------------------------------------------------------------------------

output_file = 'data/full_output.csv'
train_file = 'data/mxm_dataset_train.txt'
test_file = 'data/mxm_dataset_test.txt'

def csv_song_writer(in_file, out_file):
    fd = open(in_file)
    line = '#'
    it = iter(fd)
    while line[0] == '#':
        line = next(it)

    # need to jump past 5000 words used in BOW
    line = next(it)

    while line:  
        try:
            # pulls out mxm track_id from line in text and uses help func to grab year  
            year = song_year_finder(line.strip().split(',')[0])

            song_data = list(line.strip().split(',')) 
            song_data.insert(2, str(year))

            # join list of strings and print output to csv 
            print(','.join(song_data), file=out_file)

            line = next(it)

        except StopIteration:
            print("done")
            break

# helper func to grab year from metadata DB 
def song_year_finder(track_id): 
    """get the year from metadata DB using track id"""
    sql_state = "SELECT year FROM songs WHERE track_id == ?;"
    sql_data = (track_id,)
    track_year = cur.execute(sql_state, sql_data).fetchone()

    return track_year

def main(): 
    with open(output_file, 'a') as fd:
        #csv_song_writer(train_file, fd)
        #csv_song_writer(test_file, fd)
main()

conn_tmdb.close()




