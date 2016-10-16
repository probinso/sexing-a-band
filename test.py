import csv

# Import all the sources modules
from lyrico_sources.lyric_wikia    import donwload_from_lyric_wikia as wikia
from lyrico_sources.lyrics_n_music import donwload_from_lnm         as lnm
from lyrico_sources.az_lyrics      import donwload_from_az_lyrics   as az
from lyrico_sources.musix_match    import donwload_from_musix_match as mm
from lyrico_sources.lyricsmode     import donwload_from_lyricsmode  as lm

from lyrics_to_bow import lyrics_to_bow

from random import shuffle

class Song:
    def __init__(self, year, ident, artist, title):
        self.year    = year
        self.ident   = ident
        self.artist  = artist
        self.title   = title
        self.lyrics  = None
        self.sources = [wikia, lnm, az, mm, lm]
        self.error   = None
        self.bow     = None

    def download_lyrics(self):
        shuffle(self.sources)
        for site in self.sources:
            try:
                site(self)
                if self.lyrics:
                    self.bow = lyrics_to_bow(self.lyrics)
                    break
                
            except Exception as e:
                print(e)
                continue


def test():
    fd = open("./tracks_per_year.txt")
    for line in fd:
        song = Song(*line.strip().split('<SEP>'))
        song.download_lyrics()
        print(song.bow)
            


	
if __name__ == '__main__':
    test()
