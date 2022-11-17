#!/usr/bin/python3
#-------------------------------------------------------
# Datei main.functions.py Version 1.01 
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
import os, stat
import csv
from sqlite3 import OperationalError
from pathlib import Path
from django.conf import settings
from main.functions.sql2spatialite import  write2SQL, write2So, write2spatialite, read2spatial,  readSQLSo, readsoSQL, readSQL

p = settings.ELGIS2INSPIRE__PATH
path = p['dbase']

def getbbox(tab):
    sql = 'select UpdateLayerStatistics();'
    sql11 = 'select extent_min_x, extent_min_y, extent_max_x, extent_max_y from geometry_columns_statistics where f_table_name=?;'
    write2spatialite(sql)
    row = readSQL(sql11, (tab,))
    return row

def writeDok(inspirelayer,sddi):
  sql = """select ows_inspire_temporal_reference ,  ows_inspire_mpoc_name ,  ows_inspire_mpoc_email ,  ows_inspire_metadatadate ,  ows_inspire_resourcelocator ,  contactperson ,  contactorganisation , 
 ows_hoursofservice ,  ows_contactinstructions ,  contactposition ,  contactvoicetelephone ,  ows_contactfacsimiletelephone ,  contactelectronicmailaddress ,  postcode ,  address ,  city ,
 stateorprovince ,  addresstype , ows_service_onlineresource,  ows_role ,  ows_inspire_dsid_code ,  ows_inspire_dsid_ns ,  meta_uri , authorityurl_name, authorityurl_href from main_capabilities where inspirelayer = ? AND sddi = ?""" 
  row = readSQL(sql,(inspirelayer, sddi))
  erg = 'alles ok'
  for c in range(len(row[0])):
    if not (row[0][c]):
      erg = 'der Metadatensatz zum layer: '+inspirelayer+' und dem speciesdistributiondataset: ' + sddi+' ist unvollständig. Bitte zuerst ergänzen'
  if inspirelayer == 'HabitatsandBiotopes':
    antwort = hbDok(row)
    return antwort
  if inspirelayer == 'ProtectedSites':
    antwort = psDok(row)
    return antwort
  if inspirelayer == 'SpeciesDistribution':
    if not row:
      return 'Abfrage gescheitert'
    elif not erg == 'alles ok':
      return erg
    else:
      antwort = sdDok(row,sddi)
      return antwort

def hbDok(ergebnis):
  for i in ergebnis:
    hbwfs = '''MAP
  NAME "habitatsandBiotops_server"
  STATUS ON
  SIZE 400 300
  EXTENT 4021379 2871487 4214276 3093359
  UNITS meters
  SHAPEPATH "../data"
  IMAGECOLOR 255 255 255
  CONFIG "MS_ERRORFILE" "/var/www/inspire/dok/ms_error.txt"
  DEBUG 5


  #
  # Start of web interface definition
  #
  WEB
    IMAGEPATH "/ms4w/tmp/ms_tmp/"
    IMAGEURL "/ms_tmp/"
   METADATA
    "ows_languages" "eng,ger"               #first default, values according ISO 639-2/B
    "ows_inspire_capabilities" "embed"
    "ows_languages" "eng,ger"               #first default, values according ISO 639-2/B
    "ows_inspire_temporal_reference" "'''+i[0]+'''"     #date of last revision, value according YYYY-MM-DD
    "ows_inspire_mpoc_name" "'''+i[1]+'''"                                          #point of contact
    "ows_inspire_mpoc_email" "'''+i[2]+'''"           #point of contact, no personal email
    "ows_inspire_metadatadate" "'''+i[3]+'''"
    "ows_inspire_resourcelocator" "'''+i[4]+'''/hb_wfs"
    "ows_inspire_keyword" "infoFeatureAccessService"                                  #value according "classification of spatial data services"
    "ows_inspire_dsid_code" "'''+i[19]+'''"
    "ows_inspire_dsid_ns" "'''+i[20]+'''"
    "ows_keywordlist" "habitats and biotopes"
    "wfs_contactperson" "'''+i[5]+'''"
    "wfs_contactorganization" "'''+i[6]+'''"
    "ows_hoursofservice" "'''+i[7]+'''"
    "ows_contactinstructions" "'''+i[8]+'''"
    "ows_role" "'''+i[19]+'''"
    "wfs_contactposition" "'''+i[9]+'''"
    "wfs_contactvoicetelephone" "'''+i[10]+'''"
    "ows_contactfacsimiletelephone" "'''+i[11]+'''"
    "wfs_contactelectronicmailaddress" "'''+i[12]+'''"
    "wfs_postcode" "'''+i[13]+'''"
    "wfs_address" "'''+i[14]+'''"
    "wfs_city" "'''+i[15]+'''"
    "wfs_stateorprovince" "'''+i[16]+'''"
    "wfs_country" "DE"
    "wfs_addresstype" "'''+i[17]+'''"  
    "wfs_onlineresource"  "'''+i[4]+'''/hb_wfs"
    "wfs_encoding" "utf-8"
    "wfs_namespace_prefix" "hb"
    "wfs_namespace_uri"  "http://inspire.ec.europa.eu/schemas/hb/4.0"
    "wfs_title.eng"          "HabitatsAndBiotopes" 
    "wfs_title.ger"     "Biotope"
    "ows_service_onlineresource" "'''+i[18]+'''"
    "wfs_srs"            "EPSG:3035 EPSG:4326 EPSG:4269 EPSG:3978 EPSG:3857"
    "wfs_abstract.eng"       "download service inspire Habitates and Biotopes of Rhineland-pallatine"
    "wfs_abstract.ger"    "web feature service für das inspire Thema Biotope"
    "wfs_fees"           "none"
    "wfs_accessconstraints"   "license odbl Version 3.0"
    "wfs_enable_request" "*"  # necessary
    "wfs_maxfeatures"   "1000"           #responsible organization, value according "INSPIRE 
    "wfs_maxfeatures_ignore_for_resulttype_hits" "true" 
#
END
  END

  PROJECTION
    "init=epsg:3035"
  END

  #
  # Start of layer definitions
  #

  ##################
  # HabitatsAndBiotopes
  ##################
  LAYER
    NAME "Habitat"
    METADATA
      "wfs_title"         "HabitatsAndBiotopes" ##REQUIRED
      "wfs_srs"           "EPSG:3035" ## REQUIRED
     # "gml_include_items" "all" ## Optional (serves all attributes for layer)
      "ows_featureid"     "featureid" ## REQUIRED
      "wfs_enable_request" "*"
      "wfs_metadataurl_href" "'''+i[22]+'''"
  END
    TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE OGR
    CONNECTION "/var/www/inspire/db.sqlite3"
    DATA "hb_habitat"
    PROJECTION
      "init=epsg:3035"
    END
    CLASS
      NAME 'hb'
      STYLE
        COLOR 255 128 128
        OUTLINECOLOR 96 96 96
      END
    END
  END #layer

END #mapfile'''
    hbwms = '''MAP
  NAME "HB.Habitats"
  STATUS ON
  SIZE 400 300
  EXTENT 4021379 2871487 4214276 3093359
  UNITS meters
  SHAPEPATH "../data"
  IMAGECOLOR 255 255 255
  CONFIG "MS_ERRORFILE" "/var/www/inspire/dok/ms_error.txt"
  DEBUG 5


  #
  # Start of web interface definition
  #
  WEB
    IMAGEPATH "/var/www/inspire/static/tmp/"
    IMAGEURL "/static/tmp/"
  

  METADATA
  "ows_languages" "eng,ger"               #first default, values according ISO 639-2/B, Entscheidung noch ausstehend
  "ows_inspire_capabilities" "embed"
  #root layer nicht ladbar machen
  "wms_rootlayer_name"     ""
  "wms_rootlayer_title.eng" "HabitatsAndBiotopes"
  "wms_rootlayer_title.ger" "Biotope"
  "wms_rootlayer_abstract.eng" "root layer of view service Hb.Habitat not loadable"
  "wms_rootlayer_abstract.ger" "Gesamtlayer des inspire Themas Biotope nicht ladbar"
  # extended capabilities
  "ows_inspire_temporal_reference" "'''+i[0]+'''"     #date of last revision, value according YYYY-MM-DD
  "ows_inspire_mpoc_name" "'''+i[1]+'''"                                          #point of contact
  "ows_inspire_mpoc_email" "'''+i[2]+'''"           #point of contact, no personal email
  "ows_inspire_metadatadate" "'''+i[3]+'''"
  "ows_inspire_resourcelocator" "'''+i[4]+'''/hb_wms"
  "ows_inspire_keyword" "infoMapAccessService"                                  #value according "classification of spatial data services"
  #wms metadata
  "wms_title.eng"   "WMS Habitats And Biotopes RLP"
  "wms_title.ger"   "WMS Biotope für inspire"
  "wms_abstract.eng" "inspire view service habitats and biotopes according to annex III inspire regulation"
  "wms_abstract.ger" "inspire Kartendienst für Biotope in Rheinland-Pfalz entsprechend Annex III Thema der inspire Richtlinie"
  "wms_onlineresource"   "'''+i[4]+'''/hb_wms"
  "wms_keywordlist_vocabulary" "GEMET"   
  "wms_keywordlist_GEMET_items" "habitat,biotope"
  "wms_accessconstraints" "licence (OdBl 3.0)"
  "wms_fees" "no conditions apply"
  "wms_contactperson" "'''+i[5]+'''"
  "wms_contactorganization" "'''+i[6]+'''"
  "wms_contactposition" "'''+i[9]+'''"
  "wms_contactvoicetelephone" "'''+i[10]+'''"
  "wms_contactelectronicmailaddress" "'''+i[12]+'''"
  "wms_postcode" "'''+i[13]+'''"
  "wms_address" "'''+i[14]+'''"
  "wms_city" "'''+i[15]+'''"
  "wms_stateorprovince" "'''+i[16]+'''"
  "wms_country" "DE"
  "wms_addresstype" "'''+i[17]+'''"  
  "wms_srs" "EPSG:3035 EPSG:4269 EPSG:4326 EPSG:25832" 
  "wms_enable_request" "*"
  END
END
  PROJECTION
    "init=epsg:3035"
  END

  #
  # Start of layer definitions
  #

  ##################
  # HabitatsAndBiotopes
  ##################
  LAYER
    NAME "HB.Habitat"
    METADATA
      "wms_title"         "Habitat" ##REQUIRED
      "wms_abstract.eng" "habitat data from Rhineland-Pallatine"
      "wms_abstract.ger" "Daten der Biotopkartierung von Rheinland-Pfalz"
      "wms_srs"           "EPSG:3035" ## REQUIRED
      "wms_keywordlist_vocabulary" "GEMET"   
      "wms_keywordlist_GEMET_items" "habitat,biotope"
      "gml_include_items" "all" ## Optional (serves all attributes for layer)
      "wms_authorityurl_name" "'''+i[23]+'''"
      "wms_authorityurl_href" "'''+i[24]+'''"
      "wms_identifier_authority" "'''+i[23]+'''"
      "wms_identifier_value" "'''+i[19]+'''"
      "wms_metadataurl_format" "text/xml"
      "wms_metadataurl_href"  "'''+i[22]+'''"                                                                             
      "wms_metadataurl_type" "TC211"
    END 
    
    TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE OGR
    CONNECTION "/var/www/inspire/db.sqlite3"
    DATA "hb_habitat"
    PROJECTION
      "init=epsg:3035"
    END
    CLASS
      NAME 'hb'
      STYLE
        OPACITY 50
        COLOR 80 80 80
        OUTLINECOLOR 0 0 0
      END
    END
  END #layer

END #mapfile'''
  wfsfile = Path(path+"dok/hb.map")
  if wfsfile.is_file():
    os.remove(wfsfile)
  with open(path+"dok/hb.map", "w", encoding='utf8') as wfs_file:
    wfs_file.write(hbwfs)
  os.chmod(path+"dok/hb.map", stat.S_IRWXU)
  wmsfile = Path(path+"dok/hb_wms.map")
  if wfsfile.is_file():
    os.remove(wmsfile)
  with open(path+"dok/hb_wms.map", "w", encoding='utf8') as wfs_file:
    wfs_file.write(hbwms)
  os.chmod(path+"dok/hb_wms.map", stat.S_IRWXU)
  return 'alles erledigt'
    

