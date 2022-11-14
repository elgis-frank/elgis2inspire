#-------------------------------------------------------
# Datei ps.views.py Version 1.01 
#
#  Programming by eLGIS
#               
#      Copyright (C) by elgis ( https://elgis.de ) 2022
# Diese Datei ist Bestandteil der Software elgis2inspire, erhältlich unter https://github.com/elgis-frank/elgis2inspire .
# Diese Software wird unter der European Union Public Licence (EUPL-1.2) bereitgestellt. Bitte beachten Sie die Bestimmungen der Lizenz, insbesondere
# zur Bereitstellung und Nutzung der Software und zum Haftungsausschluss. Die Lizenz ist in allen Amtssprachen der EU veröffentlicht unter https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
# 
#--------------------------------------------------------

from pickle import PERSID
from django.shortcuts import render
from django.http import HttpResponse,QueryDict, HttpResponseRedirect
from .models import ProtectedSite, SiteDesignation, SiteProtectionClassification
from django.views.generic.edit import UpdateView
from django.template import loader
from .forms import psGeoForm
from .functions.functions import handle_uploaded_file, dele
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
import json
# Create your views here.

@login_required
def ps(request):
    return render(request, 'ps.html', {})

@login_required
def psgeo(request):
    kenn = request.POST.get('spkenn', 'Null')
    name = request.POST.get('spname', 'Null')
    url = request.POST.get('spurl', 'Null')
    date = request.POST.get('spdate', 'Null')
    sptype = request.POST.get('sptype', 'Null')
    psid = request.POST.get('psid', 'Null')
    psmurl = request.POST.get('psmurl', 'Null')
    
    if request.method == 'POST':
        psgeo = psGeoForm(request.POST, request.FILES)  
        if psgeo.is_valid():
            ergebnis = handle_uploaded_file(request.FILES['datei'], kenn, name, url, date, sptype, psid, psmurl)
            messages.info(request, ergebnis)
            return render(request, 'psok.html')  
    else:
        initial = {"spkenn":"kennung","spname":"name","spurl":"url","spdate":"datum","sptype":"typ" }  
        psgeo = psGeoForm(initial=initial)  
        return render(request,"psgeo.html",{'form':psgeo})

@login_required
def delps(request):
    ergebnis = dele()
    messages.info(request, ergebnis)
    return render(request, 'psok.html') 


