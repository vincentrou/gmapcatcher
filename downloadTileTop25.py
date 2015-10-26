#!/usr/bin/env python

# Download one single jpeg tile of 256x256 pixels from geoportail at zoom level 15 (Top25) given lon/lat in decimal degrees.
# Usage: ./downloadTileTop25.py lon lat (in decimal degree)"
# Sample (col de Marraut): ./downloadTileTop25.py 0.052279 42.829535 

import sys
import math
import urllib2

APIKEY = "3vczznk2bngd821d4jc3c9fd"
REFERER = ""
LAYER = "GEOGRAPHICALGRIDSYSTEMS.MAPS"

# usage
if len(sys.argv) != 3 :
  print sys.argv[0], "lon lat (in decimal degree)"
  sys.exit(2)

LON= sys.argv[1]
LAT= sys.argv[2]

print "LON=", LON, "LAT=", LAT

# Top25 zoom level
ZOOM="15"  

##### Compute (COL,ROW) from (LON,LAT) for ZOOM=15 #####

# Documentation: http://api.ign.fr/tech-docs-js/fr/developpeur/wmts.html
# EPSG:3857 ("WGS 84 / Pseudo-Mercator")

# The GetCapabilities request gives the following values for EPSG:3857 at zoom level 15:

# <MinTileRow>10944</MinTileRow>
# <MaxTileRow>21176</MaxTileRow>
# <MinTileCol>163</MinTileCol><MaxTileCol>31695</MaxTileCol>
# <ScaleDenominator>17061.8366707982724577</ScaleDenominator>
# <TopLeftCorner>-20037508 20037508</TopLeftCorner>
# <TileWidth>256</TileWidth>
# <TileHeight>256</TileHeight>
# <MatrixWidth>32768</MatrixWidth>
# <MatrixHeight>32768</MatrixHeight></TileMatrix>


def lonlat2xy(lon_deg, lat_deg):
  lon_rad = math.radians(lon_deg)
  lat_rad = math.radians(lat_deg)
  # rayon equatorial (demi grand axe) de l'ellipsoide
  a = 6378137.0 # in meters
  x = a * lon_rad
  y = a * math.log(math.tan(lat_rad/2 + math.pi/4))
  return (x, y) # return coordinates in meters


# convert (lon,lat) to (x,y) web-mercator coordinates in meters 
lon = float(sys.argv[1])
lat = float(sys.argv[2])
(x, y) = lonlat2xy(lon,lat)

# Top Left Corner for ZOOM=15
x0 = -20037508 
y0 = 20037508

# Shift coordinates according to the "Top Left Corner"
xx = x-x0
yy = y0-y

# Scale Denominator for ZOOM=15
scaledenominator = 17061.8366707982724577   # scale 1:scaledenominator

# The standardized rendering pixel size is defined to be 0.28mm x 0.28mm.
renderingpixelsize = 0.00028                       # meters / rendering pixel ???
pixelsize = renderingpixelsize * scaledenominator  # meters / pixel
pixelspertile = 256                                # pixels
tilesize = pixelspertile * pixelsize               # meters

tilecol = int(xx / tilesize)
tilerow = int(yy / tilesize)

##### Generate URL from (COL,ROW,ZOOM) for GetTile request #####

COL = str(tilecol)
ROW = str(tilerow)

print "COL=", COL, "ROW=", ROW, "ZOOM=", ZOOM

URL = "http://wxs.ign.fr/"+APIKEY+"/geoportail/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER="+LAYER+"&STYLE=normal&TILEMATRIXSET=PM&TILEMATRIX="+ZOOM+"&TILEROW="+ROW+"&TILECOL="+COL+"&FORMAT=image/jpeg"  

print "URL=", URL

FILE = "zoom"+ZOOM+"-row"+ROW+"-col"+COL+".jpeg"

print "FILE=", FILE

##### launch HTTP request and save output #####

passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, URL, 'vincent-rou@hotmail.fr', '091186')
urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))
req = urllib2.Request(URL)
#req.add_header('Referer', REFERER)
ans = urllib2.urlopen(req)
output = open(FILE,'wb')
output.write(ans.read())
output.close()

# EOF