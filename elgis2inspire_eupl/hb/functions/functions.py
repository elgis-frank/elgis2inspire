#!/usr/bin/python3
#-------------------------------------------------------
# Datei hb.functions.py Version 1.01 
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
import os
import csv
from sqlite3 import OperationalError, IntegrityError
from django.conf import settings
from main.functions.sql2spatialite import  write2SQL, write2So, write2spatialite, read2spatial,  readSQLSo, readsoSQL, readSQL

p = settings.ELGIS2INSPIRE__PATH
path = p['dbase']

def load_csv_dat(attdat):
    l = []
    with open(attdat, encoding='utf-8', newline='') as csvfile:
        attreader = csv.reader(csvfile, delimiter=';')
        for row in attreader:
            l.append(row)
    if 'lcode' in l[0]:
        #erst aufräumen
        sql22 = 'delete from hb_habitatlist;'
        write2So(sql22)
        attlist = ''
        inlist = ''
        for at in l[0]:
            attlist = attlist  + at + ","
        attlist = attlist.rstrip(',')
        sql = "insert into hb_habitatlist (" + attlist + " ) values ("
        for i in range(1,len(l)):
            for inn in l[i]:
                inlist = inlist + "'" + inn + "',"
            inlist = inlist.rstrip(',')
            inlist = inlist + ");"
            sqln = sql + inlist 
            write2So(sqln)
            sqln = ''
            inlist = ''
        return 'Die csv Datei wurde erfolgreich geladen'
        
    else:
        return 'Die csv ist nicht gültig. lcode ist nicht vorhanden'


