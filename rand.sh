#!/usr/bin/env bash

DST=/media/terra/UndecidedTeam
sort -R ${DST}/tracks_per_year.txt | head -n 200 | sort > ${DST}/test/tracks_per_year.txt
