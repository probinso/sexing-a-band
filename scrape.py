
from __future__ import print_function, absolute_import
import csv

# Import all the sources modules
from lyrico_sources.lyric_wikia    import donwload_from_lyric_wikia as wikia
#from lyrico_sources.lyrics_n_music import donwload_from_lnm         as lnm
#from lyrico_sources.az_lyrics      import donwload_from_az_lyrics   as az
#from lyrico_sources.musix_match    import donwload_from_musix_match as mm
from lyrico_sources.lyricsmode     import donwload_from_lyricsmode  as lm

from lyrics_to_bow import lyrics_to_bow

from random import shuffle

from collections import defaultdict

import utility

class Song:
    sources = [wikia, lm]
    scores  = defaultdict(int)
    def __init__(self, year, ident, artist, title):
        self.year    = year
        self.ident   = ident
        self.artist  = artist
        self.title   = title
        self.lyrics  = None
        self.error   = None
        self.bow     = None

    def download_lyrics(self):
        shuffle(self.sources)
        for site in self.sources:
            try:
                site(self)
                if self.lyrics:
                    self.bow = lyrics_to_bow(self.lyrics)
                    self.scores[site.__name__] += 1
                    break

            except Exception as e:
                print(e)
                continue

import csv
def test():
    with open(utility.make_resource('tracks_per_year.txt')) as search_tracks:
        in_iter = iter(search_tracks)
        with open(utility.make_resource('bow_runner.csv'), 'a') as bag_of_words:
            w = csv.writer(bag_of_words)
            with open(utility.make_resource('processed.txt')) as processed:
                for skip in processed:
                    _ = next(in_iter)

            with open(utility.make_resource('processed.txt'), 'a') as processed:
                p = csv.writer(processed)
                for read in in_iter:
                    year, ident, artist, title = read.strip().split('<SEP>')

                    song = Song(year, ident, artist, title)
                    song.download_lyrics()
                    succ = bool(song.bow)
                    if succ:
                        bow  = [':'.join([str(word), str(song.bow[word])]) for word in song.bow]
                        meta = [song.year, song.title, song.artist]
                        w.writerow(meta + bow)
                    p.writerow([year, ident, artist, title, succ])
                    print(song.scores)
                    processed.flush()
                    bag_of_words.flush()

    with open("scores.txt", 'wb') as fd:
        for i in Song.scores:
            print(i, sum(scores[i]), sum(map(lambda x: 1 - x, scores[i])), file=fd)


if __name__ == '__main__':
    test()