def psDok(ergebnis):
  sql1 = 'select distinct(ps_type) from ps_protectedsite order by ps_type;'
  type = readsoSQL(sql1)
  if not type:
    return 'Es sind keine Daten zu protectedsites gespeichert, es wurden keine mapfiles angelegt'
  else:
    for i in ergebnis:
      pswfs = '''
  MAP
  NAME "protectedsites_server"
  STATUS ON
  SIZE 400 300
  EXTENT 4021379 2871487 4214276 3093359
  UNITS meters
  SHAPEPATH "../data"
  IMAGECOLOR 255 255 255
  CONFIG "MS_ERRORFILE" "/var/www/inspire/dok/ms_error.txt"
  DEBUG 5
  #
  # Start of web interface definition
  #
  WEB
    IMAGEPATH "/ms4w/tmp/ms_tmp/"
    IMAGEURL "/ms_tmp/"
    METADATA
    "ows_languages" "eng,ger"               #first default, values according ISO 639-2/B
    "ows_inspire_capabilities" "embed"
    "ows_languages" "eng,ger"               #first default, values according ISO 639-2/B
    "ows_inspire_temporal_reference" "'''+i[0]+'''"     #date of last revision, value according YYYY-MM-DD
    "ows_inspire_mpoc_name" "'''+i[1]+'''"                                          #point of contact
    "ows_inspire_mpoc_email" "'''+i[2]+'''"           #point of contact, no personal email
    "ows_inspire_metadatadate" "'''+i[3]+'''"
    "ows_inspire_resourcelocator" "'''+i[4]+'''/hb_wfs"
    "ows_inspire_keyword" "infoFeatureAccessService"                                  #value according "classification of spatial data services"
    "ows_inspire_dsid_code" "'''+i[19]+'''"
    "ows_inspire_dsid_ns" "'''+i[20]+'''"
    "ows_keywordlist" "habitats and biotopes"
    "wfs_contactperson" "'''+i[5]+'''"
    "wfs_contactorganization" "'''+i[6]+'''"
    "ows_hoursofservice" "'''+i[7]+'''"
    "ows_contactinstructions" "'''+i[8]+'''"
    "ows_role" "'''+i[19]+'''"
    "wfs_contactposition" "'''+i[9]+'''"
    "wfs_contactvoicetelephone" "'''+i[10]+'''"
    "ows_contactfacsimiletelephone" "'''+i[11]+'''"
    "wfs_contactelectronicmailaddress" "'''+i[12]+'''"
    "wfs_postcode" "'''+i[13]+'''"
    "wfs_address" "'''+i[14]+'''"
    "wfs_city" "'''+i[15]+'''"
    "wfs_stateorprovince" "'''+i[16]+'''"
    "wfs_country" "DE"
    "wfs_addresstype" "'''+i[17]+'''"  
    "wfs_onlineresource"  "'''+i[4]+'''/ps_wfs"
    "ows_service_onlineresource" "'''+i[18]+'''"
    "wfs_encoding" "utf-8"
    "wfs_namespace_prefix" "ps"
    "wfs_namespace_uri"  "http://inspire.ec.europa.eu/schemas/ps/4.0"
    "wfs_title.eng"     "protectedsites" 
    "wfs_title.ger"     "Schutzgebiete"
    "wfs_srs"            "EPSG:3035 EPSG:4326 EPSG:4269 EPSG:3978 EPSG:3857"
    "wfs_abstract.eng"       "download service inspire protected sites of Rhineland-pallatine"
    "wfs_abstract.ger"    "web feature service für das inspire Thema Schutzgebiete"
    "wfs_fees"           "none"
    "wfs_accessconstraints"   "license odbl Version 3.0"
    "wfs_enable_request" "*"  # necessary
    "wfs_maxfeatures"   "1000"          
    "wfs_maxfeatures_ignore_for_resulttype_hits" "true"
    END
  END

  PROJECTION
    "init=epsg:3035"
  END

  #
  # Start of layer definitions
  #

  ##################
  # protected sites
  ##################
  LAYER
    NAME "ProtectedSite"
    METADATA
      "wfs_title"         "ProtectedSite" ##REQUIRED
      "wfs_srs"           "EPSG:3035" ## REQUIRED
      #"gml_include_items" "all" ## Optional (serves all attributes for layer)
      "gml_featureid"       "featureid" ## REQUIRED
      "wfs_enable_request" "*"
      "wfs_metadataurl_href" "'''+i[22]+'''"
  END
    TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE OGR
    CONNECTION "/var/www/inspire/db.sqlite3"
    DATA "ps_protectedsite"
    PROJECTION
      "init=epsg:3035"
    END   
  CLASS
      NAME 'ps'
      STYLE
        COLOR 255 128 128
        OUTLINECOLOR 96 96 96
      END
    END
  END #layer

END #mapfile '''
  ergebnis = pswmsDok(ergebnis,type)
  wfsfile = Path(path+"dok/ps.map")
  if wfsfile.is_file():
    os.remove(wfsfile)
  with open(path+"dok/ps.map", "w", encoding='utf8') as wfs_file:
    wfs_file.write(pswfs)
  os.chmod(path+"dok/ps.map", stat.S_IRWXU)
  return ergebnis

