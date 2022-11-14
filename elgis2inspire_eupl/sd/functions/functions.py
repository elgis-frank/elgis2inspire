#-------------------------------------------------------
# Datei sd.functions.py Version 1.01 
#
#  Programming by eLGIS
#               
#      Copyright (C) by elgis ( https://elgis.de ) 2022
# Diese Datei ist Bestandteil der Software elgis2inspire, erhältlich unter https://github.com/elgis-frank/elgis2inspire .
# Diese Software wird unter der European Union Public Licence (EUPL-1.2) bereitgestellt. Bitte beachten Sie die Bestimmungen der Lizenz, insbesondere
# zur Bereitstellung und Nutzung der Software und zum Haftungsausschluss. Die Lizenz ist in allen Amtssprachen der EU veröffentlicht unter https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
# 
#--------------------------------------------------------

import subprocess
import sqlite3
import spatialite
import shlex
import datetime
import os, sys, stat, shutil
from sqlite3 import OperationalError
from urllib import request as urlrequest, error as uerror
from pathlib import Path
from django.conf import settings
from main.functions.functions import writeDok
from main.functions.sql2spatialite import  write2SQL, write2So, write2spatialite, read2spatial, readsoSQL, readSQL

p = settings.ELGIS2INSPIRE__PATH
path = p['dbase']


