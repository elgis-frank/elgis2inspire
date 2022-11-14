#-------------------------------------------------------
# Datei main.sql2spatialite.py Version 1.01 
#
#  Programming by eLGIS
#               
#      Copyright (C) by elgis ( https://elgis.de ) 2022
# Diese Datei ist Bestandteil der Software elgis2inspire, erhältlich unter https://github.com/elgis-frank/elgis2inspire .
# Diese Software wird unter der European Union Public Licence (EUPL-1.2) bereitgestellt. Bitte beachten Sie die Bestimmungen der Lizenz, insbesondere
# zur Bereitstellung und Nutzung der Software und zum Haftungsausschluss. Die Lizenz ist in allen Amtssprachen der EU veröffentlicht unter https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
# 
#--------------------------------------------------------

import sqlite3
import spatialite
from sqlite3 import OperationalError, IntegrityError
from django.conf import settings

p = settings.ELGIS2INSPIRE__PATH
path = p['dbase']



def exscript(file):
    try:
        con = sqlite3.connect(path + 'db.sqlite3')
        cur = con.cursor()
        sql_file = open(file)
        sql_as_string = sql_file.read()
        cur.executescript(sql_as_string)
        con.commit()
        con.close()
    except OperationalError:
        return 'Ein Fehler ist aufgetreten'

def write2SQL(befehl, param):
    try:
        con = sqlite3.connect(path  + 'db.sqlite3')
        cur = con.cursor()
        cur.execute(befehl, param)
        con.commit()
        con.close()
    except OperationalError:
        return 'Ein Fehler ist aufgetreten'


def write2So(sql):
    try:
        con = sqlite3.connect(path  + 'db.sqlite3')
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        con.close()
    except OperationalError:
        return 'Ein Fehler ist aufgetreten'

def write2spatialite(sql):
    try:
        con = spatialite.connect(path  + 'db.sqlite3')
        con.enable_load_extension(True)
        con.execute('SELECT load_extension("mod_spatialite")') 
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        con.close()
        return 'alles geladen'
    except (OperationalError,IntegrityError):
        con.close()
        return 'Ein Fehler ist aufgetreten, entweder die Daten existieren bereits oder im Importdatensatz gibt es Dubletten'

def read2spatial(sql):
    try:
        con = sqlite3.connect(path + 'db.sqlite3')
        con.enable_load_extension(True)
        con.execute('SELECT load_extension("mod_spatialite")') 
        cur = con.cursor()
        cur.execute(sql)
        row = cur.fetchall()
        con.commit()
        con.close()
        return row
    except OperationalError:
        return 'Ein Fehler ist aufgetreten'

def readSQL(befehl, param):
    try:
        con = sqlite3.connect(path  + 'db.sqlite3')
        cur = con.cursor()
        cur.execute(befehl, param)
        row = cur.fetchall()
        con.commit()
        con.close()
        return row
    except OperationalError:
        return 'Ein Fehler ist aufgetreten'

def readSQLSo(befehl):
    try:
        con = sqlite3.connect(path + 'db.sqlite3')
        cur = con.cursor()
        cur.execute(befehl)
        row = cur.fetchone()
        con.commit()
        con.close()
        return row
    except OperationalError:
        return 'Ein Fehler ist aufgetreten'

def readsoSQL(befehl):
    try:
        con = sqlite3.connect(path + 'db.sqlite3')
        cur = con.cursor()
        cur.execute(befehl)
        row = cur.fetchall()
        con.commit()
        con.close()
        return row
    except OperationalError:
        return 'Ein Fehler ist aufgetreten'