def pswmsDok(ergebnis, type):
  dtype = {'ffh':'SpecialAreaOfConservation','vsg':'SpecialProtectionArea','Nationalpark':'NationalPark','ramsar':'Ramsar','biosphere':'BiosphereReserve'}
  for i in ergebnis:
    pswms = '''

  MAP
  NAME "PS.ProtectedSite"
  STATUS ON
  SIZE 400 300
  EXTENT 4021379 2871487 4214276 3093359
  UNITS meters
  SHAPEPATH "../data"
  IMAGECOLOR 255 255 255
  CONFIG "MS_ERRORFILE" "/var/www/inspire/dok/ms_error.txt"
  DEBUG 5


  #
  # Start of web interface definition
  #
  WEB
    IMAGEPATH "/var/www/inspire/static/tmp/"
    IMAGEURL "/static/tmp/"
  

   METADATA
  "ows_languages" "eng,ger"               #first default, values according ISO 639-2/B
  "wms_rootlayer_name"     ""
  "ows_inspire_capabilities" "embed"
  # extended capabilities
  "ows_inspire_temporal_reference" "'''+i[0]+'''"     #date of last revision, value according YYYY-MM-DD
  "ows_inspire_mpoc_name" "'''+i[1]+'''"                                          #point of contact
  "ows_inspire_mpoc_email" "'''+i[2]+'''"           #point of contact, no personal email
  "ows_inspire_metadatadate" "'''+i[3]+'''"
  "ows_inspire_resourcelocator" "'''+i[4]+'''/ps_wms"
  "ows_inspire_keyword" "infoMapAccessService" 
  #wms metadata
  "wms_title.eng"           "Protected Sites"
  "wms_title.ger"   "Inspire WMS Schutzgebiete RLP"
  "wms_abstract.eng" "inspire view service protected sites according to annex I inspire regulation"
  "wms_abstract.ger" "inspire Kartendienst für Schutzgebiete in Rheinland-Pfalz entsprechend Annex I Thema der inspire Richtlinie"
  "wms_onlineresource"   "'''+i[4]+'''/ps_wms"                         
  "wms_keywordlist_vocabulary" "GEMET"   
  "wms_keywordlist_GEMET_items" "protected sites,biosphere reserve,national park"
  "wms_accessconstraints" "licence (OdBl 3.0)"
  "wms_fees" "no conditions apply"
  "wms_contactperson" "'''+i[5]+'''"
  "wms_contactorganization" "'''+i[6]+'''"
  "wms_contactposition" "'''+i[9]+'''"
  "wms_contactvoicetelephone" "'''+i[10]+'''"
  "wms_contactelectronicmailaddress" "'''+i[12]+'''"
  "wms_postcode" "'''+i[13]+'''"
  "wms_address" "'''+i[14]+'''"
  "wms_city" "'''+i[15]+'''"
  "wms_stateorprovince" "'''+i[16]+'''"
  "wms_country" "DE"
  "wms_addresstype" "'''+i[17]+'''" 
  "wms_srs"    "EPSG:3035 EPSG:4269 EPSG:4326 EPSG:25832" 
  "wms_enable_request" "*"
  END
END
  PROJECTION
    "init=epsg:3035"
  END

  #
  # Start of layer definitions
  #

  ##################
  # protected sites
  ##################
  LAYER
    NAME "PS.ProtectedSite"
    METADATA
      "wms_title"         "Protected Site – root layer" ##REQUIRED
      "wms_srs"           "EPSG:3035" ## REQUIRED
      "gml_include_items" "all" ## Optional (serves all attributes for layer)
      "wms_authorityurl_name" "SGD Nord"
      "wms_authorityurl_href" "http://naturschutz.rlp.de"
      "wms_identifier_authority" "SGD Nord"
      "wms_identifier_value" "Point of Contact"
      "wms_metadataurl_format" "text/xml"
      "wms_metadataurl_href"  "https://geodaten.naturschutz.rlp.de/kartendienste_naturschutz/mod_metadata/ajax/getxml.php?id=5184"
      "wms_metadataurl_type" "TC211"
    END 
    
    TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE OGR
    CONNECTION "/var/www/inspire/db.sqlite3"
    DATA "ps_protectedsite"
    PROJECTION
      "init=epsg:3035"
    END
    CLASS
	NAME 'PS'
      STYLE
        OPACITY 50
        COLOR 80 80 80
        OUTLINECOLOR 0 0 0
      END
    END
  END #layer
  LAYER
    NAME "PS.ProtectedSitesNatureConservation"
    METADATA
      "wms_title"         "Protected Sites – Nature Conservation" ##REQUIRED
      "wms_srs"           "EPSG:3035" ## REQUIRED
      "gml_include_items" "all" ## Optional (serves all attributes for layer)
      "wms_authorityurl_name" "'''+i[23]+'''"
      "wms_authorityurl_href" "'''+i[24]+'''"
      "wms_identifier_authority" "'''+i[23]+'''"
      "wms_identifier_value" "'''+i[19]+'''"
      "wms_metadataurl_format" "text/xml"
      "wms_metadataurl_href"  "'''+i[22]+'''"
      "wms_metadataurl_type" "TC211"
    END 
    
    TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE OGR
    CONNECTION "/var/www/inspire/db.sqlite3"
    DATA "ps_protectedsite"
    PROJECTION
      "init=epsg:3035"
    END
    CLASS
	NAME 'PS'
      STYLE
        OPACITY 50
        COLOR 80 80 80
        OUTLINECOLOR 0 0 0
      END
    END
  END #layer
  '''
    for i2 in type:
      nam = i2[0]
      namtype = dtype[nam]
      pswms = pswms + '''LAYER
    NAME "PS.ProtectedSites'''+namtype+'''"
     METADATA
      "wms_title"         "Protected Sites - ''' +namtype+'''" ##REQUIRED
      "wms_srs"           "EPSG:3035" ## REQUIRED
      "gml_include_items" "all" ## Optional (serves all attributes for layer)
       "wms_abstract" "ProtectedSite where ProtectedSite.siteDesignation.designation = ''' +namtype+'''"
       "wms_identifier_authority" "'''+i[23]+'''"
       "wms_identifier_value" "'''+i[19]+'''"
       "wms_metadataurl_format" "text/xml"
       "wms_metadataurl_href"  "'''+i[22]+'''"
       "wms_metadataurl_type" "TC211"
    END
 TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE OGR
    CONNECTION "/var/www/inspire/db.sqlite3"
    DATA "select localID, the_geom from ps_protectedsite where ps_type = \''''+nam+'''\'"
    PROJECTION
      "init=epsg:3035"
    END
    CLASS
     NAME "'''+nam+'''"
      STYLE
        OPACITY 50
        COLOR 80 80 80
        OUTLINECOLOR 0 0 0
      END
    END
  END #layer
  '''
  pswms = pswms + 'END'
  wmsfile = Path(path+"dok/ps_wms.map")
  if wmsfile.is_file():
    os.remove(wmsfile)
  with open(path+"dok/ps_wms.map", "w", encoding='utf8') as wms_file:
    wms_file.write(pswms)
  os.chmod(path+"dok/ps_wms.map", stat.S_IRWXU)
  return '  alle mapfiles wurden geschrieben'