def handle_uploaded_sdfile(f, data_select, nmsp, name, fid):
    try:
        fileweg(f)
        with open(path+'/upload/'+f.name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        ergebnis = loadsdGeo(path+'/upload/'+f.name, data_select, nmsp, name, fid)
    except OSError:
        ergebnis = 'Der file ' + f +' konnte nicht geöffnet werden'
    fileweg(f)
    return ergebnis
    
def loadsdGeo(datei, data_select, nmsp, name, fid):
    # geojson mit shellscript laden
    param = 'geojson-to-sqlite '+path+'db.sqlite3 sd_in ' + datei + ' --spatialite'
    args = shlex.split(param)
    subprocess.run(args)
    sqltest = 'select ST_GeometryType(GEOMETRY) from sd_in;'
    r = read2spatial(sqltest)
    if r[0][0] == 'POINT':
        sqindex = "select CreateSpatialIndex('sd_in','GEOMETRY');"
        write2spatialite(sqindex)
        #da geojson immer epsg:2446 dieser aber nicht, verbessern
        param = (1, 3035, 'sd_in')
        sql = '''update geometry_columns set geometry_type = ?, srid = ?  where f_table_name = ?'''
        write2SQL(sql, param)
        sql2 = 'update sd_in set geometry = SetSRID(geometry, 3035);'
        write2spatialite(sql2)
        #Aufbau inspire
        ergebnis1 = testsd(name, fid)
        if ergebnis1 == 'die Geodaten wurden erfolgreich geladen':
            ergebnis2 = makeRaster(data_select, nmsp, name, fid)
            if ergebnis2 == 'Raster ok':
                ergebnis = writeDok('SpeciesDistribution',data_select)
                rooming()
                #ergebnis = 'die Geodaten wurden erfolgreich geladen'
                return ergebnis
            else:
                #rooming()
                return ergebnis2
        else:
            rooming()    
            return ergebnis1
    else:
        rooming()
        return 'Der Datensatz beinhaltet keine Punktgeometrie, bitte überprüfen'
    

def testsd(name, fid):
    sql = "PRAGMA table_info('sd_in')"
    fcol = []
    col = []
    frage = [name, fid]
    r = readsoSQL(sql)
    sqlgeom = "select st_intersects(a.geometry, b.GEOMETRY) from sd_in as a, rlp as b;"
    match = read2spatial(sqlgeom)
    testmatch = 'True'
    for i in match:
        if i[0] == 0:
            testmatch = 'False'
    for z in r:
        col.append(z[1])
    for q in frage:
        if not q in col:
            fcol.append(q)
    if fcol:
        ans = ''
        for i in fcol:
            ans = ans +i+', '
        return 'Fehler! Die Spalten: ' + ans+ 'fehlen'
    elif testmatch == 'False':
        return 'Die Daten liegen nicht in Rheinland-Pfalz oder es wurde ein falsches Koordinatensystem verwendet'
    else:
        return 'die Geodaten wurden erfolgreich geladen'

def fileweg(f):
    if os.path.exists(path+'upload/'+f.name):
        os.remove(path+'upload/'+f.name)#print("Content-type: text/html
    
    

def allefileweg(sddi):
    filel = [path+'dok/sd_d'+sddi+'.map',path+'dok/sd_d'+sddi+'_wms.map',path+'python/sd_d'+sddi+'_wfs',path+'python/sd_d'+sddi+'_wms']
    for f in filel:
        if os.path.exists(f):
            os.remove(f)
    return "alle files weg"


def dels(sddi):
    sql1 = 'delete from sd_speciesdistributionunit where sddi =?;'
    write2SQL(sql1, (sddi,))
    sql = 'select count(*) from sd_speciesdistributionunit where sddi=?;'
    z = readSQL(sql, (sddi,))
    if z[0][0] == 0:
        ergebnis = allefileweg(sddi)
        if sddi != '1':            
            if ergebnis == "alle files weg":
                return 'die Daten wurden gelöscht'
        else:
            return 'Die Artendaten wurden gelöscht, der dataset bleibt erhalten'
    else:
        return 'Oops irgendwas ist schief gegangen'
    
def fillguid(data_select, nmsp):
    sql00 = "create index if not exists arten_idx on sd_artenliste(name)"
    sql001 = "create index if not exists spec_idx on sd_speciesdistributionunit(referenceSpeciesName)"
    sql0 = "select distinct(name) from interclean;"
    sql1 = "insert into sd_artenliste (name,guid) values (?,?);"
    sql11 = "update interclean set guid = (select guid as gui from sd_artenliste where interclean.name = sd_artenliste.name)"
    sql21 = "delete from interclean where guid is Null;"
    sql22 = "insert into sd_speciesdistributionunit (sddi, namespace , referenceSpeciesId , referenceSpeciesScheme , referenceSpeciesName, cellcode) select '"+ data_select +"', '"+ nmsp +"', 'http://inspire.ec.europa.eu/codelist/EuNomenCodeValue/'||guid, 'http://inspire.ec.europa.eu/codelist/ReferenceSpeciesSchemeValue/eunomen', name, cellcode from interclean;"
    sql3 = "delete from sd_speciesdistributionunit where referenceSpeciesId is Null;"
    sql4 = "drop table if exists interclean;"
    sql5 =  "update sd_speciesdistributionunit set the_geom = (select rlp_10km.GEOMETRY as geo from rlp_10km where rlp_10km.cellcode = sd_speciesdistributionunit.cellcode);"
    sql6 = "update sd_speciesdistributionunit set localID = sdid where sddi = "+data_select+";"
    #nachsehen, wo noch kein guid vorhanden ist
    write2So(sql00)
    write2So(sql001)
    r = readsoSQL(sql0)
    if r:
        for i in r:
            art = i[0]
            art2 = art.replace("ä", "ae")
            art1 = art2.replace(" ", "%20") #Leerzeichen beseitigen
            #request = "http://www.eu-nomen.eu/portal/rest/PESIGUIDByName/" + art1
            #proxy_host = '83.243.48.15:8080'    # host and port of your proxy
            url = "http://www.eu-nomen.eu/portal/rest/PESIGUIDByName/" + art1

            req = urlrequest.Request(url)
            #req.set_proxy(proxy_host, 'http')

            try:
                with urlrequest.urlopen(req) as response:
                    guid = response.read()
            except uerror.URLError as e:
                pass
            print('guid = '+ guid.decode("UTF-8"))
            if guid != None and guid.decode("UTF-8") != '':
                p = guid.decode("UTF-8")
                p = p.replace('"','')
                intab = (art, p,)
                write2SQL(sql1, intab)
            else:
                faultg(i[0])
        write2So(sql11)
        write2So(sql21)
        write2spatialite(sql22)
        write2So(sql3)
    write2So(sql4)
    write2spatialite(sql5)
    write2So(sql6)
    return 'guid ok'    

    
def delfaultguid():
    sql = "delete from sd_faultguid;"
    write2So(sql)
    return 'die Liste mit Arten ohne guid wurde gelöscht'




def makeRaster(data_select, nmsp, name, fid):
    sql = ["drop table if exists inter;","create table inter (intid Integer primary key, featureid text, cellcode text, name text, zus text);", "insert into  inter (featureid, cellcode, name) select sd_in."+fid+", rlp_10km.cellcode, sd_in."+name+" from rlp_10km, sd_in where st_within(sd_in.geometry, rlp_10km.GEOMETRY) = 1;",
    "update inter set zus = cellcode||name;","drop table if exists interclean;","create table interclean (incid Integer primary key,  cellcode text, name text, zus text, guid text, pruef Integer);",
"insert into interclean ( zus) select distinct zus from inter;","create  INDEX interidx on inter(zus);","create  INDEX intercleanidx on interclean(zus);","create INDEX intercleanname on interclean(name);",
"update interclean set name = (select inter.name as inam from inter where inter.zus = interclean.zus);","update interclean set cellcode = (select inter.cellcode as cel from inter where inter.zus = interclean.zus);",
"update interclean set pruef = (select pruef as p from sd_faultguid Where sd_faultguid.name = interclean.name);","delete from interclean where pruef = 1;","update interclean set guid = (select sd_artenliste.guid as gu from sd_artenliste where sd_artenliste.name = interclean.name);",
"insert into sd_speciesdistributionunit (sddi, namespace , referenceSpeciesId , referenceSpeciesScheme , referenceSpeciesName, cellcode) select '"+ data_select +"', '"+ nmsp +"', 'http://inspire.ec.europa.eu/codelist/EuNomenCodeValue/'||guid, 'http://inspire.ec.europa.eu/codelist/ReferenceSpeciesSchemeValue/eunomen', name, cellcode from interclean where guid is not null;",
"delete from interclean where guid is not null;","drop table if exists inter;",]
    
    try:
        con = sqlite3.connect(path + 'db.sqlite3')
        con.enable_load_extension(True)
        con.execute('SELECT load_extension("mod_spatialite")') 
        cur = con.cursor()
        for i in sql:
            cur.execute(i)
            con.commit()
        con.close()
        ergebnis = fillguid(data_select, nmsp)
        if ergebnis == 'guid ok':
            return 'Raster ok'
        else:
            return "Ein Fehler bei guid ist aufgetreten"
    except OperationalError:
        return 'Ein Fehler mit der Datenbank ist aufgetreten'


    
#nachstehende Funktion entfernt Datensätze für die keine guid ermittelt werden kann
def faultg(n):
    sql0 = "select name from sd_faultguid where name =?;"
    row = readSQL(sql0, (n,))
    if row:
        return 'Schon vorhanden'
    else:
        sql1 = "insert into sd_faultguid (name) values (?)"
        write2SQL(sql1, (n,))
        return 'Eintrag neu'#print("Content-type: text/html

def addCapabilities(lid):
    sqlcount = "select count(*) from sd_speciesdistributionunit where  sddi =?;"
    sqln = '''select ows_inspire_temporal_reference, ows_inspire_mpoc_name, ows_inspire_mpoc_email, ows_inspire_metadatadate, ows_inspire_resourcelocator, contactperson, ows_hoursofservice,
    ows_contactinstructions, contactposition, contactvoicetelephone, ows_contactfacsimiletelephone, contactelectronicmailaddress, postcode, address, city, stateorprovince, addresstype,
    ows_service_onlineresource, ows_role, inspirelayer, contactorganisation, sddi from main_capabilities where sddi = ?;'''
    r = readSQL(sqln,(1,))
    ins = (r[0][0],r[0][1],r[0][2],r[0][3],r[0][4],r[0][5],r[0][6],r[0][7],r[0][8],r[0][9],r[0][10],r[0][11],r[0][12],r[0][13],r[0][14],r[0][15],r[0][16],r[0][17],r[0][18],r[0][19],r[0][20],lid,'bitte ausfüllen', 'bitte ausfüllen', 'bitte ausfüllen', 'SGD Nord als Lanis Z', 'https://sgdnord.rlp.de')
    sqlin = '''insert into main_capabilities (ows_inspire_temporal_reference, ows_inspire_mpoc_name, ows_inspire_mpoc_email, ows_inspire_metadatadate, ows_inspire_resourcelocator, 
    contactperson, ows_hoursofservice, ows_contactinstructions, contactposition, contactvoicetelephone, ows_contactfacsimiletelephone, contactelectronicmailaddress, postcode, address, city, 
    stateorprovince, addresstype, ows_service_onlineresource, ows_role, inspirelayer, contactorganisation, sddi, ows_inspire_dsid_code, ows_inspire_dsid_ns, meta_uri, authorityurl_name, authorityurl_href) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);'''
    write2SQL(sqlin,ins)
    zahl = readSQL(sqlcount,(lid,))
    if zahl[0][0] > 0:
        writeDok('SpeciesDistribution',lid)
    return  'Einträge in die capabilities wurden vorgenommen, bitte editieren!'
    



def dellocalid(sddi):
    if sddi == '1':
        return 'Dieser Datensatz kann nicht gelöscht werden'
    else:
        sql = 'delete from sd_speciesdistributiondataset where sddi =?;'
        param = (sddi,)
        write2SQL(sql, param)
        sql1 = 'delete from main_capabilities where sddi =?;'
        write2SQL(sql1, param)
        erg = allefileweg(sddi)
        if erg == "alle files weg":
            return 'der speciesditributiondataset und alle files wurden gelöscht'
        else:
            return ' es konnte nicht alles gelöscht werden'   

def rooming():
    sql = 'drop table sd_in'
    sql2 = "delete from geometry_columns where f_table_name = 'sd_in'"
    write2So(sql)
    write2So(sql2)
    



def date():
    x = datetime.datetime.now()
    jahr = str(x.year)
    monat = str(x.month)
    tag = str(x.day)
    datum = jahr+'-'+monat+'-'+tag
    return datum




    





