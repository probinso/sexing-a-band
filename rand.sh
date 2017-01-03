#!/usr/bin/env bash

DST=/media/terra/UndecidedTeam
sort -R ${DST}/tracks_per_year.txt | head -n 500 | sort > ${DST}/test/tracks_per_year.txt
