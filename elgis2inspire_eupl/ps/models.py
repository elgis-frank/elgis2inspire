#-------------------------------------------------------
# Datei ps.models.py Version 1.01 
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

class ProtectedSite(models.Model):
    psid = models.AutoField(primary_key=True)
    featureid = models.IntegerField(null=True)
    localID = models.TextField(unique=True)
    idnamespace = models.TextField(blank=True,null=True)
    legalfoundationdate = models.TextField(blank=True,null=True)
    legalfoundationdocument = models.TextField(blank=True,null=True)
    sitename = models.TextField(blank=True,null=True)
    ps_type = models.TextField(blank=True,null=True)
    the_geom = models.MultiPolygonField(srid=3035)

class SiteDesignation(models.Model):
    sid = models.AutoField(primary_key=True)
    fid = models.IntegerField(null=True)
    designation = models.TextField(blank=True,null=True)
    designationScheme = models.TextField(blank=True,null=True)
    percentageUnderDesignation = models.TextField(blank=True,null=True)


class SiteProtectionClassification(models.Model):
    pid = models.AutoField(primary_key=True)
    fid = models.IntegerField(null=True)
    siteProtectionClassification = models.TextField(blank=True,null=True)

    
    