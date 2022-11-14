#-------------------------------------------------------
# Datei sd.models.py Version 1.01 
#
#  Programming by eLGIS
#               
#      Copyright (C) by elgis ( https://elgis.de ) 2022
# Diese Datei ist Bestandteil der Software elgis2inspire, erhältlich unter https://github.com/elgis-frank/elgis2inspire .
# Diese Software wird unter der European Union Public Licence (EUPL-1.2) bereitgestellt. Bitte beachten Sie die Bestimmungen der Lizenz, insbesondere
# zur Bereitstellung und Nutzung der Software und zum Haftungsausschluss. Die Lizenz ist in allen Amtssprachen der EU veröffentlicht unter https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
# 
#--------------------------------------------------------

from django.contrib.gis.db import models


# Create your models here.
class SpeciesDistributionUnit(models.Model):
    sdid = models.AutoField(primary_key=True)
    sddi = models.TextField(blank=True,null=True)
    localID = models.TextField(blank=True,null=True)
    namespace = models.TextField(blank=True,null=True)
    referenceSpeciesId = models.TextField(blank=True,null=True)
    referenceSpeciesScheme = models.TextField(blank=True,null=True)
    referenceSpeciesName = models.TextField(blank=True,null=True)
    cellcode = models.TextField(blank=True,null=True)
    the_geom = models.PolygonField(srid=3035,null=True)   
    

class DistributionInfoType(models.Model):
    did = models.AutoField(primary_key=True)
    fid = models.IntegerField(blank=True,null=True)
    occurrenceCategory = models.TextField(blank=True,null=True)
    collectedFrom = models.TextField(blank=True,null=True)
    collectedTo = models.TextField(blank=True,null=True)
    sizecountingM = models.TextField(blank=True,null=True)
    sizecountingU = models.TextField(blank=True,null=True)
    sizelowerB = models.TextField(blank=True,null=True)
    sizeupperB = models.TextField(blank=True,null=True)
    populationType = models.TextField(blank=True,null=True)
    residencyStatus = models.TextField(blank=True,null=True)  
    sensitiveInfo = models.TextField(blank=True,null=True)

class SpeciesDistributionDataSet(models.Model):
    def __str__(self):
        return self.name

    sddi = models.AutoField(primary_key=True)
    localID = models.IntegerField(blank=True,null=True)
    namespace = models.TextField(null=True)
    versionId = models.TextField(null=True)
    name = models.TextField(null=True)
    beginLifespanVersion = models.TextField(null=True)
    endLifespanVersion = models.TextField(null=True)
    domainExtent = models.TextField(null=True)
    title_ger = models.TextField(null=True)
    abstract_eng = models.TextField(blank=True,null=True)
    abstract_ger = models.TextField(blank=True,null=True)
    keywords_eng = models.TextField(blank=True,null=True)
    keywords_ger = models.TextField(blank=True,null=True)

class DocumentCitation(models.Model):
    dcid = models.AutoField(primary_key=True)
    name = models.TextField(blank=True,null=True)
    shortName = models.TextField(blank=True,null=True) 
    date = models.TextField(blank=True,null=True)
    

class CitationUrl(models.Model):
    urid = models.AutoField(primary_key=True)
    dcid = models.IntegerField(blank=True,null=True)
    link = models.TextField(blank=True,null=True)
    specificReference = models.TextField(blank=True,null=True)

class Artenliste(models.Model):
    artid = models.AutoField(primary_key=True)
    name = models.TextField(blank=True,null=True)
    localname = models.TextField(blank=True,null=True)
    deutname = models.TextField(blank=True,null=True)
    guid = models.TextField(blank=True,null=True)

class faultguid(models.Model):
    faid = models.AutoField(primary_key=True)
    name = models.TextField(blank=True,null=True)
    pruef = models.IntegerField(blank=True,null=True)



