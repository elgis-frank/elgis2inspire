#-------------------------------------------------------
# Datei sd.forms.py Version 1.01 
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
from .models import SpeciesDistributionDataSet


class sdGeoForm(forms.Form):
    datei      = forms.FileField(label='Wählen Sie für Verbreitung von Arten eine geojson Datei aus') # Geodatensatz
    data_select = forms.ModelChoiceField(queryset=SpeciesDistributionDataSet.objects.all(), empty_label=None, label='wählen Sie den speciesDistributionDataset')
    name = forms.CharField(label='Attributname des wiss. Artnamens')
    fid = forms.CharField(label='Attributname der featureid')
    nmsp = forms.CharField(label='Attributname des namespace')
    

class delGeoForm(forms.Form):    
    data_select = forms.ModelChoiceField(queryset=SpeciesDistributionDataSet.objects.all(), empty_label=None, label='wählen Sie den speciesDistributionDataset')
  
class sdFormdataset(forms.ModelForm):
    class Meta:
        model = SpeciesDistributionDataSet
        fields = ['localID','namespace', 'versionId', 'name', 'beginLifespanVersion', 'endLifespanVersion', 'domainExtent', 'title_ger', 'abstract_eng', 'abstract_ger', 'keywords_eng']
        labels = {
            'title_ger':('Titel der Dienste auf Deutsch'),
            'name': ('Benennung des Datensatzes auf Englisch'),
            'namespace': ('Namespace'),
            'versionId': ('Versionsnummer'),
            'beginLifespanVersion': ('Beginn des Untersuchungszeitraumes'),
            'endLifespanVersion': ('Ablauf der Daten'),
            'domainExtent':('URL zur Abgrenzung des Verbreitungsgebietes'),
            'abstract_eng':('Kurzfassung auf Englisch'),
            'abstract_ger':('Kurzfassung auf Deutsch'),
            'keywords_eng':('Schlüsselwörter auf Englisch'),
                }
        widgets = {
            'localID': forms.HiddenInput(),
            'namespace': forms.Textarea(attrs={'cols': 40, 'rows': 1}),
            'versionId': forms.Textarea(attrs={'cols': 20, 'rows': 1}),
            'name': forms.Textarea(attrs={'cols': 40, 'rows': 1}),
            'beginLifespanVersion': forms.Textarea(attrs={'cols': 20, 'rows': 1}),
            'endLifespanVersion': forms.Textarea(attrs={'cols': 20, 'rows': 1}),
            'domainExtent': forms.Textarea(attrs={'cols': 40, 'rows': 1}),
            'title_ger': forms.Textarea(attrs={'cols': 40, 'rows': 1}),
            'abstract_eng': forms.Textarea(attrs={'cols': 40, 'rows': 1}), 
            'abstract_ger': forms.Textarea(attrs={'cols': 40, 'rows': 1}),
            'keywords_eng': forms.Textarea(attrs={'cols': 40, 'rows': 1}),
                }

