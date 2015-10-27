#!/usr/bin/env python

# Download one single jpeg tile of 256x256 pixels from geoportail at zoom level 15 (Top25) given lon/lat in decimal degrees.
# Usage: ./downloadTileTop25.py lon lat (in decimal degree)"
# Sample (col de Marraut): ./downloadTileTop25.py 0.052279 42.829535 

import sys
import math
import urllib2
import os
import mapviz.lonlat2tilecoord as lonlat2tilecoord
from mapviz.get_tile import get_tile
import utm


# usage
if len(sys.argv) < 3 :
  print sys.argv[0], "lon lat (in decimal degree)"
  sys.exit(2)
if len(sys.argv) > 3 and len(sys.argv) != 5:
  print sys.argv[0], "lon lat (in decimal degree) start_level nb_level"
  sys.exit(2)

start_level = int(sys.argv[3])
nb_level = int(sys.argv[4])

# Top25 zoom level
ZOOM="15"

# convert (lon,lat) to (x,y) web-mercator coordinates in meters
lon = float(sys.argv[1])
lat = float(sys.argv[2])

(x, y) = lonlat2tilecoord.lonlat2xy(lon, lat)
(tilecol, tilerow, tilesize) = lonlat2tilecoord.xy2colrow(x, y, start_level)

(orig_lon, orig_lat) = lonlat2tilecoord.xy2lonlat((tilecol)*tilesize, (tilerow)*tilesize)
#print("orig_lon "+str(orig_lon)+" orig_lat "+str(orig_lat))
u = utm.from_latlon(orig_lat, orig_lon)
print("0,0")
print(u)
(orig_lon, orig_lat) = lonlat2tilecoord.xy2lonlat((tilecol+1)*tilesize, (tilerow+1)*tilesize)
#print("orig_lon "+str(orig_lon)+" orig_lat "+str(orig_lat))
u = utm.from_latlon(orig_lat, orig_lon)
print("max,max")
print(u)
(orig_lon, orig_lat) = lonlat2tilecoord.xy2lonlat((tilecol)*tilesize, (tilerow+1)*tilesize)
#print("orig_lon "+str(orig_lon)+" orig_lat "+str(orig_lat))
u = utm.from_latlon(orig_lat, orig_lon)
print("0,max")
print(u)

for l in range(nb_level):
    # convert (lon,lat) to (x,y) web-mercator coordinates in meters
    lon = float(sys.argv[1])
    lat = float(sys.argv[2])

    (x, y) = lonlat2tilecoord.lonlat2xy(lon, lat)
    (tilecol, tilerow, tilesize) = lonlat2tilecoord.xy2colrow(x, y, start_level+l)

    #### Generate URL from (COL,ROW,ZOOM) for GetTile request #####
    for i in range(int(math.pow(2,l))):
        for j in range(int(math.pow(2,l))):
            #print("col "+str(tilecol+i)+" row " +str(tilerow+j)+" zoom " +str(start_level+l))
            #get_tile(tilecol, i, tilerow, j, start_level, l, nb_level)
            pass

# EOF
