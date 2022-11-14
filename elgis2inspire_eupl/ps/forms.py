#-------------------------------------------------------
# Datei ps.forms.py Version 1.01 
#
#  Programming by eLGIS
#               
#      Copyright (C) by elgis ( https://elgis.de ) 2022
# Diese Datei ist Bestandteil der Software elgis2inspire, erhältlich unter https://github.com/elgis-frank/elgis2inspire .
# Diese Software wird unter der European Union Public Licence (EUPL-1.2) bereitgestellt. Bitte beachten Sie die Bestimmungen der Lizenz, insbesondere
# zur Bereitstellung und Nutzung der Software und zum Haftungsausschluss. Die Lizenz ist in allen Amtssprachen der EU veröffentlicht unter https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
# 
#--------------------------------------------------------


from django import forms
#from .models import ProtectedSite
from django.utils.html import format_html




class psGeoForm(forms.Form):    
    datei      = forms.FileField(label='Wählen Sie für protected sites eine geojson Datei aus') # Geodatensatz
    spkenn = forms.CharField(label='Attributname der Kennung')
    spname = forms.CharField(label='Attributname des Namens')
    spurl = forms.CharField(label='Attributname der URL der Rechtsgrundlage')
    spdate = forms.CharField(label='Attributname Datum der Unterschutzstellung')
    sptype = forms.CharField(label='Attributname des Schutzgebiettyps')
    
