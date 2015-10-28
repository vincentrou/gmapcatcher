## @package gmapcatcher.mapServers.Geoportail
# All the interaction with www.geoportail.gouv.fr
#
# Copyright : IGN France
#
# See http://www.geoportail.gouv.fr for details.
#
import re
import urllib

### Layer names
#
layers = ('GEOGRAPHICALGRIDSYSTEMS.MAPS', 'ORTHOIMAGERY.ORTHOPHOTOS')

clef = None

from gmapcatcher.mapConst import MAP_MAX_ZOOM_LEVEL

## Returns a template URL for the Stamen
def layer_url_template():
    global clef
    if clef is None:
        #script = urllib.urlopen ("http://www.geoportail.gouv.fr/js/config/swfParam.js")
        #s = script.read()
        #script.close()
        #p = re.compile(r"var\s*KEY2D\s*=\s*\"(\S*)\"")
        #clef = p.findall(s)[0]
        clef = '3vczznk2bngd821d4jc3c9fd'
        #print('clef : '+clef)
    return  'https://wxs.ign.fr/' + clef + '/wmts?SERVICE=WMTS&VERSION=1.0.0&EXCEPTIONS=text/xml&REQUEST=GetTile&LAYER=%s&STYLE=normal&FORMAT=image/jpeg&TILEMATRIXSET=PM&TILEMATRIX=%i&TILEROW=%i&TILECOL=%i'
    #return 'http://wxs.ign.fr/c19uzdyrb5yttrgmhr2mmyij/wmts?SERVICE=WMTS&VERSION=1.0.0&EXCEPTIONS=text/xml&REQUEST=GetTile&LAYER=GEOGRAPHICALGRIDSYSTEMS.MAPS&STYLE=normal&FORMAT=image/jpeg&TILEMATRIXSET=PM&TILEMATRIX=2&TILEROW=1&TILECOL=2'

## Returns the URL to the Geoportail tile
def get_url(counter, coord, layer_name, conf):
    return layer_url_template() % (layers[layer_name], MAP_MAX_ZOOM_LEVEL - coord[2], coord[1], coord[0])