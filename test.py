
from __future__ import print_function
import csv

# Import all the sources modules
from lyrico_sources.lyric_wikia    import donwload_from_lyric_wikia as wikia
from lyrico_sources.lyrics_n_music import donwload_from_lnm         as lnm
from lyrico_sources.az_lyrics      import donwload_from_az_lyrics   as az
from lyrico_sources.musix_match    import donwload_from_musix_match as mm
from lyrico_sources.lyricsmode     import donwload_from_lyricsmode  as lm

from lyrics_to_bow import lyrics_to_bow

from random import shuffle

from collections import defaultdict

class Song:
    sources = [wikia, lnm, az, mm, lm]
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
    with open("/media/terra/UndecidedTeam/tracks_per_year.txt") as fd:
        with open("/media/terra/UndecidedTeam/bow_runner.csv", 'w') as gd:
            w = csv.writer(gd)

            for line in fd:
                song = Song(*line.strip().split('<SEP>'))
                song.download_lyrics()
                if song.bow:
                    bow  = [':'.join([str(word), str(song.bow[word])]) for word in song.bow]
                    meta = [song.year, song.title, song.artist]
                    w.writerow(meta + bow)
                print(song.scores)

    with open("scores.txt", 'wb') as fd:
        for i in Song.scores:
            print(i, sum(scores[i]), sum(map(lambda x: 1 - x, scores[i])), file=fd)


if __name__ == '__main__':
    test()

