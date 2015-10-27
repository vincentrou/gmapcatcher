
import math

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

zoom_level_pixelsize = (156543.0339280410
                        ,78271.5169640205
                        ,39135.7584820102
                        ,19567.8792410051
                        ,9783.9396205026
                        ,4891.9698102513
                        ,2445.9849051256
                        ,1222.9924525628
                        ,611.4962262814
                        ,305.7481131407
                        ,152.8740565704
                        ,76.4370282852
                        ,38.2185141426
                        ,19.1092570713
                        ,9.5546285356
                        ,4.7773142678
                        ,2.3886571339
                        ,1.1943285670
                        ,0.5971642835
                        ,0.2985821417
                        ,0.1492910709
                        ,0.0746455354)


def xy2colrow(xx, yy, zoom):
    pixelsize = zoom_level_pixelsize[zoom]  # meters / pixel
    pixelspertile = 256                                # pixels
    tilesize = pixelspertile * pixelsize               # meters

    tilecol = int(xx / tilesize)
    tilerow = int(yy / tilesize)
    return (tilecol, tilerow, tilesize)


def lonlat2xy(lon_deg, lat_deg):
  lon_rad = math.radians(lon_deg)
  lat_rad = math.radians(lat_deg)
  # rayon equatorial (demi grand axe) de l'ellipsoide
  a = 6378137.0 # in meters
  # Top Left Corner for PM TileMatrixSet
  x0 = -20037508
  y0 = 20037508
  x = a * lon_rad - x0
  y = -a * math.log(math.tan(lat_rad/2 + math.pi/4)) + y0
  return (x, y) # return coordinates in meters


def xy2lonlat(x, y):
  # rayon equatorial (demi grand axe) de l'ellipsoide
  a = 6378137.0 # in meters
  # Top Left Corner for PM TileMatrixSet
  x0 = -20037508
  y0 = 20037508
  lon_rad = (x + x0) / a
  lat_rad = (math.atan( math.exp( (y0 - y) / a) ) - math.pi/4) * 2
  lon_deg = math.degrees(lon_rad)
  lat_deg = math.degrees(lat_rad)
  return (lon_deg, lat_deg) # return coordinates in degrees