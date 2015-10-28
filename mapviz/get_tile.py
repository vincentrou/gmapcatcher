import os
import urllib2

APIKEY = "3vczznk2bngd821d4jc3c9fd"
REFERER = ""
# maximum level = 18; level = 16 : carte topo 25
LAYER = "GEOGRAPHICALGRIDSYSTEMS.MAPS"
# maximum level = 19
#LAYER = "ORTHOIMAGERY.ORTHOPHOTOS"

## Checks if a directory exist if not it will be created
def check_dir(strPath, strSubPath=None):
    if (strSubPath is not None):
        strPath = os.path.join(strPath, strSubPath)
    if not os.path.isdir(strPath):
        try:
            os.makedirs(strPath)
        except Exception:
            print 'Error! Can not create directory:'
            print '  ' + strPath
    return strPath

def get_tile(tilecol, inc_col, tilerow, inc_row, ref_zoom, inc_zoom, nb_zoom):
    #### Generate URL from (COL,ROW,ZOOM) for GetTile request #####
    col = str(tilecol+inc_col)
    row = str(tilerow+inc_row)
    zoom = str(ref_zoom+inc_zoom)

    print "col=", col, "row=", row, "zoom=", zoom

    URL = "http://wxs.ign.fr/"+APIKEY+"/geoportail/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER="+LAYER+"&STYLE=normal&TILEMATRIXSET=PM&TILEMATRIX="+zoom+"&TILEROW="+row+"&TILECOL="+col+"&FORMAT=image/jpeg"

    #print "URL=", URL

    directory = "layer"+str(nb_zoom -1 -inc_zoom)

    file = "tile%05dx%05d.jpg"% (inc_row, inc_col)
    file = os.path.join(directory, file)
    check_dir(directory)
    print "FILE=", file

    ##### launch HTTP request and save output #####

    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, URL, 'vincent-rou@hotmail.fr', '091186')
    urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))
    req = urllib2.Request(URL)
    #req.add_header('Referer', REFERER)
    ans = urllib2.urlopen(req)
    output = open(file,'wb')
    output.write(ans.read())
    output.close()