def sdDok(ergebnis, sddi):
  sdi = str(sddi)
  sql3 = 'select name, title_ger, abstract_eng, abstract_ger from sd_speciesdistributiondataset where localID = ?'
  sql2 = 'select distinct(referenceSpeciesName) from sd_speciesdistributionunit where sddi = ?  order by referenceSpeciesName;'
  name = readSQL(sql2,(sddi,))
  data = readSQL(sql3,(sddi,))
  if not name:
    return 'Es sind keine Daten zu SpeciesDistribution gespeichert, es wurden keine mapfiles angelegt'
  else:
    for i in ergebnis:
      if not i:
        i = ''
      sdwfs = '''
  MAP
  NAME "speciesdistribution"
  STATUS ON
  SIZE 400 300
  EXTENT 4021379 2871487 4214276 3093359
  UNITS meters
  SHAPEPATH "../data"
  IMAGECOLOR 255 255 255
  CONFIG "MS_ERRORFILE" "/var/www/inspire/dok/ms_error.txt"
  
  #
  # Start of web interface definition
  #
  WEB
    IMAGEPATH "/ms4w/tmp/ms_tmp/"
    IMAGEURL "/ms_tmp/"
    METADATA
    "ows_inspire_capabilities" "embed"
    "ows_languages" "eng,ger"               #first default, values according ISO 639-2/B
    "ows_inspire_temporal_reference" "'''+i[0]+'''"     #date of last revision, value according YYYY-MM-DD
    "ows_inspire_mpoc_name" "'''+i[1]+'''"                                          #point of contact
    "ows_inspire_mpoc_email" "'''+i[2]+'''"           #point of contact, no personal email
    "ows_inspire_metadatadate" "'''+i[3]+'''"
    "ows_inspire_resourcelocator" "'''+i[4]+'''/sd_d'''+sdi+'''_wfs"
    "ows_inspire_keyword" "infoFeatureAccessService"                                  #value according "classification of spatial data services"
    "ows_inspire_dsid_code" "'''+i[19]+'''"
    "ows_inspire_dsid_ns" "'''+i[20]+'''"
    "ows_keywordlist" "habitats and biotopes"
    "wfs_contactperson" "'''+i[5]+'''"
    "wfs_contactorganization" "'''+i[6]+'''"
    "ows_hoursofservice" "'''+i[7]+'''"
    "ows_contactinstructions" "'''+i[8]+'''"
    "ows_role" "'''+i[19]+'''"
    "wfs_contactposition" "'''+i[9]+'''"
    "wfs_contactvoicetelephone" "'''+i[10]+'''"
    "ows_contactfacsimiletelephone" "'''+i[11]+'''"
    "wfs_contactelectronicmailaddress" "'''+i[12]+'''"
    "wfs_postcode" "'''+i[13]+'''"
    "wfs_address" "'''+i[14]+'''"
    "wfs_city" "'''+i[15]+'''"
    "wfs_stateorprovince" "'''+i[16]+'''"
    "wfs_country" "DE"
    "wfs_addresstype" "'''+i[17]+'''"  
    "wfs_onlineresource"  "'''+i[4]+'''/sd_d'''+sdi+'''_wfs"
    "ows_service_onlineresource" "'''+i[18]+'''"
    "wfs_encoding" "utf-8"
    "wfs_namespace_prefix" "sd"
    "wfs_namespace_uri"  "http://inspire.ec.europa.eu/schemas/sd/4.0"
    "wfs_title.eng"          "'''+data[0][0]+'''" ## REQUIRED
    "wfs_title.ger"     "'''+data[0][1]+'''"
    "wfs_srs"            "EPSG:3035 EPSG:4326 EPSG:4269 EPSG:3978 EPSG:3857" ## Recommended
    "wfs_abstract.eng"       "'''+data[0][2]+'''" 
    "wfs_abstract.ger"    "'''+data[0][3]+'''"
    "wfs_keywordlist"    "species distribution, natural range"
    "wfs_fees"           "none"
    "wfs_accessconstraints"   "license odbl Version 3.0" 
    "wfs_enable_request" "*"  # necessary
    "wfs_maxfeatures"   "1000"
    "wfs_maxfeatures_ignore_for_resulttype_hits" "true"
          END
    END
  

  PROJECTION
    "init=epsg:3035"
  END

  #
  # Start of layer definitions
  #

  ##################
  # species distribution
  ##################
  LAYER
    NAME "SpeciesDistributionUnit"
    METADATA
    "wfs_title"         "SpeciesDistributionUnit" ##REQUIRED
    "wfs_srs"           "EPSG:3035" ## REQUIRED
    #"gml_include_items" "all" ## Optional (serves all attributes for layer)
    "gml_featureid"       "localID" ## REQUIRED
    "wfs_enable_request" "*"
    "wfs_metadataurl_href" "'''+i[22]+'''"
     END
    TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE OGR
    CONNECTION "/var/www/inspire/db.sqlite3"
    DATA "select localID, the_geom from sd_speciesdistributionunit where sddi = '''+sdi+'''"
     CLASS
      NAME "sd'''+sdi+'''"
      STYLE
        COLOR 255 128 128
        OUTLINECOLOR 96 96 96
      END
    END
  END #layer

END #mapfile
'''
      sdwms ='''MAP
  NAME "speciesdistribution"
  STATUS ON
  SIZE 400 300
  EXTENT 4021379 2871487 4214276 3093359
  UNITS meters
  #SHAPEPATH "../data"
  IMAGECOLOR 255 255 255
  CONFIG "MS_ERRORFILE" "/var/www/inspire/dok/ms_error.txt"
  #
  # Start of web interface definition
  #
  WEB
    IMAGEPATH "/var/www/inspire/static/tmp/"
    IMAGEURL "/static/tmp/"
  METADATA
  "ows_inspire_capabilities" "embed"
  "ows_languages" "eng,ger"               #first default, values according ISO 639-2/B
  "wms_rootlayer_name"     ""
   # extended capabilities
  "ows_inspire_temporal_reference" "'''+i[0]+'''"     #date of last revision, value according YYYY-MM-DD
  "ows_inspire_mpoc_name" "'''+i[1]+'''"                                          #point of contact
  "ows_inspire_mpoc_email" "'''+i[2]+'''"           #point of contact, no personal email
  "ows_inspire_metadatadate" "'''+i[3]+'''"
  "ows_inspire_resourcelocator" "'''+i[4]+'''/sd_d'''+sdi+'''wms"
  "ows_inspire_keyword" "infoMapAccessService" 
  #wms metadata
  "wms_accessconstraints" "licence (OdBl 3.0)"
  "wms_fees" "no conditions apply"
  "wms_contactperson" "'''+i[5]+'''"
  "wms_contactorganization" "'''+i[6]+'''"
  "wms_contactposition" "'''+i[9]+'''"
  "wms_contactvoicetelephone" "'''+i[10]+'''"
  "wms_contactelectronicmailaddress" "'''+i[12]+'''"
  "wms_postcode" "'''+i[13]+'''"
  "wms_address" "'''+i[14]+'''"
  "wms_city" "'''+i[15]+'''"
  "wms_stateorprovince" "'''+i[16]+'''"
  "wms_country" "DE"
  "wms_addresstype" "'''+i[17]+'''"  
  "wms_title.eng"  "'''+data[0][0]+'''"
  "wms_title.ger"   "'''+data[0][1]+'''"
  "wms_abstract.eng" "'''+data[0][2]+'''"
  "wms_abstract.ger" "'''+data[0][3]+'''"
  "wms_onlineresource"   "'''+i[4]+'''/sd_d'''+sdi+'''_wms"
  "wms_srs"   "EPSG:3035 EPSG:4269 EPSG:4326 EPSG:25832" 
  "wms_enable_request" "*"
  END
END
  PROJECTION
    "init=epsg:3035"
  END
  
    #
  # Start of layer definitions
  #
  LAYER
    NAME "SD._ReferenceSpeciesCodeValue_"
    METADATA
    "wms_title"         "SpeciesDistributionUnit" ##REQUIRED
    "wms_srs"           "EPSG:3035" ## REQUIRED
    #"gml_include_items" "all" ## Optional (serves all attributes for layer)
    "wms_srs"           "EPSG:3035" ## REQUIRED
    "wms_keywordlist_vocabulary" "GEMET"   
    "wms_keywordlist_GEMET_items" "species"
    "wms_authorityurl_name" "'''+i[23]+'''"
    "wms_authorityurl_href" "'''+i[24]+'''"
    "wms_identifier_authority" "'''+i[23]+'''"
    "wms_identifier_value" "'''+i[19]+'''"
    "wms_metadataurl_format" "text/xml"
    "wms_metadataurl_href"  "'''+i[22]+'''"
    "wms_metadataurl_type" "TC211"
           
    END 
    
    TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE OGR
    CONNECTION "/var/www/inspire/db.sqlite3"
    DATA "select localID, the_geom from sd_speciesdistributionunit where sddi = '''+sdi+'''"
    PROJECTION
      "init=epsg:3035"
    END
    CLASS
      NAME 'SD.SpeciesDistribution.Default'
      STYLE
        OPACITY 50
        COLOR 80 80 80
        OUTLINECOLOR 0 0 0
      END
    END
  END #layer
   '''
      
      for n in name:
        nam = n[0]
        namshort = nam.replace(' ','')
        sdwms = sdwms + '''
  
    LAYER
    NAME "SD.'''+namshort+'''"
    METADATA
    "wms_title"         "Species Distribution of (''' +namshort+''')" ##REQUIRED
    "wms_srs"           "EPSG:3035" ## REQUIRED
    #"gml_include_items" "all" ## Optional (serves all attributes for layer)
    "wms_srs"           "EPSG:3035" ## REQUIRED
    "wms_keywordlist_vocabulary" "GEMET"   
    "wms_keywordlist_GEMET_items" "species"
    "wms_authorityurl_name" "'''+i[23]+'''"
    "wms_authorityurl_href" "'''+i[24]+'''"
    "wms_identifier_authority" "'''+i[23]+'''"
    "wms_identifier_value" "'''+i[19]+'''"
    "wms_metadataurl_format" "text/xml"
    "wms_metadataurl_href"  "'''+i[22]+'''"
    "wms_metadataurl_type" "TC211"
           
    END 
    
    TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE OGR
    CONNECTION "/var/www/inspire/db.sqlite3"
    DATA "select localID, the_geom from sd_speciesdistributionunit where sddi = '''+sdi+''' and referenceSpeciesName = \''''+nam+'''\'"
    PROJECTION
      "init=epsg:3035"
    END
    CLASS
      NAME 'sd'
      STYLE
        OPACITY 50
        COLOR 80 80 80
        OUTLINECOLOR 0 0 0
      END
    END
  END #layer'''
      sdwms = sdwms + '''
      END'''

  #ab hier Anpassung der python files
  pysdwfs = """#!/usr/bin/python3
#-------------------------------------------------------
# Datei sd_wfs Version 1.01 
#
#  Programming by eLGIS
#               
#      Copyright (C) by elgis ( https://elgis.de ) 2022
# Diese Datei ist Bestandteil der Software elgis2inspire, erhältlich unter https://github.com/elgis-frank/elgis2inspire .
# Diese Software wird unter der European Union Public Licence (EUPL-1.2) bereitgestellt. Bitte beachten Sie die Bestimmungen der Lizenz, insbesondere
# zur Bereitstellung und Nutzung der Software und zum Haftungsausschluss. Die Lizenz ist in allen Amtssprachen der EU veröffentlicht unter https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
# 
#--------------------------------------------------------

import sys
from xml.sax import saxutils, make_parser, parseString
import mapscript
import sqlite3
#import spatialite
from datetime import datetime

#Vorbereitung

# Read database*********************************
# hier wird aus der Datenbank ausgelesen
class InspireDB:
	def __init__(self, name):
		self.name = name
		

	def sddataset(self):
		conn = sqlite3.connect('/var/www/inspire/db.sqlite3')
		c = conn.cursor()
		t = (self.name,)
		l = []		
		for row in c.execute('select localID, namespace, versionId, name, beginLifespanVersion, endLifespanVersion, domainExtent from sd_speciesdistributiondataset where localID = ?', t):
			l.append(row)
		inid = l
		return inid	

	def sdunit(self):
		conn = sqlite3.connect('/var/www/inspire/db.sqlite3')
		c = conn.cursor()
		t = (self.name,"""+sdi+""" )
		l = []		
		for row in c.execute('select sddi, localID, namespace, referenceSpeciesId, referenceSpeciesScheme, referenceSpeciesName from sd_speciesdistributionunit where localID = ? AND sddi = ?' , t):
			l.append(row)
		sdt = l
		return sdt
		
# class zum parsen*********************************
# XMLGenerator Klasse*******************************
# **************************************************
class Tweak(saxutils.XMLGenerator):
	def startElement(self, name, attrs):
		if name == 'wfs:FeatureCollection':
			if 'next' in attrs:
				xsi = attrs['xsi:schemaLocation']
				# 3 gml Versionen berücksichtigen
				if 'http://www.opengis.net/gml/3.2' in xsi:
					gml = 'http://www.opengis.net/gml/3.2'
					gml1 = 'http://www.opengis.net/gml/3.2 http://schemas.opengis.net/gml/3.2.1/gml.xsd'
				elif 'http://schemas.opengis.net/gml/3.1.1/base/gml.xsd' in xsi:
					gml = 'http://www.opengis.net/gml'
					gml1 = 'http://www.opengis.net/gml http://schemas.opengis.net/gml/3.1.1/base/gml.xsd'
				elif 'http://schemas.opengis.net/gml/2.1.2/feature.xsd' in xsi:
					gml = 'http://www.opengis.net/gml'
					gml1 = 'http://www.opengis.net/gml http://schemas.opengis.net/gml/2.1.2/feature.xsd'
				co = attrs['next']
				ts = attrs['timeStamp']
				nm = attrs['numberMatched']
				nr = attrs['numberReturned']
				attrs = {'xmlns:sd':"http://inspire.ec.europa.eu/schemas/sd/4.0", 'xmlns:wfs':"http://www.opengis.net/wfs/2.0", 'xmlns:ad':"http://inspire.ec.europa.eu/schemas/ad/4.0", 
				'xmlns:base':"http://inspire.ec.europa.eu/schemas/base/3.3",'xmlns:base2':"http://inspire.ec.europa.eu/schemas/base2/2.0",
				'xmlns:gco':"http://www.isotc211.org/2005/gco",'xmlns:gmd':"http://www.isotc211.org/2005/gmd",'xmlns:gml':gml,
				'xmlns:gn':"http://inspire.ec.europa.eu/schemas/gn/4.0", 'xmlns:gsr':"http://www.isotc211.org/2005/gsr", 'xmlns:gss':"http://www.isotc211.org/2005/gss", 
				'xmlns:gts':"http://www.isotc211.org/2005/gts", 'xmlns:sd':"http://inspire.ec.europa.eu/schemas/sd/4.0", 'xmlns:xlink':"http://www.w3.org/1999/xlink", 
				'xmlns:xml':"http://www.w3.org/XML/1998/namespace", 'xmlns:xsi':"http://www.w3.org/2001/XMLSchema-instance", 
				'xsi:schemaLocation':"http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0/wfs.xsd http://inspire.ec.europa.eu/schemas/sd/4.0 http://inspire.ec.europa.eu/schemas/sd/4.0/SpeciesDistribution.xsd  " + gml1, 'timeStamp':ts,'numberMatched':nm,'numberReturned':nr, 'next': co}
			else:
				xsi = attrs['xsi:schemaLocation']
			# 3 gml Versionen berücksichtigen
				if 'http://www.opengis.net/gml/3.2' in xsi:
					gml = 'http://www.opengis.net/gml/3.2'
					gml1 = 'http://www.opengis.net/gml/3.2 http://schemas.opengis.net/gml/3.2.1/gml.xsd'
				elif 'http://schemas.opengis.net/gml/3.1.1/base/gml.xsd' in xsi:
					gml = 'http://www.opengis.net/gml'
					gml1 = 'http://www.opengis.net/gml http://schemas.opengis.net/gml/3.1.1/base/gml.xsd'
				elif 'http://schemas.opengis.net/gml/2.1.2/feature.xsd' in xsi:
					gml = 'http://www.opengis.net/gml'
					gml1 = 'http://www.opengis.net/gml http://schemas.opengis.net/gml/2.1.2/feature.xsd'
				ts = attrs['timeStamp']
				nm = attrs['numberMatched']
				nr = attrs['numberReturned']
				attrs = {'xmlns:sd':"http://inspire.ec.europa.eu/schemas/sd/4.0", 'xmlns:wfs':"http://www.opengis.net/wfs/2.0", 'xmlns:ad':"http://inspire.ec.europa.eu/schemas/ad/4.0", 
				'xmlns:base':"http://inspire.ec.europa.eu/schemas/base/3.3",'xmlns:base2':"http://inspire.ec.europa.eu/schemas/base2/2.0",'xmlns:gco':"http://www.isotc211.org/2005/gco",
				'xmlns:gmd':"http://www.isotc211.org/2005/gmd",'xmlns:gml':gml,'xmlns:gn':"http://inspire.ec.europa.eu/schemas/gn/4.0", 
				'xmlns:gsr':"http://www.isotc211.org/2005/gsr", 'xmlns:gss':"http://www.isotc211.org/2005/gss", 'xmlns:gts':"http://www.isotc211.org/2005/gts", 
				'xmlns:sd':"http://inspire.ec.europa.eu/schemas/sd/4.0", 'xmlns:xlink':"http://www.w3.org/1999/xlink", 'xmlns:xml':"http://www.w3.org/XML/1998/namespace", 
				'xmlns:xsi':"http://www.w3.org/2001/XMLSchema-instance",'xsi:schemaLocation':"http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0/wfs.xsd http://inspire.ec.europa.eu/schemas/sd/4.0 http://inspire.ec.europa.eu/schemas/sd/4.0/SpeciesDistribution.xsd  " + gml1, 'timeStamp':ts,'numberMatched':nm,'numberReturned':nr}
		if name == 'wfs:boundedBy':
			e = InspireDB("""+sdi+""").sddataset()
			# Zeit von Datum auf datetime ändern
			# to do Zeitformat ermitteln
			zeit1 = e[0][4] + ' 00:00:00'
			date1 = datetime.strptime(zeit1, '%d.%m.%Y %H:%M:%S')
			dt1 = date1.strftime("%Y-%m-%dT%H:%M:%S")
			zeit2 = e[0][5] + ' 00:00:00'
			date2 = datetime.strptime(zeit2, '%d.%m.%Y %H:%M:%S')
			dt2 = date2.strftime("%Y-%m-%dT%H:%M:%S")
			print('<sd:SpeciesDistributionDataSet gml:id="SpeciesDistributionDataSet.' + str(e[0][0]) + '">')
			print('<sd:inspireId>')
			print('<base:Identifier>')
			print('<base:localId>SpeciesDistributionDataSet.'+ str(e[0][0]) + '</base:localId>')
			print('<base:namespace>' + e[0][1] + '</base:namespace>')
			print('<base:versionId >' + e[0][2] + '</base:versionId>')
			print('</base:Identifier>')
			print('</sd:inspireId>')
			print('<sd:name >sd:' + e[0][3] + '</sd:name>')
			print('<sd:domainExtent  xlink:href="' + e[0][6] + '" ></sd:domainExtent>')
			print('<sd:beginLifespanVersion>' + dt1 + '</sd:beginLifespanVersion>')
			print('<sd:endLifespanVersion >' + dt2 + '</sd:endLifespanVersion>')
			print('<sd:documentBasis nilReason="inapplicable" />')
		if name == 'sd:msGeometry':
			name = 'sd:geometry'
		saxutils.XMLGenerator.startElement(self, name,  attrs)
		if name == 'sd:SpeciesDistributionUnit':
			#wegen anderer gml Version vom Geoportal
			if 'gml:id' in attrs:
				qid = attrs['gml:id']
			else:
				qid = attrs['fid']
			n = qid.split('.')
			fid = int(n[1])
			#fid = n
			el = InspireDB(fid).sdunit()
			print('<sd:inspireId>')
			print('<base:Identifier>')
			print('<base:localId>SpeciesDistributionUnit.' + el[0][1] + '</base:localId>')
			print('<base:namespace>' + el[0][2] + '</base:namespace>')
			print('</base:Identifier>')
			print('</sd:inspireId>')
			print('<sd:speciesName>')
			print('<sd:SpeciesNameType>')
			print('<sd:referenceSpeciesId xlink:actuate="onLoad"  xlink:href="' + el[0][3] + '"/>')
			print('<sd:referenceSpeciesScheme  xlink:actuate="onLoad"  xlink:href="' + el[0][4] + '"/>')
			print('<sd:referenceSpeciesName >sd:' + el[0][5] + '</sd:referenceSpeciesName>')
			print('</sd:SpeciesNameType>')
			print('</sd:speciesName>')
			print('<sd:distributionInfo nilReason="http://inspire.ec.europa.eu/codelist/VoidReasonValue/Unpopulated"/>')
	def	endElement(self, name):
		if name == 'sd:msGeometry':
			name = 'sd:geometry' 
		if name == 'wfs:FeatureCollection':
			print('</sd:SpeciesDistributionDataSet>')
		saxutils.XMLGenerator.endElement(self, name)
# Ende XMLGeneratorklasse main *********************************************
# **************************************************************************
# **************************************************************************	
#  XMLGenerator Klasse für stored query extra*******************************	
class Tweakn(saxutils.XMLGenerator):
	gmlid = ''
	def startElement(self, name, attrs):
		e = InspireDB("""+sdi+""").sddataset()
		# Zeit von Datum auf datetime ändern
		# to do Zeitformat ermitteln
		zeit1 = e[0][4] + ' 00:00:00'
		date1 = datetime.strptime(zeit1, '%d.%m.%Y %H:%M:%S')
		dt1 = date1.strftime("%Y-%m-%dT%H:%M:%S")
		zeit2 = e[0][5] + ' 00:00:00'
		date2 = datetime.strptime(zeit2, '%d.%m.%Y %H:%M:%S')
		dt2 = date2.strftime("%Y-%m-%dT%H:%M:%S")
		gml = 'http://www.opengis.net/gml/3.2'
		gml1 = 'http://www.opengis.net/gml/3.2 http://schemas.opengis.net/gml/3.2.1/gml.xsd'
		if name == 'sd:SpeciesDistributionUnit':
			self.gmlid = attrs['gml:id']
			name = 'sd:SpeciesDistributionDataSet'
			attrs = { 'gml:id':'SpeciesDistributionDataSet.'+str(e[0][0]), 'xmlns:sd':"http://inspire.ec.europa.eu/schemas/sd/4.0", 'xmlns:wfs':"http://www.opengis.net/wfs/2.0", 'xmlns:ad':"http://inspire.ec.europa.eu/schemas/ad/4.0", 
				'xmlns:base':"http://inspire.ec.europa.eu/schemas/base/3.3",'xmlns:base2':"http://inspire.ec.europa.eu/schemas/base2/2.0",'xmlns:gco':"http://www.isotc211.org/2005/gco",
				'xmlns:gmd':"http://www.isotc211.org/2005/gmd",'xmlns:gml':gml,'xmlns:gn':"http://inspire.ec.europa.eu/schemas/gn/4.0", 
				'xmlns:gsr':"http://www.isotc211.org/2005/gsr", 'xmlns:gss':"http://www.isotc211.org/2005/gss", 'xmlns:gts':"http://www.isotc211.org/2005/gts", 
				'xmlns:sd':"http://inspire.ec.europa.eu/schemas/sd/4.0", 'xmlns:xlink':"http://www.w3.org/1999/xlink", 'xmlns:xml':"http://www.w3.org/XML/1998/namespace", 
				'xmlns:xsi':"http://www.w3.org/2001/XMLSchema-instance",'xsi:schemaLocation':"http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0/wfs.xsd http://inspire.ec.europa.eu/schemas/sd/4.0 http://inspire.ec.europa.eu/schemas/sd/4.0/SpeciesDistribution.xsd  " + gml1}
		if name == 'gml:boundedBy':
			print('<sd:inspireId>')
			print('<base:Identifier>')
			print('<base:localId>SpeciesDistributionDataSet.'+ str(e[0][0]) + '</base:localId>')
			print('<base:namespace>' + e[0][1] + '</base:namespace>')
			print('<base:versionId >' + e[0][2] + '</base:versionId>')
			print('</base:Identifier>')
			print('</sd:inspireId>')
			print('<sd:name >sd:' + e[0][3] + '</sd:name>')
			print('<sd:domainExtent  xlink:href="' + e[0][6] + '" ></sd:domainExtent>')
			print('<sd:beginLifespanVersion>' + dt1 + '</sd:beginLifespanVersion>')
			print('<sd:endLifespanVersion >' + dt2 + '</sd:endLifespanVersion>')
			print('<sd:documentBasis nilReason="inapplicable" />')
		if name == 'sd:msGeometry':
			name= 'sd:geometry'
			qid = self.gmlid
			n = qid.split('.')
			fid = int(n[1])
			el = InspireDB(fid).sdunit()
			print('<sd:SpeciesDistributionUnit gml:id="'+self.gmlid +'">')
			print('<sd:inspireId>')
			print('<base:Identifier>')
			print('<base:localId>base:' + el[0][1] + '</base:localId>')
			print('<base:namespace>base:' + el[0][2] + '</base:namespace>')
			print('</base:Identifier>')
			print('</sd:inspireId>')
			print('<sd:speciesName>')
			print('<sd:SpeciesNameType>')
			print('<sd:referenceSpeciesId xlink:actuate="onLoad"  xlink:href="' + el[0][3] + '"/>')
			print('<sd:referenceSpeciesScheme  xlink:actuate="onLoad"  xlink:href="' + el[0][4] + '"/>')
			print('<sd:referenceSpeciesName >sd:' + el[0][5] + '</sd:referenceSpeciesName>')
			print('</sd:SpeciesNameType>')
			print('</sd:speciesName>')
			print('<sd:distributionInfo nilReason="http://inspire.ec.europa.eu/codelist/VoidReasonValue/Unpopulated"/>')
		saxutils.XMLGenerator.startElement(self, name,  attrs)
	def	endElement(self, name):
		if name == 'sd:msGeometry':
			name = 'sd:geometry'
		if name == 'sd:SpeciesDistributionUnit':
			name = 'sd:SpeciesDistributionDataSet'
			print('</sd:SpeciesDistributionUnit>')
		saxutils.XMLGenerator.endElement(self, name)
# Ende der class für storedquery
# Ende der Vorbereitung*****************************************************************
req = mapscript.OWSRequest()
req.loadParams()
if req.getValueByName('csrftoken'):
	req.setParameter('csrftoken',None)
if req.getValueByName('sessionid'):
	req.setParameter('sessionid',None)
# Abfrage abfangen
reco1 = req.getValueByName('REQUEST')
#wenn kein request Parameter vorhanden ist
if not reco1:
	reco1 = 'Fault'
reco = reco1.lower()
#für resultType=hits
zusatz = req.getValueByName('resultType')
#falls der typename falsch ist bei describefeaturetype
typename = req.getValueByName('typename')
if typename == 'SpeciesDistribution' or typename == None:
	typename = "OK"
#Abfrage nach der storedquery_id
squery = req.getValueByName('storedquery_id')
if squery == 'urn:ogc:def:query:OGC-WFS::GetFeatureById':
	squery = 'OK'
	map = mapscript.mapObj( '/var/www/inspire/dok/sd_query.map' )
else:
	map = mapscript.mapObj( '/var/www/inspire/dok/sd_d"""+sdi+""".map' )
#bei Abfragen über die featureid
fid = req.getValueByName('featureid')
if not fid:
	pass
else:
	fidn = 'OK'
	map = mapscript.mapObj( '/var/www/inspire/dok/sd_query.map' )
#Frage nachfehlenden Parametern
names = req.getValueByName('typenames')
tn = 'false'
if names == 'speciesdistributionunit' or names == 'SpeciesDistributionUnit' or names == 'SpeciesDistributionunit':
	tn = 'true'
elif not names:
	tn = 'true'
gml = req.getValueByName('outputFormat')
#verschiedene Versionen einspielen
if gml == 'application/gml+xml; version=3.2'  or gml == 'text/xml; subtype=gml/3.2.1':
	dokxsd = "/var/www/inspire/dok/xsd/SpeciesDistribution.xsd"
elif gml == 'text/xml; subtype=gml/3.1.1':
	dokxsd = "/var/www/inspire/dok/xsd/SpeciesDistribution_3.1.xsd"
elif gml == 'text/xml; subtype=gml/2.1.2':
	dokxsd = "/var/www/inspire/dok/xsd/SpeciesDistribution_2.1.xsd"
elif not gml:
	dokxsd = "/var/www/inspire/dok/xsd/SpeciesDistribution.xsd"
else:
	tn = 'false'
#fehlender service parameter
recop3 = req.getValueByName('SERVICE')
if recop3:
  recol = recop3.lower()

if not recop3 or recol != 'wfs' :
	answer = '''<?xml version="1.0" encoding="UTF-8"?>
<ows:ExceptionReport xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ows="http://www.opengis.net/ows/1.1" version="2.0.0" xml:lang="en-US" xsi:schemaLocation="http://www.opengis.net/ows/1.1 http://schemas.opengis.net/ows/1.1.0/owsExceptionReport.xsd">
  <ows:Exception exceptionCode="InvalidParameterValue" locator="request">
    <ows:ExceptionText>msWFSDispatch(): WFS server error. Invalid Service request: Parameter wrong or missing</ows:ExceptionText>
  </ows:Exception>
</ows:ExceptionReport>
    '''
	print('header:text/xml')
	print('')
	print(answer)	
#  Abfragen
elif reco == 'describefeaturetype' and tn == 'true':
	mapscript.msIO_installStdoutToBuffer()
	map.OWSDispatch( req )
	ct = mapscript.msIO_stripStdoutBufferContentType()
	content = mapscript.msIO_getStdoutBufferString()
	mapscript.msIO_resetHandlers()
	f = open(dokxsd)
	xsd = f.read()
	#print('Content-type: ' + ct)
	print('Content-type:text/xml' )
	print('')
	print(xsd)
	

# Do special processing for GetFeature
#
elif reco == 'getfeature' and zusatz == None and squery == None: 
	mapscript.msIO_installStdoutToBuffer()

	map.OWSDispatch( req )

	ct = mapscript.msIO_stripStdoutBufferContentType()
	content = mapscript.msIO_getStdoutBufferString()
	mapscript.msIO_resetHandlers()

			
		  
	dh = Tweak(sys.stdout)
	print('Content-type: ' + ct)
	print('')
	parseString(content, dh)


elif reco == 'getfeature' and zusatz == None and squery == 'OK': #für storedquery
	mapscript.msIO_installStdoutToBuffer()

	map.OWSDispatch( req )

	ct = mapscript.msIO_stripStdoutBufferContentType()
	content = mapscript.msIO_getStdoutBufferString()
	mapscript.msIO_resetHandlers()

	if (content.__contains__('ows:ExceptionReport')):
		print(content)
	else:
		dh = Tweakn(sys.stdout,encoding='utf-8')
		print('Content-type: ' + ct)
		print('')
		parseString(content, dh)

elif reco == 'getfeature' and zusatz == None and squery == None and fidn == 'OK': #für featureid
	mapscript.msIO_installStdoutToBuffer()

	map.OWSDispatch( req )

	ct = mapscript.msIO_stripStdoutBufferContentType()
	content = mapscript.msIO_getStdoutBufferString()
	mapscript.msIO_resetHandlers()

	if (content.__contains__('ows:ExceptionReport')):
		print(content)
	else:
		dh = Tweakn(sys.stdout,encoding='utf-8')
		print('Content-type: ' + ct)
		print('')
		parseString(content, dh)


else:
	map.OWSDispatch( req )
  """
  #Ende des python wfs files
  #*******************************************
  # wms python file
  #*******************************************
  pywms = """#!/usr/bin/python3
#-------------------------------------------------------
# Datei sd_wms Version 1.01 
#
#  Programming by eLGIS
#               
#      Copyright (C) by elgis ( https://elgis.de ) 2022
# Diese Datei ist Bestandteil der Software elgis2inspire, erhältlich unter https://github.com/elgis-frank/elgis2inspire .
# Diese Software wird unter der European Union Public Licence (EUPL-1.2) bereitgestellt. Bitte beachten Sie die Bestimmungen der Lizenz, insbesondere
# zur Bereitstellung und Nutzung der Software und zum Haftungsausschluss. Die Lizenz ist in allen Amtssprachen der EU veröffentlicht unter https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
# 
#--------------------------------------------------------

import mapscript



req = mapscript.OWSRequest()
req.loadParams()
map = mapscript.mapObj( '/var/www/inspire/dok/sd_d""" +sdi+"""_wms.map' )
#Frage nachfehlenden Parametern
serv = req.getValueByName('service')
rq = req.getValueByName('request')
if serv == 'wms' or serv == 'WMS' :
    s = 'true'
else:
    s = 'false'
if rq == 'GetMap' or rq == 'getmap' or rq == 'Getmap' and s == 'true':
    styl = req.getValueByName('styles')
    if not styl:
        answer = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<ServiceExceptionReport version="1.3.0" xmlns="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/ogc http://schemas.opengis.net/wms/1.3.0/exceptions_1_3_0.xsd">
<ServiceException>
msWMSDispatch(): WMS server error. Styles parameter missing
</ServiceException>
</ServiceExceptionReport>'''
        print('Content-type:text/xml' )
        print('')
        print(answer)
    else:
        map.OWSDispatch( req )
elif s == 'true':
    map.OWSDispatch( req )
else:
    answer = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<ServiceExceptionReport version="1.3.0" xmlns="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/ogc http://schemas.opengis.net/wms/1.3.0/exceptions_1_3_0.xsd">
<ServiceException>
msWMSDispatch(): WMS server error. Styles parameter missing
</ServiceException>
</ServiceExceptionReport>'''
    print('Content-type:text/xml' )
    print('')
    print(answer)

"""
  #**********wms.py file ******
  wfspyfile = Path(path+"python/sd_d" + sdi + "_wfs")
  if wfspyfile.is_file():
      os.remove(wfspyfile)
  with open(path+"python/sd_d"+ sdi +"_wfs", "w", encoding='utf8') as wfspy_file:
    wfspy_file.write(pysdwfs)
  os.chmod(path+"python/sd_d"+ sdi +"_wfs", stat.S_IRWXU)
  #************wms.py file ************************
  wmspyfile = Path(path+"python/sd_d" + sdi + "_wms")
  if wmspyfile.is_file():
      os.remove(wmspyfile)
  with open(path+"python/sd_d"+ sdi +"_wms", "w", encoding='utf8') as wmspy_file:
    wmspy_file.write(pywms)
#**********Ende wms file
  os.chmod(path+"python/sd_d"+ sdi +"_wms", stat.S_IRWXU)
  wfsfile = Path(path+"dok/sd_d"+sdi+".map")
  if wfsfile.is_file():
    os.remove(wfsfile)
  with open(path+"dok/sd_d"+sdi+".map", "w", encoding='utf8') as wfs_file:
    wfs_file.write(sdwfs)
  os.chmod(path+"dok/sd_d"+sdi+".map", stat.S_IRWXU)
  wmsfile = Path(path+"dok/sd_d"+sdi+"_wms.map")
  if wmsfile.is_file():
    os.remove(wmsfile)
  with open(path+"dok/sd_d"+sdi+"_wms.map", "w", encoding='utf8') as wms_file:
    wms_file.write(sdwms)
  os.chmod(path+"dok/sd_d"+sdi+"_wms.map", stat.S_IRWXU)
  return 'Daten geladen und alle mapfiles geschrieben'

   





