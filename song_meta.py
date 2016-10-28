import csv 
from enchant import Dict
import re 
import sqlite3


def db_setup():
    # meta DB connection stuff
    conn_tmdb = sqlite3.connect('data/track_metadata.db')
    cur = conn_tmdb.cursor()

    return conn_tmdb

# D = Dict('en_US')
# def word_check(word):
#     return  D.check(word)

# def criteria(func, uniq, threshold=5/10):    
#     return sum(map(func, uniq))/len(uniq) > threshold


def data_base():
    """select all artists in DB and write their names with all their songs names and dates to csv"""

    with open('/media/terra/UndecidedTeam/data/song_title_year.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        error_count = 0 

        sql_state = "SELECT artist_id, artist_name FROM songs;"
        artist_name_ids = cur.execute(sql_state,).fetchall()

        for artist in artist_name_ids:
            sql_artist_id = (artist[0], )
            artist_name = artist[1]

            sql_state_songs = "SELECT title, year from songs where artist_id == ?;"
            artist_songs = cur.execute(sql_state_songs, sql_artist_id).fetchall()

            for song in artist_songs:

                # filer out songs with no date 
                if song[1] == 0:
                    continue

                # --------------------------------------------------------------
                # ************** super slopy and needs to be cleaned up **************
                # basically gets rid of parens in song titles, doesn't catch all but gets most 
                try:
                    # matches title before parens ex: 'Allhot (feat. Nadsroic)' only matches Allhot 
                    title = re.search('^[^\(]+', song[0]).group(0) 
                except Exception:
                    try:
                        # matches title after parens ex: '(Looking For) The Heart Of Saturday' 
                        # only matches ') The Heart Of Saturday' then slice from 2nd element
                        title = re.search('\).*', song[0]).group(0)[2:]
                        
                    except Exception:
                        print(song[0])
                        continue 
                # --------------------------------------------------------------
                # check to sort out non english songs - this still has issues with figuring out 
                # if a song is english or not, may need to look at lyrics 
                #

                # words = title.split()

                # print(title)
                # print(criteria(word_check, words))               
                # --------------------------------------------------------------

                try:
                    if int(song[1]) < 1995:
                        line = ["{}, {}, {}".format(artist_name, title, song[1])]
                        print(line)
                    else: 
                        continue
                except Exception:
                    error_count += 1

                writer.writerow(line)

    print("num songs with errors: {}".format(error_count))

if __name__ =='__main__':
    conn_tmdb = db_setup()
    cur = conn_tmdb.cursor()

    data_base()

    conn_tmdb.close()