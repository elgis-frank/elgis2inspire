#-------------------------------------------------------
# Datei main.forms.py Version 1.01 
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
from .models import HabitatList, Capabilities
from django.utils.html import format_html




class GeodatForm(forms.Form):    
    datei      = forms.FileField(label='Wählen Sie für die Geodaten eine geojson Datei') # Geodatensatz
    spfid = forms.CharField(label='Spaltename der featureid')
    splcode = forms.CharField(label='Spaltename des Biotoptyps')
    spn2000 = forms.CharField(label='Spaltename des Lebensraumtyps')
    nmspace = forms.CharField(label='Namespace des Habitatdatensatzes (Basis URL)')

class attributForm(forms.Form):
    csvdat = forms.FileField(label='Wählen Sie die csv Datei') # csv Datensatz
    

class HabitatListForm(forms.ModelForm):
       

    class Meta:
        model = HabitatList
        
        match_choice = ( ('congruent','kongruent'), ('excludes', 'schließt aus'), ('includedIn', 'enthalten'), ('includes','enthält'), ('overlaps', 'überlappt'))
        fields = ['lcode', 'lname', 'icode', 'iname', 'imatch', 'hlid']
        labels = {
            'lcode': ('Localcode'),
            'lname': ('Localname'),
            'icode': ('EUNIS Code'),
            'iname': ('EUNIS Name'),
            'imatch': ('Übereinstimmung'),
            
        }
        widgets = {
            'lcode': forms.Textarea(attrs={'cols': 40, 'rows': 1}),
            'lname': forms.Textarea(attrs={'cols': 40, 'rows': 1}),
            'icode': forms.HiddenInput(),
            "iname": forms.Textarea(attrs={"onclick": "startTree()", "cols": 40, "rows": 1}),
            'imatch': forms.Select(choices=match_choice),
            'hlid': forms.HiddenInput(),
            
        }

class CapabilitiesForm(forms.ModelForm):
    class Meta:
        model = Capabilities
        
        fields = [ 'ows_inspire_temporal_reference', 'ows_inspire_mpoc_name', 'ows_inspire_mpoc_email', 'ows_inspire_metadatadate', 'ows_inspire_resourcelocator', 'contactperson', 
'ows_hoursofservice', 'ows_contactinstructions', 'contactposition', 'contactvoicetelephone', 'ows_contactfacsimiletelephone', 'contactelectronicmailaddress', 'postcode', 'address', 'city',
'stateorprovince', 'addresstype', 'ows_service_onlineresource', 'ows_role', 'ows_inspire_dsid_code', 'ows_inspire_dsid_ns', 'meta_uri','cid', 'authorityurl_name','authorityurl_href','contactorganisation', 'inspirelayer','sddi',]
        labels = {
            'ows_inspire_temporal_reference' : ('zeitliche Referenz'),          
            'ows_inspire_mpoc_name': ('Name des Kontaktpunktes '),
            'ows_inspire_mpoc_email': ('mail Adresse des Kontaktpunktes'),
            'ows_inspire_metadatadate': ('letzte Änderung der Metadaten'),
            'ows_inspire_resourcelocator': ('url der inspiredienste'),
            'contactorganisation': ('Kontaktorganisation'),
            'contactperson': ('Kontaktperson'),
            'ows_hoursofservice': ('Dienstzeiten'),
            'ows_contactinstructions': ('Art der Kontaktaufnahme'),
            'contactposition': ('Kontaktposition'),
            'contactvoicetelephone': ('Telefonnummer'),
            'ows_contactfacsimiletelephone': ('Faxnummer'),
            'contactelectronicmailaddress': ('Kontakt email Adresse'),
            'postcode': ('Postleitzahl'),
            'address': ('Strasse'),
            'city': ('Ort'),
            'stateorprovince': ('Bundesland'),
            'addresstype': ('Adresstyp'),
            'ows_service_onlineresource': ('Webadresse des Kontaktes'),
            'ows_role': ('Rolle'), 
            'ows_inspire_dsid_code': ('UUID des Layermetadatensatzes'),
            'ows_inspire_dsid_ns': ('Namespace des Layermetadatensatzes'),
            'meta_uri' : ('URL des Layermetadatensatzes'),
            }
        widgets = {
            'ows_inspire_temporal_reference' :forms.Textarea(attrs={'cols': 40, 'rows': 1}) ,          
            'ows_inspire_mpoc_name': forms.Textarea(attrs={'cols': 40, 'rows': 1}),
            'ows_inspire_mpoc_email':forms.Textarea(attrs={'cols': 40, 'rows': 1}),
            'ows_inspire_metadatadate':forms.Textarea(attrs={'cols': 40, 'rows': 1}) ,
            'ows_inspire_resourcelocator':forms.Textarea(attrs={'cols': 40, 'rows': 1}) ,
            'contactperson':forms.Textarea(attrs={'cols': 40, 'rows': 1}) ,
            'contactorganisation':forms.Textarea(attrs={'cols': 40, 'rows': 1}) ,
            'ows_hoursofservice':forms.Textarea(attrs={'cols': 40, 'rows': 1}) ,
            'ows_contactinstructions':forms.Textarea(attrs={'cols': 40, 'rows': 1}) ,
            'contactposition':forms.Textarea(attrs={'cols': 40, 'rows': 1}) ,
            'contactvoicetelephone': forms.Textarea(attrs={'cols': 40, 'rows': 1}),
            'ows_contactfacsimiletelephone': forms.Textarea(attrs={'cols': 40, 'rows': 1}),
            'contactelectronicmailaddress':forms.Textarea(attrs={'cols': 40, 'rows': 1}),
            'postcode':forms.Textarea(attrs={'cols': 40, 'rows': 1}) ,
            'address':forms.Textarea(attrs={'cols': 40, 'rows': 1}) ,
            'city':forms.Textarea(attrs={'cols': 40, 'rows': 1}) ,
            'stateorprovince':forms.Textarea(attrs={'cols': 40, 'rows': 1}) ,
            'addresstype':forms.Textarea(attrs={'cols': 40, 'rows': 1}) ,
            'ows_service_onlineresource': forms.Textarea(attrs={'cols': 40, 'rows': 1}),
            'ows_role':forms.Textarea(attrs={'cols': 40, 'rows': 1}) , 
            'authorityurl_name':forms.Textarea(attrs={'cols': 40, 'rows': 1}) , 
            'authorityurl_href':forms.Textarea(attrs={'cols': 40, 'rows': 1}) ,             
            'ows_inspire_dsid_code':forms.Textarea(attrs={'cols': 40, 'rows': 1}) ,
            'ows_inspire_dsid_ns':forms.Textarea(attrs={'cols': 40, 'rows': 1}) ,
            'meta_uri':forms.Textarea(attrs={'cols': 40, 'rows': 1}),
            'cid':forms.HiddenInput(),
            'inspirelayer':forms.HiddenInput(),
            'sddi':forms.HiddenInput(),
            
        }
            