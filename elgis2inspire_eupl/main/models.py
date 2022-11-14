from django.contrib.gis.db import models
from hb.models import HabitatList
#from model_utils import Choices


class Capabilities(models.Model):
    cid = models.AutoField(primary_key=True)
    ows_inspire_temporal_reference  = models.TextField() 
    ows_inspire_mpoc_name  = models.TextField() 
    ows_inspire_mpoc_email  = models.TextField() 
    ows_inspire_metadatadate  = models.TextField() 
    ows_inspire_resourcelocator  = models.TextField()
    contactperson  = models.TextField()
    contactorganisation = models.TextField() 
    ows_hoursofservice  = models.TextField() 
    ows_contactinstructions  = models.TextField() 
    contactposition  = models.TextField() 
    contactvoicetelephone  = models.TextField() 
    ows_contactfacsimiletelephone  = models.TextField() 
    contactelectronicmailaddress  = models.TextField() 
    postcode  = models.TextField() 
    address  = models.TextField() 
    city  = models.TextField() 
    stateorprovince  = models.TextField() 
    addresstype  = models.TextField()
    ows_service_onlineresource  = models.TextField()
    ows_role  = models.TextField(default='Point of Contact')
    inspirelayer = models.TextField(default='HabitatsandBiotopes')
    sddi = models.IntegerField()
    ows_inspire_dsid_code  = models.TextField()
    ows_inspire_dsid_ns  = models.TextField()
    meta_uri = models.TextField(null=True)
    authorityurl_name = models.TextField()
    authorityurl_href = models.TextField()
    