def handle_uploaded_file(f, spfid, splcode, spn2000, nmspace):
    fileweg(f)
    with open(path+'upload/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    ergebnis = loadGeo(path+'upload/'+f.name, spfid, splcode, spn2000, nmspace)
    fileweg(f)
    return ergebnis

def dele():
    lsq = ['delete from hb_habitat;','delete from hb_habitattypecovertype;','delete from hb_habitatvegetationtype;', 'delete from hb_localnametype;']
    for i in range(len(lsq)):
        write2So(lsq[i])
    sql = 'select count(*) from hb_habitat;'
    z = readSQLSo(sql)
    if z[0] == 0:
        return 'die Daten wurden gelöscht'
    else:
        return 'Oops irgendwas ist schief gegangen' 

    
def loadGeo(datei, spfid, splcode, spn2000, nmspace):
    # geojson mit shellscript laden
    param = 'geojson-to-sqlite '+path+'db.sqlite3 habi_in ' + datei + ' --spatialite'
    args = shlex.split(param)
    subprocess.run(args)
    param = (6, 3035, 'habi_in')
    # Geodatensatz in Ordnung bringen
    sql = '''update geometry_columns set geometry_type = ?, srid = ?  where f_table_name = ?'''
    write2SQL(sql, param)
    sql1 = 'update habi_in set geometry = setSRID(geometry, 3035)'
    write2spatialite(sql1)
    ergebnis = test_habi(spfid, splcode, spn2000)
    if ergebnis == 'die Geodaten wurden erfolgreich geladen':
        sqltest = 'select ST_GeometryType(GEOMETRY) from habi_in;'
        r = read2spatial(sqltest)
        if r[0][0] == 'MULTIPOLYGON':
            #Geodatensatz übertragen
            sql2 = "insert into hb_habitat (featureID, lcode, n2000, idnamespace, the_geom) select " + spfid + "," + splcode + "," + spn2000 + ",'" + nmspace + "', geometry from habi_in;" 
            ergebnis = write2spatialite(sql2)
            if ergebnis == 'Ein Fehler ist aufgetreten, entweder die Daten existieren bereits oder im Importdatensatz gibt es Dubletten':
                rooming()
                return 'Die Daten sind fehlerhaft, die Daten existieren bereits oder im Importdatensatz gibt es Dubletten'
            else:
                sql3 = "select UpdateLayerStatistics('hb_habitat','the_geom');"
                write2spatialite(sql3)
                rooming()
                sqlist = ["update hb_habitat set lcode = ltrim(lcode,'x');","update hb_habitat set lcode = ltrim(lcode,'y');","update hb_habitat set lcode = ltrim(lcode,'z');","delete from hb_habitattypecovertype;","insert into hb_habitattypecovertype (fid,referenceHabitatTypeScheme,referenceHabitatTypeID) select featureId,'http://inspire.ec.europa.eu/codelist/ReferenceHabitatTypeSchemeValue/habitatsDirective', n2000 from hb_habitat where n2000 is not Null;","update hb_lebensraumtyp set ltcode = trim(ltcode);","update hb_habitattypecovertype set referenceHabitatTypeID = trim(referenceHabitatTypeID);",
        "update hb_habitattypecovertype set referenceHabitatTypeName = (select ltshortname as shortname from hb_lebensraumtyp where hb_lebensraumtyp.ltcode = hb_habitattypecovertype.referenceHabitatTypeID);",
        "update hb_habitattypecovertype set referenceHabitatTypeID = 'http://dd.eionet.europa.eu/vocabularyconcept/biodiversity/n2000habitats/'||referenceHabitatTypeID;",
        "update hb_habitatlist set lcode = trim(lcode);",
        "update hb_habitat set lcode = trim(lcode);",
        "UPDATE hb_habitat set icode = (select icode as code from hb_habitatlist where hb_habitatlist.lcode = hb_habitat.lcode);",
        "update hb_habitat set iname = (select iname as name from hb_habitatlist where hb_habitatlist.lcode = hb_habitat.lcode);",
        "insert into hb_habitattypecovertype (fid, referenceHabitatTypeID, referenceHabitatTypeName, referenceHabitatTypeScheme) select featureID, 'http://dd.eionet.europa.eu/vocabularyconcept/biodiversity/eunishabitats/'||icode, iname, 'http://inspire.ec.europa.eu/codelist/ReferenceHabitatTypeSchemeValue/eunis' from hb_habitat;",
        "delete from hb_localnametype;",
        "insert into hb_localnametype (fid ,localScheme, label) select featureID, 'http://registry.gdi-de.org/codelist/de.rp.naturschutz/654', lcode from hb_habitat ;",
        "update hb_localnametype set localName =(select lname as name from hb_habitatlist where hb_habitatlist.lcode = hb_localnametype.label );",
        "update hb_localnametype set  qualifierLocalName = (select imatch as match from hb_habitatlist where hb_habitatlist.lcode = hb_localnametype.label);",
        "update hb_localnametype set localNameCode = (select lcode as id from hb_habitatlist where hb_habitatlist.lcode = hb_localnametype.label);",
        "update hb_localnametype set localNameCode = 'http://registry.gdi-de.org/codelist/de.rp.naturschutz/654/'||localNameCode;","delete from hb_habitattypecovertype where referenceHabitatTypeId is NULL;",
        "delete from hb_habitat where icode is Null;" ]
                for zx in sqlist:
                    ergebnis = write2So(zx)
                    if ergebnis == 'Ein Fehler ist aufgetreten':
                        return ergebnis
                return 'Die Geodaten wurden erfolgreich geladen'
        else:
            rooming()
            return 'Im Datensatz sind keine Multipolygone, bitte überprüfen'
    else:
        rooming()
        return ergebnis

def rooming():
    sql = 'DROP table IF EXISTS habi_in'
    sql2 = "delete from geometry_columns where f_table_name = 'habi_in'"
    sql3 = "delete from geometry_columns_statistics where f_table_name = 'habi_in'"
    write2So(sql)
    write2So(sql2)
    write2So(sql3)
    
def handle_uploaded_attfile(f):
    with open(path + 'upload/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    fertig = load_csv_dat(path + 'upload/'+f.name)
    if os.path.exists(path + 'upload/'+f.name):
        os.remove(path + 'upload/'+f.name)
    return fertig


def test_habi(spfid, splcode, spn2000):
    sql = "PRAGMA table_info('habi_in')"
    fcol = []
    col = []
    itemf = 0
    frage = [spfid, splcode, spn2000]
    r = readsoSQL(sql)
    for z in r:
        col.append(z[1])
    for q in frage:
        if not q in col:
            fcol.append(q)
    # Suche nach dubletten
    sqldub1 = "select count(a."+spfid+") from habi_in as a , habi_in as b where a."+spfid+" = b."+spfid+" AND a.rowid < b.rowid;" 
    c = readsoSQL(sqldub1)
    #feststellen, ob der lcode stimmt
    sqltest3 = "alter table habi_in add column testn2000 text;"
    write2So(sqltest3)
    sqltest = "alter table habi_in add column testlnam text;"
    write2So(sqltest)
    sqltrim1 = "update habi_in set "+splcode+" = trim("+splcode+");"
    sqltrim2 = "update habi_in set "+spn2000+" = trim("+spn2000+");"
    write2So(sqltrim1)
    write2So(sqltrim2)
    sqltest1 = "update habi_in set testlnam = (select lname from hb_habitatlist where habi_in."+splcode+" = hb_habitatlist.lcode);"
    sqltest2 = "select count(*) from habi_in where testlnam is not Null;"
    write2So(sqltest1)
    zahl = readsoSQL(sqltest2)
    if zahl[0][0] == 0:
        itemf = 1
    sqltest4 = "update habi_in set testn2000 = (select ltlongname from hb_lebensraumtyp where habi_in."+spn2000+" = hb_lebensraumtyp.ltcode);"
    sqltest5 = "select count(*) from habi_in where testn2000 is not Null;"
    sqlgeom = "select st_intersects(a.geometry, b.GEOMETRY) from habi_in as a, rlp as b;"
    match = read2spatial(sqlgeom)
    testmatch = 'True'
    for i in match:
        if i[0] == 0:
            testmatch = 'False'
    write2So(sqltest4)
    zahl1 = readsoSQL(sqltest5)
    if zahl1[0][0] == 0:
        if itemf == 1:
            itemf = 3
        else:
            itemf = 2
    if itemf == 1 or itemf == 3:
        iteman = []
        if itemf == 1 :
            iteman.append('lcode')
        elif itemf == 3:
            iteman.append('n2000')
            iteman.append('lcode')
        ang = ''
        for i in iteman:
            ang = ang + ' ' + i 
        return 'Die ' + ang +' items sind fehlerhaft'
    if fcol:
        ans = ''
        for i in fcol:
            ans = ans +i+', '
        return 'Fehler! Die Spalte(n) ' + ans+ 'fehlen oder Fehler in der Geometrie'
    elif itemf > 0:
        iteman = []
        if itemf == 1 or itemf == 3:
            iteman.append('lcode')
        if itemf == 2 or itemf == 3:
            iteman.append('n2000')
        ang = ''
        for i in iteman:
            ang = ang + ' ' + i 
        return 'Die ' + ang +' items sind fehlerhaft'
    elif c[0][0] > 0:
        return 'Es existieren Dubletten. Bitte bereinigen'
    elif testmatch == 'False':
        return 'Die Daten liegen nicht in Rheinland-Pfalz oder es wurde ein falsches Koordinatensystem verwendet'
    else:
        return 'die Geodaten wurden erfolgreich geladen'


def getbbox(tab):
    sql = 'select UpdateLayerStatistics();'
    sql11 = 'select extent_min_x, extent_min_y, extent_max_x, extent_max_y from geometry_columns_statistics where f_table_name=?;'
    write2spatialite(sql)
    row = readSQL(sql11, (tab,))
    return row

def fileweg(f):
    if os.path.exists(path+'upload/'+f.name):
        os.remove(path+'upload/'+f.name)
    
def fillRang():
    sql2 = 'select hlid from hb_habitatlist order by hlid ASC;'
    sql3 = 'update hb_habitatlist set rang = ? where hlid = ?;'
    zaehler = 1
    row2 = readsoSQL(sql2)
    for i in row2:
        param = [zaehler,i[0]]
        write2SQL(sql3,param)
        zaehler = zaehler + 1

def gethlid(rang):
    sql = 'select hlid from hb_habitatlist where rang = ?'
    param = [rang,]
    pk = readSQL(sql,param)
    hlid = pk[0][0]
    return hlid



    



   





