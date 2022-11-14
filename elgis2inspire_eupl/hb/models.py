#-------------------------------------------------------
# Datei hb.models.py Version 1.01 
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

#from model_utils import Choices

class Lebensraumtyp(models.Model):
    ltid = models.AutoField(primary_key=True)
    ltcode = models.TextField(null=True)
    ltlongname = models.TextField(null=True)
    ltshortname = models.TextField(null=True)

class Habitat(models.Model):
    id = models.AutoField(primary_key=True)
    featureID = models.IntegerField(unique=True)
    idnamespace = models.TextField(blank=True,null=True)
    lcode = models.TextField(blank=True,null=True)
    n2000 = models.TextField(blank=True,null=True)
    the_geom = models.MultiPolygonField(srid=3035,null=True)
    icode = models.TextField(blank=True,null=True)
    iname = models.TextField(blank=True,null=True)
    scheme = models.TextField(blank=True,null=True)

class HabitatList(models.Model):
    hlid = models.AutoField(primary_key=True)
    lcode = models.TextField(unique=True)
    lname = models.TextField(blank=True,null=True,unique=True)
    icode = models.TextField(blank=True,null=True)
    iname = models.TextField(blank=True,null=True)
    localid = models.TextField()
    rang = models.IntegerField(blank=True,null=True)
    imatch = models.TextField(null=True, default='http://inspire.ec.europa.eu/codelist/QualifierLocalNameValue/congruent')
    class Meta:
        permissions = [("edit_list", "Liste editieren"),]
    

class HabitatTypeCoverType(models.Model):
    hid = models.AutoField(primary_key=True)
    fid = models.IntegerField()
    referenceHabitatTypeScheme = models.TextField(blank=True,null=True)
    referenceHabitatTypeId = models.TextField(blank=True,null=True)
    referenceHabitatTypeName = models.TextField(blank=True,null=True)
    

class LocalNameType(models.Model):
    lid = models.AutoField(primary_key=True)
    fid = models.IntegerField()
    localScheme = models.TextField(blank=True,null=True)
    localNameCode = models.TextField(blank=True,null=True)
    localName = models.TextField(blank=True,null=True)
    qualifierLocalName = models.TextField(blank=True,null=True)
    label = models.TextField(blank=True,null=True)
    

class HabitatVegetationType(models.Model):
    vid = models.AutoField(primary_key=True)
    fid = models.IntegerField()
    localScheme = models.TextField(blank=True)
    localNameCode = models.TextField(blank=True,null=True)
    localName = models.TextField(blank=True,null=True)
    qualifierLocalName = models.TextField(blank=True,null=True)
    

class HabitatSpeciesType(models.Model):
    sid = models.AutoField(primary_key=True)
    fid = models.IntegerField()
    referenceSpeciesId = models.TextField(blank=True,null=True)
    referenceSpeciesScheme = models.TextField(blank=True,null=True)
    localScheme = models.TextField(blank=True,null=True)
    localNameCode = models.TextField(blank=True,null=True)
    localName = models.TextField(blank=True,null=True)
    qualifierLocalName = models.TextField(blank=True,null=True)
    




