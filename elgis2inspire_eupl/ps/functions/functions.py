#!/usr/bin/python3
#-------------------------------------------------------
# Datei ps.functions.py Version 1.01 
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
import os, datetime
#import csv
from sqlite3 import OperationalError
import urllib.request
from pathlib import Path
from django.conf import settings
from main.functions.functions import writeDok
from main.functions.sql2spatialite import  write2SQL, write2So, write2spatialite, read2spatial, readSQL, readSQLSo, readsoSQL

p = settings.ELGIS2INSPIRE__PATH
path = p['dbase']



def handle_uploaded_file(f, kenn, name, url, date, sptyp, psid, psmurl):
    try:
        fileweg(f)
        with open(path+'upload/'+f.name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        ergebnis = loadpsGeo(path+'upload/'+f.name,  kenn, name, url, date, sptyp, psid, psmurl)
        fileweg(f)
        return ergebnis
    except OSError:
        ergebnis = 'der file wurde nicht gefunden'
        return ergebnis
    
def loadpsGeo(datei,  kenn, name, url, date, sptype, psid, psmurl):
    #Leichen beseitigen
    rooming()
    # geojson mit shellscript laden
    param = 'geojson-to-sqlite '+path+'db.sqlite3 ps_in ' + datei + ' --spatialite'
    args = shlex.split(param)
    subprocess.run(args)
    #Aufräumen
    # Geodatensatz in Ordnung bringen
    sqltest1 = 'select ST_GeometryType(GEOMETRY) from ps_in;'
    r = read2spatial(sqltest1)
   
    if r[0][0] == 'MULTIPOLYGON':
        param = (6, 3035, 'ps_in')
        sql = '''update geometry_columns set geometry_type = ?, srid = ?  where f_table_name = ?'''
        write2SQL(sql, param)
        sql2 = 'update ps_in set geometry = SetSRID(geometry, 3035);'
        write2spatialite(sql2)
        #Aufbau inspire
        testergebnis = testps(kenn, name, url, date, sptype)
        if testergebnis == 'die Geodaten wurden erfolgreich geladen':
            sqin = "insert into ps_protectedsite (localID, idnamespace, legalfoundationdate, legalfoundationdocument, sitename, ps_type, the_geom) select "+ kenn +",'http://naturschutz.rlp.de',"+ date +"," + url + "," + name +"," + sptype + ", geometry FROM ps_in;"
            ergebnisin = write2spatialite(sqin)
            if ergebnisin =='alles geladen':
                sqdat = ["update ps_protectedsite set featureid = psid;","delete from ps_sitedesignation;",
    "insert into ps_sitedesignation (fid, designation, designationscheme) select featureid, 'http://inspire.ec.europa.eu/codelist/Natura2000DesignationValue/specialProtectionArea', 'http://inspire.ec.europa.eu/codelist/DesignationSchemeValue/natura2000' from ps_protectedsite where ps_type = 'vsg';", "insert into ps_sitedesignation (fid, designation, designationscheme) select featureid, 'http://inspire.ec.europa.eu/codelist/UNESCOManAndBiosphereProgrammeDesignationValue/biosphereReserve', 'http://inspire.ec.europa.eu/codelist/DesignationSchemeValue/UNESCOManAndBiosphereProgramme' from ps_protectedsite where ps_type = 'biosphere';",
    "insert into ps_sitedesignation (fid, designation, designationscheme) select featureid, 'http://inspire.ec.europa.eu/codelist/Natura2000DesignationValue/specialAreaOfConservation', 'http://inspire.ec.europa.eu/codelist/DesignationSchemeValue/natura2000' from ps_protectedsite where ps_type = 'ffh';",
    "insert into ps_sitedesignation (fid, designation, designationscheme) select featureid, 'http://inspire.ec.europa.eu/codelist/IUCNDesignationValue/nationalPark', 'http://inspire.ec.europa.eu/codelist/DesignationSchemeValue/IUCN' from ps_protectedsite where ps_type = 'Nationalpark';", 
    "insert into ps_sitedesignation (fid, designation, designationscheme) select featureid, 'http://inspire.ec.europa.eu/codelist/RamsarDesignationValue/ramsar', 'http://inspire.ec.europa.eu/codelist/DesignationSchemeValue/ramsar' from ps_protectedsite where ps_type = 'ramsar';", 
    "Delete from ps_siteprotectionclassification;",
    "insert into ps_siteprotectionclassification (fid, siteProtectionClassification) select featureid, 'natureConservation' from ps_protectedsite;",
    "drop table ps_in;","delete from geometry_columns where f_table_name = 'ps_in'","update ps_protectedsite set legalfoundationdocument = replace(legalfoundationdocument,'&','%20')"]
                for z in sqdat:
                    write2spatialite(z)
                erg = writeDok('ProtectedSites',0)
                rooming()
                return 'Alles wurde geladen und ' +erg
            else:
                rooming()
                return ergebnisin
        else:
            rooming()
            return testergebnis
    else:
        rooming()
        return 'Im Datensatz sind keine Multipolygone, bitte überprüfen'

#Test, ob alle Spalten enthalten sind
def testps(kenn, name, url, date, sptype):
    pstype = ('ffh','vsg','Nationalpark','ramsar','biosphere')
    sql = "PRAGMA table_info('ps_in')"
    fcol = []
    col = []
    frage = [kenn, name, url, date, sptype]
    r = readsoSQL(sql)
    for z in r:
        col.append(z[1])
    for q in frage:
        if not q in col:
            fcol.append(q)
    testsql = 'select '+sptype+' from ps_in;'
    row = readsoSQL(testsql)
    test = 0
    for i in row:
        if i[0] in pstype:
            test = 0
        else:
            test = 1
    # Dubletten test
    sqltest2 = "select count(a."+ kenn +") from ps_in as a , ps_in as b where a."+ kenn +" = b."+ kenn +" AND a.rowid < b.rowid;"
    c = readsoSQL(sqltest2)
    
    # Koordinatensystemtest
    sqlgeom = "select st_intersects(a.geometry, b.GEOMETRY) from ps_in as a, rlp as b;"
    match = read2spatial(sqlgeom)
    testmatch = 'True'
    for i in match:
        if i[0] == 0:
            testmatch = 'False'
    if fcol:
        ans = ''
        for i in fcol:
            ans = ans +i+', '
        return 'Fehler! Die Spalte(n)' + ans+ 'fehlen'
    elif test == 1:
        return 'Fehler! Der inspire protected sites type stimmt nicht überein'
    elif c[0][0] > 0:
        return 'Der hochgeladene Datensatz enthält Dubletten'
    elif testmatch == 'False':
        return 'Die Daten liegen nicht in Rheinland-Pfalz oder es wurde ein falsches Koordinatensystem verwendet'
    else:
        return 'die Geodaten wurden erfolgreich geladen'
    

def dele():
    lsq = ['delete from ps_protectedsite;','delete from ps_sitedesignation;','delete from ps_siteprotectionclassification;',]
    for i in lsq:
        write2So(i)
    sql = 'select count(*) from ps_protectedsite;'
    z = readsoSQL(sql)
    allefileweg()
    for i in z:
        if i[0] == 0:
            return 'die Daten wurden gelöscht'
        else:
            return 'Oops irgendwas ist schief gegangen'


def rooming():
    sql = 'DROP table IF EXISTS ps_in'
    sql2 = "delete from geometry_columns where f_table_name = 'ps_in'"
    write2So(sql)
    write2So(sql2)    

def fileweg(f):
    if os.path.exists(path+'upload/'+f.name):
        os.remove(path+'upload/'+f.name)
    

def date():
    x = datetime.datetime.now()
    jahr = str(x.year)
    monat = str(x.month)
    tag = str(x.day)
    datum = jahr+'-'+monat+'-'+tag
    return datum


def allefileweg():
    filel = [path+'dok/ps.map',path+'dok/ps_wms.map',]
    for f in filel:
        if os.path.exists(f):
            os.remove(f)
    return "alle files weg"



    





